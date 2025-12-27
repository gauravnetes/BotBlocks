from sqlalchemy.orm import Session
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.config import settings
from db import models
import os
import tempfile
import json
import logging
import re
from typing import Tuple, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RAG_Pipeline")

CHROMA_PATH = os.path.join(tempfile.gettempdir(), "botblocks_chroma_db")

# ============================================================================
# SEMANTIC ROUTER - Save tokens on simple queries
# ============================================================================
class SemanticRouter:
    """Classifies queries to determine if RAG is needed"""
    
    GREETING_PATTERNS = [
        r'\b(hi|hello|hey|greetings|good morning|good evening)\b',
        r'\bhow are you\b',
        r'\bwhat\'?s up\b',
    ]
    
    IDENTITY_PATTERNS = [
        r'\bwho are you\b',
        r'\bwhat are you\b',
        r'\bwhat can you do\b',
        r'\bwhat is your (name|purpose)\b',
        r'\btell me about yourself\b',
    ]
    
    @staticmethod
    def should_skip_rag(query: str) -> Tuple[bool, str]:
        """Returns (should_skip, route_type)"""
        query_lower = query.lower().strip()
        
        for pattern in SemanticRouter.GREETING_PATTERNS:
            if re.search(pattern, query_lower):
                return True, 'greeting'
        
        for pattern in SemanticRouter.IDENTITY_PATTERNS:
            if re.search(pattern, query_lower):
                return True, 'identity'
        
        return False, 'rag'

# ============================================================================
# HALLUCINATION GUARD - Validate LLM responses
# ============================================================================
class HallucinationGuard:
    """Validates LLM responses to prevent hallucinations"""
    
    def clean_json_text(self, text: str) -> str:
        """Extract JSON from markdown-wrapped or raw text"""
        try:
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return match.group(0).strip()
            
            text = re.sub(r'^```json\s*', '', text, flags=re.MULTILINE)
            text = re.sub(r'^```\s*', '', text, flags=re.MULTILINE)
            text = re.sub(r'```$', '', text, flags=re.MULTILINE)
            return text.strip()
        except Exception as e:
            logger.error(f"JSON cleaning error: {e}")
            return text.strip()
    
    def validate(self, context_text: str, llm_response_raw: str, threshold: float = 0.7) -> Tuple[bool, str, Dict[str, Any]]:
        """Validates LLM response against context"""
        try:
            cleaned_res = self.clean_json_text(llm_response_raw)
            data = json.loads(cleaned_res)
            
            ans = data.get("response") or data.get("answer", "I encountered an error")
            confidence = data.get("confidence", 0.0)
            is_out_of_scope = data.get("out_of_scope", False)
            
            metadata = {
                "confidence": confidence, 
                "hallucination_warning": False, 
                "flagged_as_gap": False,
                "out_of_scope": is_out_of_scope,
                "gap_type": None  # "missing_knowledge" or "out_of_scope"
            }
            
            # Check for explicit knowledge gaps
            gap_phrases = [
                "don't see that in the report",
                "don't have information about",
                "not found in the context",
                "cannot find",
            ]
            
            # OUT OF SCOPE - Don't log these (e.g., asking medical bot about cooking)
            if is_out_of_scope or confidence == 0.0:
                if is_out_of_scope:
                    logger.info("GUARD: Query is out of scope - NOT LOGGING")
                    metadata["out_of_scope"] = True
                else:
                    logger.info("GUARD: Zero confidence knowledge gap detected")
                    metadata["flagged_as_gap"] = True
                    metadata["gap_type"] = "missing_knowledge"
                
                return True, ans, metadata
            
            # LOW CONFIDENCE - This is a knowledge gap worth tracking
            if 0.0 < confidence < threshold:
                logger.warning(f"GUARD: Low confidence ({confidence}) - knowledge gap")
                metadata["flagged_as_gap"] = True
                metadata["gap_type"] = "missing_knowledge"
                warning_msg = "⚠️ *I'm not completely certain, but here's what I found:*\n\n"
                return True, warning_msg + ans, metadata
            
            # HIGH CONFIDENCE - Successful answer, no logging needed
            logger.info(f"GUARD: High confidence ({confidence}) - successful answer")
            return True, ans, metadata
        
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e}")
            return False, "I had trouble verifying my answer.", {"error": "JSON Parse Failed"}
        except Exception as e:
            logger.error(f"Validation error: {e}")
            return False, "An error occurred during validation.", {"error": str(e)}

