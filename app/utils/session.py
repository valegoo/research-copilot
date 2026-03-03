import streamlit as st
import os
import re

def initialize_session_state():
    """Initializes all required session variables."""
    # Chat History (matching user example naming)
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Paper Database
    if "papers" not in st.session_state:
        # Load papers from filesystem
        lecturas_path = "Lecturas"
        try:
            pdf_files = [f for f in os.listdir(lecturas_path) if f.lower().endswith('.pdf')]
            st.session_state.papers = []
            for i, filename in enumerate(pdf_files):
                # Simple parsing of title/author from filename if possible, otherwise use filename
                # Example: "A brief history of neoliberalism (2007).pdf"
                year_match = 2024 # Default
                try:
                    import re
                    years = re.findall(r'\((\d{4})\)', filename)
                    if years:
                        year_match = int(years[-1])
                except:
                    pass
                
                st.session_state.papers.append({
                    "id": f"{i:03d}",
                    "title": filename.replace(".pdf", ""),
                    "author": "Academic Author", # Could be extracted from metadata if we load it here too
                    "year": year_match,
                    "topic": "General Research",
                    "abstract": f"Complete text indexed in the vector store from {filename}."
                })
        except Exception as e:
            st.error(f"Error loading papers: {e}")
            st.session_state.papers = []
    
    # Token Tracker
    if "token_usage" not in st.session_state:
        st.session_state.token_usage = {"total_tokens": 0, "prompt_tokens": 0, "completion_tokens": 0}
    
    if "latency" not in st.session_state:
        st.session_state.latency = [1.2, 1.5, 0.8, 2.1] # Initial seeds
    
    # UI Filters
    if "filters" not in st.session_state:
        st.session_state.filters = {
            "search": "",
            "topic": "All",
            "year": (1980, 2026),
            "author": "All"
        }
    
    # Model Config
    if "model_config" not in st.session_state:
        st.session_state.model_config = "gpt-4o"
