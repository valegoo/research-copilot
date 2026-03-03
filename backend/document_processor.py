import os
from pypdf import PdfReader
from typing import List, Dict

class DocumentProcessor:
    def __init__(self, directory_path: str):
        self.directory_path = directory_path
        self.documents = []

    def load_documents(self) -> List[Dict]:
        """Loads and extracts text from all PDF files in the directory."""
        pdf_files = [f for f in os.listdir(self.directory_path) if f.lower().endswith('.pdf')]
        
        extracted_docs = []
        for filename in pdf_files:
            file_path = os.path.join(self.directory_path, filename)
            try:
                reader = PdfReader(file_path)
                text = ""
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                
                if text.strip():
                    extracted_docs.append({
                        "id": filename,
                        "text": text,
                        "metadata": {
                            "source": filename,
                            "path": file_path,
                            "title": filename.replace(".pdf", "")
                        }
                    })
                    print(f"Loaded: {filename}")
            except Exception as e:
                print(f"Error loading {filename}: {e}")
                
        self.documents = extracted_docs
        return extracted_docs

if __name__ == "__main__":
    # Test loading
    lecturas_path = r"C:\Users\vgonzales\Documents\Tarea 1 - Prompt\Lecturas"
    processor = DocumentProcessor(lecturas_path)
    docs = processor.load_documents()
    print(f"Total documents loaded: {len(docs)}")
