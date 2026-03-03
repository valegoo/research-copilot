import os
import sys
# Ensure we can import from the src directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ingestion.processor import DocumentIngestor
from chunking.chunker import TokenChunker
from embedding.embedder import OpenAIEmbedder
from vectorstore.chroma_store import ChromaVectorStore
from prompts.strategies import PromptManager
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class RAGPipeline:
    def __init__(self, persist_dir: str = "chroma_db", lecturas_dir: str = "papers"):
        self.lecturas_dir = lecturas_dir
        self.persist_dir = persist_dir
        
        # Initialize components
        self.ingestor = DocumentIngestor(lecturas_dir)
        self.chunker = TokenChunker(chunk_size=512, chunk_overlap=50)
        self.embedder = OpenAIEmbedder()
        self.vector_store = ChromaVectorStore(persist_directory=persist_dir)
        self.vector_store.create_collection("papers_collection")
        
        self.client = OpenAI() # For direct generation

    def initialize_index(self, force: bool = False):
        """Processes documents and populates the vector store if empty."""
        # Simple check if already indexed (could be more robust)
        try:
            count = self.vector_store.collection.count()
            if count > 0 and not force:
                print(f"✅ Index already exists with {count} chunks.")
                return
        except:
            pass

        print("🚀 Building index...")
        docs = self.ingestor.process_all_documents()
        
        all_ids = []
        all_texts = []
        all_embeddings = []
        all_metadatas = []
        
        for doc in docs:
            # Process one doc at a time to reduce memory pressure
            chunks = self.chunker.chunk_text(doc["text"], metadata=doc["metadata"])
            for chunk in chunks:
                # Sanitize metadata for ChromaDB (no None, lists or complex dicts allowed)
                sanitized_meta = {}
                for k, v in chunk["metadata"].items():
                    if v is not None:
                        if isinstance(v, (str, int, float, bool)):
                            sanitized_meta[k] = v
                        else:
                            sanitized_meta[k] = str(v)
                
                chunk_id = f"{doc['id']}_ch{chunk['chunk_id']}"
                all_ids.append(chunk_id)
                all_texts.append(chunk["text"])
                all_metadatas.append(sanitized_meta)
                
        # Generate embeddings in batches for efficiency
        print(f"🧠 Generating embeddings for {len(all_texts)} chunks...")
        # (Using a simpler batch approach for the example)
        batch_size = 50
        for i in range(0, len(all_texts), batch_size):
            batch_texts = all_texts[i:i+batch_size]
            batch_embeddings = self.embedder.embed_texts(batch_texts)
            all_embeddings.extend(batch_embeddings)
            
        self.vector_store.add_documents(
            ids=all_ids,
            documents=all_texts,
            embeddings=all_embeddings,
            metadatas=all_metadatas
        )
        print("✨ Indexing complete.")

    def query(self, question: str, strategy: str = "Standard", filter_papers: list = None):
        """Runs the RAG flow: Retrieve -> Prompt -> Generate."""
        # Mapping UI names to internal version keys
        strategy_map = {
            "Standard": "v1",
            "JSON Output": "v2",
            "Few-Shot": "v3",
            "Chain-of-Thought": "v4"
        }
        version = strategy_map.get(strategy, "v1")
        
        # 1. Retrieval
        query_emb = self.embedder.embed_query(question)
        
        # Apply filters if provided
        where_clause = None
        if filter_papers:
            where_clause = {"source": {"$in": filter_papers}}
            
        retrieved_chunks = self.vector_store.query(
            query_embedding=query_emb,
            n_results=15,
            where=where_clause
        )
        
        # 2. Context Construction
        context_parts = []
        citations = []
        for res in retrieved_chunks:
            source = res["metadata"].get("source", "Unknown")
            page = res["metadata"].get("page_number", "?")
            context_parts.append(f"Source: {source} (Page {page}):\n{res['text']}")
            
            # Extract citation info
            citations.append({
                "paper": res["metadata"].get("title", source),
                "authors": res["metadata"].get("authors", "Unspecified"),
                "year": res["metadata"].get("year", "N/A"),
                "quote": res["text"][:150] + "...",
                "page": page
            })
            
        context_text = "\n\n---\n\n".join(context_parts)
        
        # 3. Prompt Construction
        final_prompt = PromptManager.get_prompt(version, context_text, question)
        
        # 4. Generation
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": final_prompt}]
        )
        
        answer = response.choices[0].message.content
        return answer, citations

if __name__ == "__main__":
    # Test
    pipeline = RAGPipeline(lecturas_dir="papers", persist_dir="chroma_db")
    # pipeline.initialize_index()
    # ans, cites = pipeline.query("What is neoliberalism?")
    # print(ans)
