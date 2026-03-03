import streamlit as st

def display_paper_card(paper: dict):
    """Displays a stylized paper card for the browser."""
    st.markdown(f"""
        <div class="paper-card">
            <h3>{paper["title"]}</h3>
            <p style="color: #94A3B8; margin-top: -0.5rem; font-style: italic;">{paper["author"]}</p>
            <div style="margin-top: 1rem;">
                <span class="badge badge-year">{paper["year"]}</span>
                <span class="badge badge-topic">{paper["topic"]}</span>
            </div>
            <p style="margin-top: 1rem; font-size: 0.9rem;">{paper["abstract"][:200]}...</p>
        </div>
    """, unsafe_allow_html=True)
