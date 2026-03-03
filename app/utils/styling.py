import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
    /* Premium Pastel Academic Theme */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    :root {
        --primary: #A5B4FC;
        --secondary: #FDE68A;
        --accent: #FDA4AF;
        --bg-soft: #F8FAFC;
        --text-main: #1E293B;
        --text-sub: #64748B;
        --glass-bg: rgba(255, 255, 255, 0.8);
        --glass-border: rgba(255, 255, 255, 0.4);
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: var(--text-main);
        background-color: var(--bg-soft);
    }
    
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        color: #0F172A;
    }

    /* Soft Pastel Container */
    .stMainBlockContainer {
        padding: 3rem 6rem;
        background: linear-gradient(135deg, #F0F4FF 0%, #FAF5FF 100%);
        backdrop-filter: blur(10px);
        border-radius: 40px;
        border: 1px solid var(--glass-border);
        box-shadow: 0 15px 35px -10px rgba(165, 180, 252, 0.2);
        margin: 2rem;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }

    /* Chat Messages - User */
    .user-msg {
        background: linear-gradient(135deg, #A5B4FC 0%, #C7D2FE 100%);
        color: #1E293B;
        padding: 1.25rem 1.75rem;
        border-radius: 24px 24px 4px 24px;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 20px -8px rgba(165, 180, 252, 0.4);
        width: fit-content;
        max-width: 85%;
        margin-left: auto;
        font-weight: 500;
    }

    /* Chat Messages - Assistant */
    .assistant-msg {
        background: #FFFFFF;
        color: #334155;
        padding: 1.25rem 1.75rem;
        border-radius: 24px 24px 24px 4px;
        margin-bottom: 1.5rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 8px 20px -10px rgba(0, 0, 0, 0.05);
        width: fit-content;
        max-width: 85%;
    }

    /* Paper Cards */
    .paper-card {
        background: #FFFFFF;
        padding: 2rem;
        border-radius: 28px;
        border: 1px solid #F1F5F9;
        transition: all 0.4s ease;
        box-shadow: 0 4px 12px -4px rgba(0, 0, 0, 0.05);
    }
    
    .paper-card:hover {
        transform: translateY(-6px);
        background: #FDFCFD;
        border-color: #E0E7FF;
        box-shadow: 0 12px 24px -12px rgba(165, 180, 252, 0.3);
    }

    /* Badges */
    .badge {
        font-size: 0.7rem;
        padding: 0.35rem 0.85rem;
        border-radius: 100px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        margin-right: 0.5rem;
    }

    .badge-year { background: #E0E7FF; color: #4338CA; border: 1px solid #C7D2FE; }
    .badge-topic { background: #DCFCE7; color: #166534; border: 1px solid #BBF7D0; }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #E2E8F0; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #A5B4FC; }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stChatFloatingInputContainer { animation: fadeIn 0.6s cubic-bezier(0.23, 1, 0.32, 1); }

    </style>
    """, unsafe_allow_html=True)
