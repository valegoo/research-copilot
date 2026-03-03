import os
import sys
from dotenv import load_dotenv

# Add the project root and backend to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from src.rag_pipeline import RAGPipeline

def main():
    load_dotenv()
    
    print("🚀 Starting document ingestion...")
    
    # Initialize the RAG Pipeline
    pipeline = RAGPipeline(
        persist_dir="backend/chroma_db",
        lecturas_dir="Lecturas"
    )
    
    # Index documents (force re-index to be sure)
    print("📦 Processing PDFs and creating vector store...")
    pipeline.initialize_index(force=True)
    
    print("✅ Ingestion complete! Your papers are now indexed in ChromaDB.")

if __name__ == "__main__":
    main()
