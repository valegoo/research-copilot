import os
import sys
from dotenv import load_dotenv

# Ensure we can import from the backend/src directory
sys.path.append(os.path.join(os.getcwd(), "backend"))
sys.path.append(os.path.join(os.getcwd(), "backend", "src"))

from src.rag_pipeline import RAGPipeline

def finish_indexing():
    print("🔄 Initializing RAG Pipeline...")
    # Using the same path as in app/main.py
    pipeline = RAGPipeline(
        persist_dir="backend/chroma_db", 
        lecturas_dir="Lecturas"
    )
    
    print("📚 Starting indexing of 21 documents... this might take a moment.")
    pipeline.initialize_index(force=True)
    
    print("\n✅ Verification Query:")
    answer, citations = pipeline.query("What are the main characteristics of neoliberalism described in the papers?")
    print("-" * 50)
    print(answer)
    print("-" * 50)
    print(f"Total Citations found: {len(citations)}")
    print("Done!")

if __name__ == "__main__":
    load_dotenv()
    finish_indexing()
