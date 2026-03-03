import streamlit as st

def display_chat_message(role: str, content: str, assistant_avatar="🔬", user_avatar="👤"):
    """Displays a stylized chat message for Streamlit with high contrast colors."""
    if role == "User":
        st.markdown(f"""
            <div class="user-msg" style="color: #1E1B4B !important;">
                <b style="color: #4338CA !important;">{user_avatar} User:</b><br/>
                <span style="color: #1E1B4B !important;">{content}</span>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="assistant-msg" style="color: #0F172A !important;">
                <b style="color: #4338CA !important;">{assistant_avatar} Assistant:</b><br/>
                <span style="color: #0F172A !important;">{content}</span>
            </div>
        """, unsafe_allow_html=True)
