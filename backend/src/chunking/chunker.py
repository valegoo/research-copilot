import tiktoken
from typing import List, Dict, Optional

class TokenChunker:
    def __init__(
        self,
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        model: str = "gpt-4"
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoder = tiktoken.encoding_for_model(model)

    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        return len(self.encoder.encode(text))

    def chunk_text(self, text: str, metadata: dict = None) -> List[Dict]:
        """
        Split text into overlapping chunks using token counts.

        Returns:
            List of chunk dictionaries with text and metadata
        """
        tokens = self.encoder.encode(text)
        chunks = []

        start = 0
        chunk_id = 0

        while start < len(tokens):
            end = min(start + self.chunk_size, len(tokens))
            chunk_tokens = tokens[start:end]
            chunk_text = self.encoder.decode(chunk_tokens)

            # Prepare metadata for the chunk
            chunk_metadata = (metadata or {}).copy()
            chunk_metadata.update({
                "chunk_id": chunk_id,
                "token_count": len(chunk_tokens),
                "start_token": start,
                "end_token": end
            })

            chunks.append({
                "chunk_id": chunk_id,
                "text": chunk_text,
                "metadata": chunk_metadata
            })

            # Check if we've reached the end
            if end == len(tokens):
                break

            # Advance start based on overlap
            start += self.chunk_size - self.chunk_overlap
            chunk_id += 1

        return chunks

if __name__ == "__main__":
    # Test script for Chunking Comparison
    from processor import DocumentIngestor
    import os
    
    lecturas_path = r"C:\Users\vgonzales\Documents\Tarea 1 - Prompt\Lecturas"
    ingestor = DocumentIngestor(lecturas_path)
    # Process only one small document for the test to save time
    pdf_files = [f for f in os.listdir(lecturas_path) if f.lower().endswith('.pdf')]
    if not pdf_files:
        print("No PDF files found.")
        exit()
        
    # We'll use one document to estimate totals for the table
    test_doc_name = pdf_files[0]
    docs = ingestor.process_all_documents()
    target_doc = next((d for d in docs if d["id"] == test_doc_name), docs[0])
    
    configs = [
        {"name": "Small Chunks", "size": 256, "overlap": 30},
        {"name": "Large Chunks", "size": 1024, "overlap": 100}
    ]
    
    print("\n📊 --- Chunking Comparison Table Data ---")
    print(f"Document: {target_doc['id']}")
    print(f"{'Config':<15} | {'Size':<6} | {'Overlap':<8} | {'Total Chunks':<12} | {'Use Case'}")
    print("-" * 70)
    
    for cfg in configs:
        chunker = TokenChunker(chunk_size=cfg["size"], chunk_overlap=cfg["overlap"])
        chunks = chunker.chunk_text(target_doc["text"])
        use_case = "Precise facts" if cfg["size"] < 500 else "Complex context"
        print(f"{cfg['name']:<15} | {cfg['size']:<6} | {cfg['overlap']:<8} | {len(chunks):<12} | {use_case}")
