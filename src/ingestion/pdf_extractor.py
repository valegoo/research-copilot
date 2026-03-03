import fitz  # PyMuPDF

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

if __name__ == "__main__":
    import os
    test_pdf = r"C:\Users\vgonzales\Documents\Tarea 1 - Prompt\Lecturas\A brief history of neoliberalism (2007).pdf"
    if os.path.exists(test_pdf):
        result = extract_text_from_pdf(test_pdf)
        print(f"Extracted {len(result['pages'])} pages from {test_pdf}")
        print(f"Metadata: {result['metadata']}")
    else:
        print(f"File not found: {test_pdf}")
