import streamlit as st

def display_paper_card(paper: dict):
    """Displays a stylized paper card with high visibility and spacing to avoid overlaps."""
    st.markdown(f"""
        <div class="paper-card">
            <h3 style="color: #1E1B4B !important; margin-bottom: 0.25rem;">{paper["title"]}</h3>
            <p style="color: #64748B !important; margin-top: -0.25rem; font-style: italic; font-weight: 500;">{paper["author"]}</p>
            <div style="margin-top: 1rem; margin-bottom: 1rem; clear: both; display: block;">
                <span class="badge badge-year">{paper["year"]}</span>
                <span class="badge badge-topic">{paper["topic"]}</span>
            </div>
            <p style="color: #334155 !important; font-size: 0.95rem; line-height: 1.5; margin-bottom: 1rem;">{paper["abstract"][:150]}...</p>
        </div>
    """, unsafe_allow_html=True)
