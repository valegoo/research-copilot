import streamlit as st

def display_citation(paper_title: str, authors: str, year: int, page: int = None, quote: str = None):
    """Formats and displays an APA citation with optional quote in a pastel light box."""
    citation_text = f"{authors} ({year}). {paper_title}."
    if page:
        citation_text += f" p. {page}."
        
    st.markdown(f"""
        <div style="background: #F1F5F9; padding: 1.25rem; border-left: 5px solid #A5B4FC; border-radius: 12px; margin-top: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <p style="font-style: italic; margin-bottom: 0.75rem; color: #1E293B !important;">"{quote or 'No specific quote provided'}"</p>
            <p style="font-size: 0.85rem; color: #64748B !important; margin-top: 0.5rem;">
                <b style="color: #4338CA !important;">Source:</b> {citation_text}
            </p>
        </div>
    """, unsafe_allow_html=True)
