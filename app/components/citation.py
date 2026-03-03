import streamlit as st

def display_citation(paper_title: str, authors: str, year: int, page: int = None, quote: str = None):
    """Formats and displays an APA citation with optional quote."""
    citation_text = f"{authors} ({year}). {paper_title}."
    if page:
        citation_text += f" p. {page}."
        
    st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.5); padding: 1rem; border-left: 4px solid #6366F1; border-radius: 4px; margin-top: 1rem;">
            <p style="font-style: italic; margin-bottom: 0.5rem;">"{quote or 'No specific quote provided'}"</p>
            <p style="font-size: 0.85rem; color: #94A3B8;"><b>Source:</b> {citation_text}</p>
        </div>
    """, unsafe_allow_html=True)
