import streamlit as st
import sys
import os
import json
import uuid

# Ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from botblocks_app.components.ui import render_chat_bubble, render_code_snippet, inject_custom_css
from botblocks_app.services import api  # Import the real service
from botblocks_app.utils import format_datetime, get_backend_url

def show_bot_detail():
    inject_custom_css()
    
    # 1. Get Bot from Session
    bot = st.session_state.get('selected_bot')
    
    if not bot:
        st.warning("⚠️ No bot selected")
        if st.button("← Back to Dashboard"):
            st.session_state.current_page = "dashboard"
            st.rerun()
        return
    
    public_id = bot.get('public_id')
    
    # Header Section
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title(f"🤖 {bot.get('name', 'Bot Details')}")
        st.markdown(f"**ID:** `{public_id}`")
    with col2:
        if st.button("← Dashboard", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Overview", "💬 Test Chat", "🔗 Embed Widget", "⚙️ Configuration"])
    
    with tab1:
        show_overview_tab(bot)
    
    with tab2:
        show_chat_tab(bot)
    
    with tab3:
        show_embed_tab(bot)
    
    with tab4:
        show_configuration_tab(bot)

def show_overview_tab(bot: dict):
    st.markdown("### 📊 Bot Information")
    
    status = "active" # Hardcoded for MVP
    status_color = "#10b981"
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
            <strong style="color: #64748b; font-size: 0.875rem;">Status</strong>
            <div style="margin-top: 10px;">
                <span style="background-color: {status_color}; color: white; padding: 6px 14px; border-radius: 16px; font-size: 0.875rem; font-weight: 500;">
                    {status.title()}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
            <strong style="color: #64748b; font-size: 0.875rem;">Platform</strong>
            <div style="margin-top: 10px; font-size: 1.25rem; color: #1e293b;">
                🌐 {bot.get('platform', 'website').title()}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Description Card
    desc = bot.get('description') or bot.get('system_prompt', 'No description')
    
    st.markdown(f"""
    <div style="background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 20px;">
        <h4 style="color: #1e293b; margin-bottom: 15px;">Details</h4>
        <p style="color: #64748b; margin: 8px 0;"><strong>System Prompt:</strong> {desc[:100]}...</p>
        <p style="color: #64748b; margin: 8px 0;"><strong>Created:</strong> {format_datetime(bot.get('created_at'))}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mock Actions
    st.markdown("### 🛠️ Actions")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Re-index Knowledge", use_container_width=True):
             st.toast("✅ Knowledge is up to date!")
    with col2:
        st.button("📥 Export Config", use_container_width=True, disabled=True)
    with col3:
        if st.button("🗑️ Delete Bot", use_container_width=True):
            st.error("Delete disabled in demo mode.")

def show_chat_tab(bot: dict):
    st.markdown("### 💬 Test Your Bot")
    st.markdown("Chat with your bot to test its responses and knowledge")
    
    # Session State for Chat
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Chat Container
    st.markdown("""
    <div style="background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); max-height: 500px; overflow-y: auto; margin-bottom: 20px;">
    """, unsafe_allow_html=True)
    
    if not st.session_state.chat_messages:
        st.markdown("""
        <div style="text-align: center; padding: 40px; color: #94a3b8;">
            <div style="font-size: 3rem; margin-bottom: 10px;">💬</div>
            <p>No messages yet. Start a conversation!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_messages:
            render_chat_bubble(
                msg["content"],
                is_user=msg["role"] == "user"
            )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Input Area
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("Type your message", key="chat_input", placeholder="Ask me anything...")
    with col2:
        send_button = st.button("Send", type="primary", use_container_width=True)
    
    # Send Logic
    if send_button and user_input:
        # 1. Add User Message
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        
        try:
            with st.spinner("🤔 Thinking..."):
                # 2. CALL REAL BACKEND
                response_text = api.chat_with_bot(bot.get('public_id'), user_input)
                
                # 3. Add Bot Message
                st.session_state.chat_messages.append({
                    "role": "assistant", 
                    "content": response_text
                })
                st.rerun()
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            
    # Utilities
    if st.session_state.chat_messages:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_messages = []
            st.rerun()

def show_embed_tab(bot: dict):
    st.markdown("### 🔗 Embed Your Bot")
    st.markdown("Copy this code to embed the chat widget on your website")
    
    public_id = bot.get("public_id")
    # Point to the Static file we created in backend/static/widget.js
    backend_url = "http://localhost:8000" 
    
    # The "One-Line" Script Tag (The SaaS Magic)
    embed_html = f"""<script 
    src="{backend_url}/static/widget.js" 
    data-bot-id="{public_id}" 
    defer>
</script>"""
    
    render_code_snippet(embed_html, language="html", title="HTML Embed Code")
    
    st.markdown("<br/>", unsafe_allow_html=True)
    st.info("💡 **Quick Setup:** Copy the HTML code above and paste it into your website's `<body>` tag.")
    
    with st.expander("📖 Developer API"):
        st.markdown(f"""
        **API Endpoint:**
        - POST `{backend_url}/api/v1/chat/web`
        - Body: `{{"bot_id": "{public_id}", "message": "your message"}}`
        """)

def show_configuration_tab(bot: dict):
    st.markdown("### ⚙️ Bot Configuration")
    
    st.markdown(f"""
    <div style="background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 20px;">
        <h4 style="color: #1e293b; margin-bottom: 15px;">System Prompt</h4>
        <div style="background-color: #f8fafc; padding: 15px; border-radius: 8px; border-left: 4px solid #0f766e;">
            <code style="color: #475569; font-size: 0.875rem; white-space: pre-wrap;">
{bot.get('system_prompt', 'No system prompt configured')}
            </code>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔧 Update Persona")
    st.text_area("Update System Prompt", value=bot.get('system_prompt', ''), height=100)
    
    if st.button("💾 Update Prompt", type="primary"):
        st.toast("✅ Prompt updated locally (Demo Mode)")