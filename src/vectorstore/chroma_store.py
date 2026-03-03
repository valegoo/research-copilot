import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional

class ChromaVectorStore:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = None

    def create_collection(self, name: str):
        """Create or get a collection."""
        self.collection = self.client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(
        self,
        ids: List[str],
        documents: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict]
    ):
        """Add documents with embeddings and metadata."""
        if not self.collection:
            raise ValueError("Collection not initialized.")
            
        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def query(
        self,
        query_embedding: List[float],
        n_results: int = 5,
        where: Dict = None
    ) -> List[Dict]:
        """
        Query similar documents and return results in the requested format.
        """
        if not self.collection:
            raise ValueError("Collection not initialized.")
            
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where,
            include=["documents", "metadatas", "distances"]
        )

        # Reformat results to match the desired output
        formatted_results = []
        for i in range(len(results["ids"][0])):
            formatted_results.append({
                "chunk_id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "similarity_score": 1 - results["distances"][0][i]  # Convert distance to score if needed
            })
            
        return formatted_results

if __name__ == "__main__":
    # Test (local database, no OpenAI needed for the DB itself)
    store = ChromaVectorStore(persist_directory="test_db")
    store.create_collection("test_collection")
    print("Vector Store initialized successfully.")
