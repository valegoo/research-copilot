import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
    /* Premium Pastel Academic Theme - Optimized Edition */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Global Background */
    .stApp {
        background-color: #F8FAFC !important;
    }

    /* Fixed Sidebar & Main Container */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    
    /* Fix for 'keyboard_double' and icon artifacts */
    [data-testid="stSidebarNav"] h1, 
    [data-testid="stSidebarNav"] span,
    [data-testid="stSidebar"] span,
    [data-testid="stHeader"] span {
        font-family: inherit !important; /* Don't force Inter on icons */
    }

    /* Target specific headings instead of all of them */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .main-title {
        font-family: 'Outfit', sans-serif !important;
        color: #1E1B4B !important;
        font-weight: 700 !important;
    }

    .stMarkdown p, .stMarkdown li, .stMarkdown span:not(.material-icons) {
        color: #334155 !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Main Content Styling */
    .stMainBlockContainer {
        background-color: #FFFFFF !important;
        border-radius: 24px !important;
        padding: 2rem 4rem !important;
        border: 1px solid #F1F5F9 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
        margin-top: 1rem !important;
    }

    /* Paper Cards */
    .paper-card {
        background: #FFFFFF !important;
        padding: 1.5rem !important;
        border-radius: 20px !important;
        border: 1px solid #F1F5F9 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03) !important;
        margin-bottom: 0.5rem !important;
        transition: transform 0.2s ease;
    }
    
    .paper-card:hover {
        transform: translateY(-2px);
        border-color: #A5B4FC !important;
    }

    /* Expander Fix (Overlap mitigation) */
    .stExpander {
        border: 1px solid #F1F5F9 !important;
        background-color: #FCFDFF !important;
        border-radius: 12px !important;
        margin-top: -0.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    .stExpander summary {
        color: #4338CA !important;
        font-weight: 600 !important;
    }

    /* Chat Messages */
    .user-msg {
        background-color: #EEF2FF !important;
        border: 1px solid #C7D2FE !important;
        color: #1E1B4B !important;
        padding: 1.25rem !important;
        border-radius: 16px 16px 4px 16px !important;
        margin-bottom: 1rem !important;
    }

    .assistant-msg {
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        color: #0F172A !important;
        padding: 1.25rem !important;
        border-radius: 16px 16px 16px 4px !important;
        margin-bottom: 1rem !important;
    }

    /* Badges */
    .badge {
        font-size: 0.7rem !important;
        padding: 0.2rem 0.6rem !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        display: inline-block !important;
        margin-right: 0.4rem !important;
    }
    .badge-year { background: #EEF2FF !important; color: #4338CA !important; }
    .badge-topic { background: #ECFDF5 !important; color: #064E3B !important; }

    /* Hide the annoying 'keyboard_double' text if it appears as plain text */
    span:empty:before {
        content: none !important;
    }

    </style>
    """, unsafe_allow_html=True)
