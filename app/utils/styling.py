import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
    /* Professional Academic Theme - Premium Edition */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@300;400;600&display=swap');
    
    :root {
        --primary: hsl(245, 82%, 67%);
        --primary-hover: hsl(245, 82%, 75%);
        --bg-glass: rgba(15, 23, 42, 0.7);
        --border-glass: rgba(255, 255, 255, 0.1);
        --text-main: #E2E8F0;
        --text-sub: #94A3B8;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: var(--text-main);
    }
    
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
    }

    /* Premium Glassmorphism Container */
    .stMainBlockContainer {
        padding: 3rem 6rem;
        background: radial-gradient(circle at top left, rgba(99, 102, 241, 0.05), transparent), 
                    var(--bg-glass);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 32px;
        border: 1px solid var(--border-glass);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        margin: 2rem;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.95);
        border-right: 1px solid var(--border-glass);
    }

    /* Chat Messages - User */
    .user-msg {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        color: white;
        padding: 1.25rem 1.75rem;
        border-radius: 24px 24px 4px 24px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.3);
        width: fit-content;
        max-width: 85%;
        margin-left: auto;
        font-size: 1.05rem;
        line-height: 1.5;
    }

    /* Chat Messages - Assistant */
    .assistant-msg {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(5px);
        color: #F8FAFC;
        padding: 1.25rem 1.75rem;
        border-radius: 24px 24px 24px 4px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.3);
        width: fit-content;
        max-width: 85%;
        font-size: 1.05rem;
        line-height: 1.6;
    }

    /* Paper Cards */
    .paper-card {
        background: rgba(255, 255, 255, 0.03);
        padding: 2rem;
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        backdrop-filter: blur(10px);
    }
    
    .paper-card:hover {
        transform: translateY(-8px) scale(1.02);
        background: rgba(255, 255, 255, 0.06);
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.4);
    }

    /* Badges */
    .badge {
        font-size: 0.7rem;
        padding: 0.3rem 0.8rem;
        border-radius: 100px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-right: 0.5rem;
    }

    .badge-year { background: rgba(99, 102, 241, 0.15); color: #818CF8; border: 1px solid rgba(99, 102, 241, 0.2); }
    .badge-topic { background: rgba(34, 197, 94, 0.15); color: #4ADE80; border: 1px solid rgba(34, 197, 94, 0.2); }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: rgba(15, 23, 42, 0.1); }
    ::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.1); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(99, 102, 241, 0.3); }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stChatFloatingInputContainer { animation: fadeIn 0.5s ease; }

    </style>
    """, unsafe_allow_html=True)
