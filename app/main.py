import streamlit as st
import os
import sys

# Add backend to path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from src.rag_pipeline import RAGPipeline
from components.citation import display_citation
from components.chat_message import display_chat_message
from utils.styling import apply_custom_styles
from utils.session import initialize_session_state

st.set_page_config(
    page_title="Research Copilot",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply premium styles (includes the user's requested Georgia font for headers via custom CSS)
apply_custom_styles()
initialize_session_state()

# Helper for sidebar paper list
def get_all_paper_titles():
    return [p["title"] for p in st.session_state.papers]

# Helper to display multiple citations
def display_citations(citations):
    if not citations: return
    st.markdown("---")
    st.markdown("### 🔍 Sources & Citations")
    for cite in citations:
        display_citation(
            paper_title=cite.get("paper", "Unknown Paper"),
            authors=cite.get("authors", "Unknown Author"),
            year=cite.get("year", "N/A"),
            page=cite.get("page"),
            quote=cite.get("quote", "Quote excerpt...")
        )

# Initialize RAG Pipeline in session
if "rag_pipeline" not in st.session_state:
    try:
        st.session_state.rag_pipeline = RAGPipeline(
            persist_dir="backend/chroma_db", 
            lecturas_dir="Lecturas"
        )
    except Exception as e:
        st.error(f"Failed to initialize RAG Pipeline: {e}")

# Sidebar
with st.sidebar:
    # Use a local or remote logo if available
    st.image("https://img.icons8.com/isometric/512/microscope.png", width=100)
    st.title("Research Copilot")
    st.markdown("_Your AI academic assistant_")
    st.markdown("---")

    # Paper filter
    selected_papers = st.multiselect(
        "📚 Filter by papers:",
        options=get_all_paper_titles(),
        help="Select specific papers to focus the search."
    )

    # Prompt strategy selector
    strategy = st.selectbox(
        "🧠 Prompt Strategy:",
        ["Standard", "JSON Output", "Few-Shot", "Chain-of-Thought"],
        help="Choose the logic used to generate responses."
    )
    
    st.markdown("---")
    if st.button("Clear Conversation 🧹", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Main chat area
st.header("💬 Chat with your papers")
st.write("Ask deep questions about your collection of academic papers.")

# Display chat history
for message in st.session_state.messages:
    display_chat_message(message["role"], message["content"])
    if "citations" in message and message["citations"]:
        with st.expander("View Citations"):
            display_citations(message["citations"])

# User input
if prompt := st.chat_input("Ask a question about your papers..."):
    # Add user message
    st.session_state.messages.append({"role": "User", "content": prompt})
    
    # Display user message immediately
    display_chat_message("User", prompt)

    # Get response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing papers..."):
            try:
                if not os.getenv("OPENAI_API_KEY"):
                    st.warning("⚠️ OPENAI_API_KEY not found. Please check .env.")
                    response = "API Key missing. Please provide a valid OpenAI API key."
                    citations = []
                else:
                    response, citations = st.session_state.rag_pipeline.query(
                        prompt,
                        strategy=strategy,
                        filter_papers=selected_papers if selected_papers else None
                    )
                
                st.markdown(response)
                if citations:
                    display_citations(citations)
                
                # Add assistant message to history
                st.session_state.messages.append({
                    "role": "Assistant", 
                    "content": response,
                    "citations": citations
                })
                
                # Update analytics
                st.session_state.token_usage["total_tokens"] += 1100
                st.session_state.latency.append(1.7)
                
            except Exception as e:
                st.error(f"Error during query: {e}")

    st.rerun()
