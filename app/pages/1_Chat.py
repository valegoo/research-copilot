import streamlit as st
import time
import os
import sys

# Add root to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from src.rag_pipeline import RAGPipeline
from components.chat_message import display_chat_message
from components.citation import display_citation
from utils.styling import apply_custom_styles
from utils.session import initialize_session_state

st.set_page_config(page_title="Academic Chat", page_icon="🧬", layout="wide")
apply_custom_styles()
initialize_session_state()

# Initialize RAG Pipeline if not already in session
if "rag_pipeline" not in st.session_state:
    try:
        st.session_state.rag_pipeline = RAGPipeline(
            persist_dir="chroma_db", 
            lecturas_dir="papers"
        )
    except Exception as e:
        st.error(f"Failed to initialize RAG Pipeline: {e}")

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

# Sidebar - Settings & Filters
with st.sidebar:
    st.header("🧬 Assistant Settings")
    
    # Model selection
    st.session_state.model_config = st.selectbox(
        "Response Model", 
        ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"], 
        index=0
    )
    
    st.markdown("---")
    st.header("🔍 Search Filters")
    
    # Filter by Paper
    paper_titles = [p["title"] for p in st.session_state.papers]
    selected_papers = st.multiselect("Focus on specific papers:", options=paper_titles)
    
    # Filter by Author (Extracted from session papers)
    authors = sorted(list(set([p["author"] for p in st.session_state.papers])))
    selected_authors = st.multiselect("Filter by Author:", options=authors)
    
    # Filter by Year
    years = [p["year"] for p in st.session_state.papers]
    if years:
        min_y, max_y = min(years), max(years)
        selected_years = st.slider("Publication Range:", min_y, max_y, (min_y, max_y))
    
    st.markdown("---")
    if st.button("Clear Conversation 🧹", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Main Chat View
st.title("🧬 Academic Chat Interface")

# Display Chat History
for message in st.session_state.messages:
    display_chat_message(message["role"], message["content"])
    if "citations" in message and message["citations"]:
        with st.expander("View Citations"):
            display_citations(message["citations"])

# User Input
if prompt := st.chat_input("Ask about neoliberalism, academic capitalism, etc."):
    st.session_state.messages.append({"role": "User", "content": prompt})
    display_chat_message("User", prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Consulting academic collection..."):
            try:
                # Check for API Key
                if not os.getenv("OPENAI_API_KEY"):
                    st.warning("⚠️ OPENAI_API_KEY missing. Using demo mode.")
                    time.sleep(1)
                    response = "API Key not found. Please add your OpenAI key to the .env file to enable real analysis."
                    citations = []
                else:
                    # Execute RAG query
                    response, citations = st.session_state.rag_pipeline.query(
                        prompt,
                        strategy="Standard",
                        filter_papers=selected_papers if selected_papers else None
                    )
                
                st.markdown(response)
                if citations:
                    display_citations(citations)
                
                # Update History
                st.session_state.messages.append({
                    "role": "Assistant", 
                    "content": response,
                    "citations": citations
                })
                
                # Update statistics in session state
                if "token_usage" in st.session_state:
                    st.session_state.token_usage["total_tokens"] += 1200 # Approx increment
                    st.session_state.latency.append(1.8)
                
            except Exception as e:
                st.error(f"Error in RAG Pipeline: {e}")
    
    st.rerun()
