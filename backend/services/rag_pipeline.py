from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from core.config import settings
from db import models
import os
import tempfile

# Use system temp folder to avoid OneDrive/File Lock issues
CHROMA_PATH = os.path.join(tempfile.gettempdir(), "botblocks_chroma_db")

def generate_response(message: str, bot: models.Bot) -> str:
    print(f"--- RAG START: Processing message for bot {bot.public_id} ---")
    
    try:
        # 1. Setup Embeddings (Local)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # 2. Connect to Vector DB
        if not os.path.exists(CHROMA_PATH):
            print("❌ DB Path does not exist!")
            return "I have no memory yet (Database missing)."

        vector_store = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings,
            collection_name=f"collection_{bot.public_id}"
        )
        
        # 3. Check for Data
        doc_count = 0
        try:
            doc_count = vector_store._collection.count()
        except Exception as e:
            print(f"❌ Error counting docs (Collection might not exist): {e}")
            return "I haven't been trained yet."

        # 4. Setup LLM - USING THE MODEL WE VERIFIED EXISTS
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",  # <--- CRITICAL UPDATE
            temperature=0.3,
            google_api_key=settings.GOOGLE_API_KEY,
            transport="rest"
        )

        # 5. Handle Empty DB Case
        if doc_count == 0:
            print("⚠️ Collection is empty. Falling back to LLM only.")
            return llm.invoke(message).content

        # 6. Create Retriever & Prompt
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})

        template = f"""{bot.system_prompt}
        
        Answer based ONLY on the following context. 
        If the answer isn't in the context, say "I don't see that in the report."
        
        Context:
        {{context}}
        
        Question: {{question}}
        """
        prompt = ChatPromptTemplate.from_template(template)
        
        def format_docs(docs):
            return "\n\n".join([d.page_content for d in docs])

        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        print(f"4. Invoking Chain with model: {llm.model}...")
        response = rag_chain.invoke(message)
        print("✅ Success!")
        return response

    except Exception as e:
        print(f"❌ CRITICAL RAG ERROR: {str(e)}")
        if "404" in str(e):
            return "Error: The selected AI model version is not available in your region. Please try updating the model name in backend/services/rag_pipeline.py"
        return f"I encountered an internal error: {str(e)}"