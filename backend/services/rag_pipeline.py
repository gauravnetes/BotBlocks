from sqlalchemy.orm import Session
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.config import settings
from db import models
import os
import tempfile
import json
import logging
import re

# logging config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RAG_Pipeline")

# Use system temp folder to avoid OneDrive/File Lock issues
CHROMA_PATH = os.path.join(tempfile.gettempdir(), "botblocks_chroma_db")
class HallucinationGuard:
    def clean_json_text(self, text: str) -> str:
        text = re.sub(r'^```json\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'^```\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'```$', '', text, flags=re.MULTILINE)
        return text.strip()
    
    def validate(self, context_text: str, llm_response_raw: str, threshold: float = 0.7):
        
        try:
            cleaned_res = self.clean_json_text(llm_response_raw)
            data = json.loads(cleaned_res)
            
            ans = data.get("response", "I encountered an error")
            quote = data.get("source_quote")
            confidence = data.get("confidence", 0.0)
            
            metadata = {
                "confidence": confidence, 
                "source_quote": quote, 
                "hallucination_warning": False, 
                "flagged_as_gap": False
            }
            
            if confidence == 0.0 or "don't see that in the report" in ans.lower():
                metadata["flagged_as_gap"] = True
                return True, ans, metadata
            
            if 0.0 < confidence < threshold:
                logger.warning(f"GUARD: Low confidence ({confidence}).")
                metadata["hallucination_warning"] = True
                metadata['flagged_as_gap'] = True
                
                warning_msg = "⚠️ *I'm not 100% sure about this, but here is what I found:* \n\n"
                return False, warning_msg + ans, metadata
            
            if quote:
                def normalize(s): return " ".join(s.lower().split())
                
                if normalize(quote) not in normalize(context_text):
                    logger.warning(f"GUARD: Hallucination Detected. Quote '{quote}' NOT FOUND in context")
                    metadata["hallucination_warning"] = True
                    metadata["flagged_as_gap"] = True
                    return False, "I detected a factual inconsistency in my reasoning and blocked the response."
                
            if confidence > 0.8 and not quote:
                if "don't know" not in ans.lower():
                    logger.warning(f"GUARD: High confidence claim without any evidence")
                    
            return True, ans, metadata
        
        except json.JSONDecodeError:
            return False, "I had trouble verifying my own answer.", {"error": "JSON Parse Fail"}
        
    
def generate_response(message: str, bot: models.Bot, db: Session) -> str:
    print(f"RAG START: Processing message for bot {bot.public_id}")
    
    try:
        # 1. Setup Embeddings (Local)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # 2. Connect to Vector DB
        if not os.path.exists(CHROMA_PATH):
            print("DB Path does not exist!")
            return "I have no memory yet (Database missing)."

        vector_store = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings,
            collection_name=f"collection_{bot.public_id}"
        )
        
        # Check for Data
        try:
            doc_count = vector_store._collection.count()
            if doc_count == 0: 
                print("Collection is empty")
                return "I haven't been trained with any decisions yet."
        except Exception as e:
            return "I haven't been trained yet."

        # Setup LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.1, # prev -> 0.3
            google_api_key=settings.GOOGLE_API_KEY,
            transport="rest"
        )
        
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        docs = retriever.invoke(message)
        
        context_text = "\n\n".join()

        # Handle Empty DB Case
        if doc_count == 0:
            print("⚠️ Collection is empty. Falling back to LLM only.")
            return llm.invoke(message).content

        # 6. Create Retriever & Prompt
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})

        docs = retriever.invoke(message)
        
        context_text = "\n\n".join([d.page_content for d in  docs])
        
        sysytem_prompt = f"""{bot.system_prompt} 
                
        INSTRUCTIONS:
        1. Answer the question based ONLY on the provided Context.
        2. You must return your answer in valid JSON format with these keys:
           - "response": (string) Your natural language answer to the user.
           - "source_quote": (string or null) Copy the EXACT sentence from the Context that proves your answer.
           - "confidence": (float) 0.0 to 1.0 score of how well the context supports the answer.
        3. IF YOU CANNOT ANSWER:
           - "response": "I don't see that in the report"
           - "source_quote": null
           - "confidence": 0.0
        """
        prompt = ChatPromptTemplate.from_template("""
        {system_prompt}
        
        Context: 
        {context}
        
        Question: {question}                                          
                      
        """)
        
        print("Generating Response...")
        chain = prompt | llm
        
        raw_response = chain.invoke({
            "system_prompt": sysytem_prompt, 
            "context": context_text, 
            "question": message
        })
        
        guard = HallucinationGuard()
        is_safe, final_ans, metadata = guard.validate(context_text, raw_response.content)
        try:
            audit_entry = models.BotAuditLog(
                bot_id = bot.id, 
                user_query = message, 
                bot_res = final_ans, 
                confidence_score = metadata.get('confidence', 0.0), 
                flagged_as_gap = metadata.get('flagged_as_gap', False)
            )
            
            db.add(audit_entry)
            db.commit()
            print("Audit Log Saved")
            
        except Exception as log_error: 
            print(f"Failed to save audit log: {log_error}")
        
        if is_safe: 
            print("GUARD Passed")
            return final_ans
        else: 
            print("GUARD Blocked Response")
            return  f"{final_ans}"

    except Exception as e:
        print(f"CRITICAL RAG ERROR: {str(e)}")
        if "404" in str(e):
            return "Error: Model not found. Check API key or Model Name."
        return f"I encountered an internal error: {str(e)}"
    
    
def add_document_to_knowledge_base(bot_id: int, file_content: str, source_filename: str):
    
    print(f"RAG: Training bot {bot_id} with file: {source_filename}")
    
    try: 
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        vector_store = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings,
            collection_name=f"collection_{bot_id}"
        )
        
        raw_doc = Document(
            page_content=file_content, 
            metadata={"source": source_filename}
        )
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=100
        )
        
        chunks = text_splitter.split_documents([raw_doc])
        
        print(f"Created {len(chunks)} chunks from {source_filename}")
        
        vector_store.add_documents(chunks)
        
        print(f"RAG: Training Complete")
        return True
    
    except Exception as e:
        print(f" RAG Error: {e}")
        return False

def remove_document_from_knowledge_base(bot_id: int, source_filename: str):
    
    print(f"RAG: Untraining bot {bot_id} (removing {source_filename})...")
    
    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_store = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings,
            collection_name=f"collection_{bot_id}"
        )
        
        vector_store._collection.delete(
            where={"source": source_filename}
        )
        
        print(f"RAG: Removed knowledge derived from {source_filename}")
        return True

    except Exception as e:
        print(f"RAG Delete Error: {e}")
        return False