# ============================================================================
# AUDIT LOGGER - Only logs knowledge gaps
# ============================================================================
def log_knowledge_gap(bot: models.Bot, message: str, response: str, metadata: Dict[str, Any], db: Session):
    """
    Selective logging: Only saves queries that reveal knowledge gaps.
    This keeps analytics clean and actionable.
    """
    try:
        # Only log if it's a real knowledge gap (not out-of-scope or successful)
        if metadata.get("flagged_as_gap") and metadata.get("gap_type") == "missing_knowledge":
            audit_entry = models.BotAuditLog(
                bot_id=bot.id,
                user_query=message,
                bot_response=response,
                confidence_score=metadata.get('confidence', 0.0),
                flagged_as_gap=True
            )
            db.add(audit_entry)
            db.commit()
            logger.info("✅ Knowledge gap logged for analytics")
        else:
            logger.info("✅ Successful answer - no logging needed")
    except Exception as log_error:
        logger.error(f"Audit log error: {log_error}")

# ADAPTIVE RETRIEVAL
def get_adaptive_k(query: str) -> int:
    """Determine optimal number of documents based on query complexity"""
    word_count = len(query.split())
    
    # For short general queries like "results", retrieve more chunks
    if word_count <= 5:
        return 5  # Increased from 3
    elif word_count <= 15:
        return 7  # Increased from 5
    else:
        return 9  # Increased from 7


# MAIN RAG FUNCTION - OPTIMIZED
def generate_response(message: str, bot: models.Bot, db: Session) -> str:
    """Main RAG pipeline with selective audit logging"""
    logger.info(f"RAG START: Processing message for bot {bot.public_id}")
    
    try:
        # STEP 1: SEMANTIC ROUTING (No logging for these)
        should_skip, route_type = SemanticRouter.should_skip_rag(message)
        
        if should_skip:
            logger.info(f"ROUTER: Skipping RAG for {route_type} query (token savings)")
            
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                temperature=0.7,
                google_api_key=settings.GOOGLE_API_KEY,
                transport="rest"
            )
            
            if route_type == 'greeting':
                prompt = f"{bot.system_prompt}\n\nUser said: {message}\n\nRespond warmly and briefly."
            else:
                prompt = f"{bot.system_prompt}\n\nUser asked: {message}\n\nIntroduce yourself based on your role."
            
            response = llm.invoke(prompt).content
            # ✅ NO LOGGING - These are normal conversations
            return response
        
        # STEP 2: SETUP EMBEDDINGS & VECTOR STORE
        embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        collection_name = f"collection_{bot.public_id}"
        logger.info(f"📦 Using collection: {collection_name}")
        
        if not os.path.exists(CHROMA_PATH):
            os.makedirs(CHROMA_PATH, exist_ok=True)
        
        vector_store = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings,
            collection_name=collection_name,
            collection_metadata={"hnsw:space": "cosine"}
        )
        
        # STEP 3: CHECK FOR DOCUMENTS
        try:
            doc_count = vector_store._collection.count()
            logger.info(f"Collection '{collection_name}' has {doc_count} documents")
            
            if doc_count == 0:
                logger.warning("Collection is empty - no training data")
                gap_response = "I haven't been trained with any documents yet. Please upload training materials first."
                
                # ✅ LOG THIS - Empty knowledge base is a critical gap
                metadata = {"confidence": 0.0, "flagged_as_gap": True, "gap_type": "missing_knowledge"}
                log_knowledge_gap(bot, message, gap_response, metadata, db)
                
                return gap_response
        
        except Exception as e:
            logger.error(f"Error checking collection: {e}")
            return "I encountered an error accessing my knowledge base."
        
        # STEP 4: ADAPTIVE RETRIEVAL WITH HIGHER K
        k = get_adaptive_k(message)
        # Retrieve more docs to ensure we get both methodology AND results sections
        k = min(k + 3, 10)  # Add 3 more docs, cap at 10
        docs_with_scores = vector_store.similarity_search_with_relevance_scores(message, k=k)
        
        if not docs_with_scores:
            logger.warning("KNOWLEDGE GAP: No documents found")
            gap_response = "I don't see that in the report."
            
            # ✅ LOG THIS - Relevant query but no matching documents
            metadata = {"confidence": 0.0, "flagged_as_gap": True, "gap_type": "missing_knowledge"}
            log_knowledge_gap(bot, message, gap_response, metadata, db)
            
            return gap_response
        
        # Log scores for debugging
        best_score = docs_with_scores[0][1]
        logger.info(f"📊 Best relevance score: {best_score:.3f}")
        logger.info(f"📊 Retrieved {len(docs_with_scores)} documents")
        
        # ADAPTIVE THRESHOLD: Lower for general questions that need multiple chunks
        # Questions like "results" or "outcome" need context from multiple sections
        threshold = 0.30 if best_score < 0.50 else 0.35
        
        # SMART THRESHOLD: Distinguish between "low relevance" and "missing knowledge"
        if best_score < threshold:
            logger.warning(f"KNOWLEDGE GAP: Best match score {best_score:.3f} is too low")
            gap_response = "I don't see that in the report."
            
            # ✅ LOG THIS - Relevant query but weak matches
            metadata = {"confidence": 0.0, "flagged_as_gap": True, "gap_type": "missing_knowledge"}
            log_knowledge_gap(bot, message, gap_response, metadata, db)
            
            return gap_response
        
        # Filter docs with acceptable scores (use dynamic threshold)
        docs = [doc for doc, score in docs_with_scores if score >= threshold]
        
        if len(docs) == 0:
            logger.warning("KNOWLEDGE GAP: No documents passed threshold")
            gap_response = "I don't see that in the report."
            
            # ✅ LOG THIS
            metadata = {"confidence": 0.0, "flagged_as_gap": True, "gap_type": "missing_knowledge"}
            log_knowledge_gap(bot, message, gap_response, metadata, db)
            
            return gap_response
        
        # STEP 5: BUILD CONTEXT
        context_text = "\n\n".join([d.page_content for d in docs])
        logger.info(f"📄 Context length: {len(context_text)} characters")
        
        # STEP 6: SETUP LLM WITH IMPROVED PROMPT
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.1,
            google_api_key=settings.GOOGLE_API_KEY,
            transport="rest"
        )
        
        # ✅ SIMPLIFIED PROMPT - Minimal tokens, maximum clarity
        cached_system_instructions = f"""You are: {bot.system_prompt}

Answer using ONLY the Context below.

Rules:
- If Context has the answer (even partial): Give it, confidence 0.5-1.0
- If question is unrelated to your purpose: confidence 0.0, out_of_scope true
- If relevant but Context truly has nothing: confidence 0.0, out_of_scope false

Note: "results" = "accuracy" = "metrics" = "performance" (same meaning)

JSON format:
{{"response": "answer", "confidence": 0.0-1.0, "out_of_scope": true/false}}"""
        
        prompt = ChatPromptTemplate.from_template("""
{system_instructions}

Context:
{context}

Question: {question}

Respond with valid JSON only.
""")
        
        # STEP 7: GENERATE RESPONSE
        logger.info("Generating LLM response...")
        chain = prompt | llm
        
        raw_response = chain.invoke({
            "system_instructions": cached_system_instructions,
            "context": context_text,
            "question": message
        })
        
        # STEP 8: HALLUCINATION GUARD
        guard = HallucinationGuard()
        is_safe, final_ans, metadata = guard.validate(context_text, raw_response.content)
        
        # STEP 9: SELECTIVE AUDIT LOGGING
        log_knowledge_gap(bot, message, final_ans, metadata, db)
        
        return final_ans
    
    except Exception as e:
        logger.error(f"CRITICAL RAG ERROR: {str(e)}", exc_info=True)
        
        if "404" in str(e):
            return "Error: Model not found. Check API key or model name."
        
        return f"I encountered an internal error. Please try again later."

