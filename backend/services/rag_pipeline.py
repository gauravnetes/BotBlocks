from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from core.config import settings
from db import models

CHROMA_PATH = "./data/chroma_db"

def generate_response(message: str, bot: models.Bot) -> str:
    """
    Robust RAG Pipeline (Chain).
    Instead of a complex Agent, we use a direct Chain:
    1. Search Vector DB
    2. Add Context to Prompt
    3. Ask LLM
    """
    
    # --- 1. Setup Embeddings & DB Connection ---
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=settings.GOOGLE_API_KEY
    )
    
    vector_store = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings,
        collection_name=f"collection_{bot.public_id}"
    )
    
    # Create the Retriever (The "Search Engine")
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # --- 2. Setup the LLM ---
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.3,
        google_api_key=settings.GOOGLE_API_KEY
    )

    # --- 3. Create the Prompt ---
    # We inject the Bot's custom Persona here
    template = f"""{bot.system_prompt}

    Answer the question based ONLY on the following context:
    {{context}}

    Question: {{question}}
    """
    
    prompt = ChatPromptTemplate.from_template(template)

    # --- 4. Build the Chain (The "Pipeline") ---
    # This is LCEL (LangChain Expression Language)
    # It says: Take input -> Search DB (Retriever) -> Format Prompt -> Ask Gemini -> Return Text
    
    def format_docs(docs):
        return "\n\n".join([d.page_content for d in docs])

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # --- 5. Run It ---
    try:
        # Check if DB is empty first to avoid crashes
        doc_count = vector_store._collection.count()
        if doc_count == 0:
            # Fallback if no data uploaded yet: Just chat normally
            simple_prompt = ChatPromptTemplate.from_template(f"{bot.system_prompt}\n\nUser: {{question}}")
            simple_chain = simple_prompt | llm | StrOutputParser()
            return simple_chain.invoke({"question": message})
            
        return rag_chain.invoke(message)
        
    except Exception as e:
        print(f"RAG Error: {e}")
        return "I'm having trouble accessing my memory right now."