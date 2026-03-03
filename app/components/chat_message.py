import streamlit as st

def display_chat_message(role: str, content: str, assistant_avatar="🔬", user_avatar="👤"):
    """Displays a stylized chat message for Streamlit."""
    if role == "User":
        st.markdown(f"""
            <div class="user-msg">
                <b>{user_avatar} User:</b> {content}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="assistant-msg">
                <b>{assistant_avatar} Assistant:</b> {content}
            </div>
        """, unsafe_allow_html=True)