# ============================================================================
# KNOWLEDGE BASE MANAGEMENT
# ============================================================================
def add_document_to_knowledge_base(bot_id: str, file_content: str, source_filename: str) -> bool:
    """Add document to knowledge base with improved chunking"""
    logger.info(f"RAG: Training bot {bot_id} with file: {source_filename}")
    
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        collection_name = f"collection_{bot_id}"
        
        vector_store = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings,
            collection_name=collection_name,
            collection_metadata={"hnsw:space": "cosine"}
        )
        
        raw_doc = Document(
            page_content=file_content,
            metadata={"source": source_filename}
        )
        
        # Improved chunking: Larger chunks with more overlap to keep related info together
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,  # Increased from 800 to keep results + methodology together
            chunk_overlap=250,  # Increased from 150 to ensure context continuity
            separators=["\n\n", "\n", ". ", " ", ""]  # Smart splitting
        )
        
        chunks = text_splitter.split_documents([raw_doc])
        logger.info(f"Created {len(chunks)} chunks from {source_filename}")
        
        vector_store.add_documents(chunks)
        logger.info(f"RAG: Training complete for {source_filename}")
        
        return True
    
    except Exception as e:
        logger.error(f"RAG Training Error: {e}", exc_info=True)
        return False

def remove_document_from_knowledge_base(bot_id: str, source_filename: str) -> bool:
    """Remove a document from the bot's knowledge base"""
    logger.info(f"RAG: Removing {source_filename} from bot {bot_id}")
    
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        collection_name = f"collection_{bot_id}"
        
        vector_store = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings,
            collection_name=collection_name,
            collection_metadata={"hnsw:space": "cosine"}
        )
        
        vector_store._collection.delete(
            where={"source": source_filename}
        )
        
        logger.info(f"RAG: Removed knowledge from {source_filename}")
        return True
    
    except Exception as e:
        logger.error(f"RAG Delete Error: {e}", exc_info=True)
        return False