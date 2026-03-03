import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

class VectorStoreManager:
    def __init__(self, persist_directory: str = "db"):
        self.persist_directory = os.path.join(os.getcwd(), persist_directory)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        self.vector_store = None

    def create_or_load_store(self, documents: List[Dict]):
        """Creates a new vector store or loads an existing one."""
        if os.path.exists(self.persist_directory) and len(os.listdir(self.persist_directory)) > 0:
            print("Loading existing vector store...")
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        else:
            print("Creating new vector store...")
            langchain_docs = []
            for doc in documents:
                chunks = self.text_splitter.split_text(doc["text"])
                for i, chunk in enumerate(chunks):
                    metadata = doc["metadata"].copy()
                    metadata["chunk_id"] = i
                    langchain_docs.append(Document(page_content=chunk, metadata=metadata))
            
            self.vector_store = Chroma.from_documents(
                documents=langchain_docs,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
        return self.vector_store

    def similarity_search(self, query: str, k: int = 5):
        if not self.vector_store:
            raise ValueError("Vector store not initialized")
        return self.vector_store.similarity_search(query, k=k)

if __name__ == "__main__":
    # Test vector store logic
    # Requires OPENAI_API_KEY environment variable
    pass
