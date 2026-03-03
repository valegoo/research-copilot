import os
from openai import OpenAI
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

class OpenAIEmbedder:
    def __init__(self, model: str = "text-embedding-3-small"):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            # Structurally ready, but logically blocked without key
            print("⚠️ Warning: OPENAI_API_KEY not found in environment. OpenAIEmbedder will fail if used.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts."""
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY must be set in environment variables.")
            
        response = self.client.embeddings.create(
            model=self.model,
            input=texts
        )
        return [item.embedding for item in response.data]

    def embed_query(self, query: str) -> List[float]:
        """Generate embedding for a single query."""
        return self.embed_texts([query])[0]

if __name__ == "__main__":
    # Test (will fail if no API key is set)
    try:
        embedder = OpenAIEmbedder()
        print("Embedder initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize embedder: {e}")
