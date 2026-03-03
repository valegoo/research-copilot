import fitz  # PyMuPDF
import re
import os
from typing import List, Dict

def clean_extracted_text(text: str) -> str:
    """Clean and normalize extracted PDF text."""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)

    # Fix hyphenated words at line breaks
    text = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', text)

    # Remove page numbers and headers (basic pattern)
    text = re.sub(r'\n\d+\n', '\n', text)

    # Normalize quotes
    text = text.replace('"', '"').replace('"', '"')

    return text.strip()

def extract_text_from_pdf(pdf_path: str) -> dict:
    """
    Extract text and metadata from a PDF file.

    Returns:
        dict with keys: text, metadata, pages, extraction_warnings
    """
    doc = fitz.open(pdf_path)

    full_text = ""
    pages = []
    warnings = []

    for page_num, page in enumerate(doc):
        text = page.get_text()
        pages.append({
            "page_number": page_num + 1,
            "text": text,
            "char_count": len(text)
        })
        full_text += f"\n[PAGE {page_num + 1}]\n{text}"

    # Document metadata
    metadata = doc.metadata

    return {
        "text": full_text,
        "metadata": metadata,
        "pages": pages,
        "total_pages": len(doc),
        "extraction_warnings": warnings
    }

class DocumentIngestor:
    """
    Unified class to handle the ingestion pipeline:
    Extraction -> Cleaning
    """
    def __init__(self, Lecturas_dir: str):
        self.Lecturas_dir = Lecturas_dir

    def process_all_documents(self) -> List[Dict]:
        processed_docs = []
        pdf_files = [f for f in os.listdir(self.Lecturas_dir) if f.lower().endswith('.pdf')]
        
        print(f"🚀 Starting Ingestion Pipeline for {len(pdf_files)} documents...")
        
        for filename in pdf_files:
            file_path = os.path.join(self.Lecturas_dir, filename)
            try:
                # 1. Extraction
                raw_data = extract_text_from_pdf(file_path)
                
                # 2. Cleaning
                cleaned_text = clean_extracted_text(raw_data["text"])
                
                processed_docs.append({
                    "id": filename,
                    "raw_text": raw_data["text"],
                    "text": cleaned_text,
                    "metadata": {
                        **raw_data["metadata"],
                        "source": filename,
                        "total_pages": raw_data["total_pages"]
                    }
                })
                print(f"✅ Processed: {filename}")
            except Exception as e:
                print(f"❌ Error processing {filename}: {e}")
                
        return processed_docs

if __name__ == "__main__":
    lecturas_path = r"C:\Users\vgonzales\Documents\Tarea 1 - Prompt\Lecturas"
    ingestor = DocumentIngestor(lecturas_path)
    documents = ingestor.process_all_documents()
    print(f"\n✨ Ingestion Pipeline Complete. Total documents: {len(documents)}")
    
    # Quick sanity check on the first doc
    if documents:
        print(f"Sample snippet from {documents[0]['id']}:")
        print(documents[0]['text'][:200] + "...")
