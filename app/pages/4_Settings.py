import streamlit as st
import os
import sys

# Add root to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from src.rag_pipeline import RAGPipeline
from utils.styling import apply_custom_styles
from utils.session import initialize_session_state

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")
apply_custom_styles()
initialize_session_state()

# Initialize RAG Pipeline in session if not already present
if "rag_pipeline" not in st.session_state:
    try:
        st.session_state.rag_pipeline = RAGPipeline(
            persist_dir="chroma_db", 
            lecturas_dir="papers"
        )
    except Exception as e:
        st.error(f"Failed to initialize RAG Pipeline: {e}")

# Title
st.title("⚙️ System Configuration")
st.write("Manage your Research Copilot backend and AI models.")

st.markdown("---")

# API Keys
st.subheader("🔑 API Key Management")
api_key = st.text_input("OpenAI API Key", value=os.getenv("OPENAI_API_KEY", ""), type="password", help="Sign up at openai.com to get your key.")
if st.button("Save to Session Defaults"):
    os.environ["OPENAI_API_KEY"] = api_key
    st.success("API Key updated for this session!")

st.info("API keys can also be configured permanently in the .env file.")

st.markdown("---")

# Model Configuration
st.subheader("🧬 Model Selection")
model_choice = st.radio("Current Response Model", ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"], 
                       index=["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"].index(st.session_state.model_config))
st.session_state.model_config = model_choice

st.markdown("---")

# Indexing Controls
st.subheader("🏗️ Vector Store Indexing")
c1, c2 = st.columns(2)

with c1:
    is_indexed = os.path.exists("chroma_db")
    st.write(f"Status: **{'Indexed' if is_indexed else 'Not Indexed'}**")
    st.write(f"Papers in Collection: **{len(st.session_state.papers)}**")
    
    if st.button("Re-Index Document Collection 🔄"):
        if "rag_pipeline" in st.session_state:
            with st.status("Re-indexing entire collection..."):
                st.write("1. Extracting text from 21 PDFs...")
                st.write("2. Chunking content...")
                st.write("3. Generating embeddings via OpenAI...")
                st.session_state.rag_pipeline.initialize_index(force=True)
                st.write("4. Persisting to ChromaDB...")
            st.success("Indexing complete!")
        else:
            st.error("RAG Pipeline not initialized. Please check backend logs.")

with c2:
    st.write("Storage Path: `./chroma_db`")
    st.write("Distance Metric: **Cosine**")
    if st.button("Clear Vector Database 🧨"):
        import shutil
        if os.path.exists("chroma_db"):
            shutil.rmtree("chroma_db")
            st.success("Vector database cleared successfully!")
            st.rerun()
        else:
            st.warning("No database found to clear.")

st.markdown("---")

# System Reset
st.subheader("☣️ System Reset")
if st.button("Factory Reset ⚠️"):
    st.session_state.clear()
    st.rerun()

st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748B;'>Research Copilot v1.0 | Settings & Configuration</p>", unsafe_allow_html=True)
