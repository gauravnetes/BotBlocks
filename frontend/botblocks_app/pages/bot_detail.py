import streamlit as st
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from botblocks_app.components.ui import render_chat_bubble, render_code_snippet, inject_custom_css, render_platform_badge
from botblocks_app.utils import api_get, api_post_json, format_datetime, is_demo_mode

def show_bot_detail():
    inject_custom_css()
    
    if "selected_bot_id" not in st.session_state:
        st.warning("⚠️ No bot selected")
        if st.button("← Back to Dashboard"):
            st.session_state.current_page = "dashboard"
            st.rerun()
        return
    
    public_id = st.session_state.selected_bot_id
    
    try:
        with st.spinner("Loading bot details..."):
            response = api_get(f"/bots/{public_id}")
            bot = response.get("bot", {})
        
        if not bot:
            st.error("❌ Bot not found")
            if st.button("← Back to Dashboard"):
                st.session_state.current_page = "dashboard"
                st.rerun()
            return
        
        col1, col2 = st.columns([4, 1])
        with col1:
            st.title(f"🤖 {bot.get('name', 'Bot Details')}")
            st.markdown(f"**ID:** `{public_id}`")
        with col2:
            if st.button("← Dashboard", use_container_width=True):
                st.session_state.current_page = "dashboard"
                st.rerun()
        
        st.markdown("<br/>", unsafe_allow_html=True)
        
        default_tab = st.session_state.get("bot_detail_tab", "overview")
        tab_index = 0
        if default_tab == "chat":
            tab_index = 1
        elif default_tab == "embed":
            tab_index = 2
        elif default_tab == "config":
            tab_index = 3
        
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Overview", "💬 Test Chat", "🔗 Embed Widget", "⚙️ Configuration"])
        
        with tab1:
            show_overview_tab(bot)
        
        with tab2:
            show_chat_tab(bot)
        
        with tab3:
            show_embed_tab(bot)
        
        with tab4:
            show_configuration_tab(bot)
    
    except Exception as e:
        st.error(f"❌ Error loading bot: {str(e)}")

def show_overview_tab(bot: dict):
    st.markdown("### 📊 Bot Information")
    
    status_colors = {
        "active": "#10b981",
        "inactive": "#6b7280",
        "indexing": "#f59e0b",
        "error": "#ef4444"
    }
    
    status = bot.get("status", "active")
    status_color = status_colors.get(status, "#6b7280")
    
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
    
    st.markdown(f"""
    <div style="background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 20px;">
        <h4 style="color: #1e293b; margin-bottom: 15px;">Details</h4>
        <p style="color: #64748b; margin: 8px 0;"><strong>Description:</strong> {bot.get('description', 'No description')}</p>
        <p style="color: #64748b; margin: 8px 0;"><strong>Created:</strong> {format_datetime(bot.get('created_at'))}</p>
        <p style="color: #64748b; margin: 8px 0;"><strong>Last Indexed:</strong> {format_datetime(bot.get('last_indexed'))}</p>
        <p style="color: #64748b; margin: 8px 0;"><strong>Documents:</strong> {bot.get('documents_count', 0)} uploaded</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🛠️ Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Re-index Knowledge", use_container_width=True):
            try:
                with st.spinner("Indexing..."):
                    response = api_post_json(f"/bots/{bot.get('public_id')}/index", {})
                    st.success("✅ Indexing completed!")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    with col2:
        if st.button("📥 Export Config", use_container_width=True):
            config = {
                "name": bot.get("name"),
                "description": bot.get("description"),
                "platform": bot.get("platform"),
                "system_prompt": bot.get("system_prompt"),
                "status": bot.get("status")
            }
            config_json = json.dumps(config, indent=2)
            st.download_button(
                "💾 Download JSON",
                data=config_json,
                file_name=f"{bot.get('name', 'bot')}_config.json",
                mime="application/json"
            )
    
    with col3:
        if st.button("🗑️ Delete Bot", use_container_width=True):
            st.warning("⚠️ Delete functionality coming soon")

def show_chat_tab(bot: dict):
    st.markdown("### 💬 Test Your Bot")
    st.markdown("Chat with your bot to test its responses and knowledge")
    
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    if "chat_session_id" not in st.session_state:
        import uuid
        st.session_state.chat_session_id = str(uuid.uuid4())
    
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
                is_user=msg["role"] == "user",
                sources=msg.get("sources")
            )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "Type your message",
            key="chat_input",
            placeholder="Ask me anything..."
        )
    
    with col2:
        send_button = st.button("Send", type="primary", use_container_width=True)
    
    if send_button and user_input:
        st.session_state.chat_messages.append({
            "role": "user",
            "content": user_input
        })
        
        try:
            with st.spinner("🤔 Thinking..."):
                response = api_post_json(f"/bots/{bot.get('public_id')}/chat", {
                    "user_input": user_input,
                    "session_id": st.session_state.chat_session_id
                })
                
                reply = response.get("reply", "No response")
                sources = response.get("sources", [])
                
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": reply,
                    "sources": sources
                })
                
                st.rerun()
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    if st.session_state.chat_messages:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chat_messages = []
                st.rerun()
        
        with col2:
            if st.button("📋 Copy Last Response", use_container_width=True):
                last_bot_msg = next(
                    (msg for msg in reversed(st.session_state.chat_messages) if msg["role"] == "assistant"),
                    None
                )
                if last_bot_msg:
                    st.success("✅ Response copied!")
                    st.code(last_bot_msg["content"])

def show_embed_tab(bot: dict):
    st.markdown("### 🔗 Embed Your Bot")
    st.markdown("Copy this code to embed the chat widget on your website")
    
    public_id = bot.get("public_id")
    bot_name = bot.get("name", "Bot")
    
    backend_url = os.getenv("BOTBLOCKS_BACKEND", "http://localhost:8000")
    
    embed_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{bot_name} - Chat Widget</title>
    <style>
        #botblocks-chat-widget {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 350px;
            height: 500px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            background: white;
            display: flex;
            flex-direction: column;
            z-index: 1000;
        }}
        #botblocks-chat-header {{
            background: linear-gradient(135deg, #0f766e 0%, #14b8a6 100%);
            color: white;
            padding: 15px;
            border-radius: 12px 12px 0 0;
            font-weight: bold;
        }}
        #botblocks-chat-messages {{
            flex: 1;
            overflow-y: auto;
            padding: 15px;
        }}
        #botblocks-chat-input {{
            border-top: 1px solid #e2e8f0;
            padding: 15px;
            display: flex;
            gap: 10px;
        }}
        #botblocks-chat-input input {{
            flex: 1;
            padding: 10px;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
        }}
        #botblocks-chat-input button {{
            padding: 10px 20px;
            background: #0f766e;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }}
        .message {{
            margin: 10px 0;
            padding: 10px;
            border-radius: 8px;
            max-width: 80%;
        }}
        .user-message {{
            background: #0f766e;
            color: white;
            margin-left: auto;
        }}
        .bot-message {{
            background: #f1f5f9;
            color: #1e293b;
        }}
    </style>
</head>
<body>
    <div id="botblocks-chat-widget">
        <div id="botblocks-chat-header">{bot_name}</div>
        <div id="botblocks-chat-messages"></div>
        <div id="botblocks-chat-input">
            <input type="text" id="message-input" placeholder="Type a message...">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        const BOT_ID = '{public_id}';
        const API_URL = '{backend_url}/api/v1';
        
        async function sendMessage() {{
            const input = document.getElementById('message-input');
            const message = input.value.trim();
            if (!message) return;
            
            addMessage(message, 'user');
            input.value = '';
            
            try {{
                const response = await fetch(`${{API_URL}}/bots/${{BOT_ID}}/chat`, {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ user_input: message }})
                }});
                
                const data = await response.json();
                addMessage(data.reply || 'No response', 'bot');
            }} catch (error) {{
                addMessage('Error: Could not connect to bot', 'bot');
            }}
        }}
        
        function addMessage(text, sender) {{
            const messagesDiv = document.getElementById('botblocks-chat-messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${{sender}}-message`;
            messageDiv.textContent = text;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }}
        
        document.getElementById('message-input').addEventListener('keypress', (e) => {{
            if (e.key === 'Enter') sendMessage();
        }});
    </script>
</body>
</html>"""
    
    render_code_snippet(embed_html, language="html", title="Complete HTML Widget")
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    javascript_snippet = f"""<script>
// Minimal JavaScript snippet
const botId = '{public_id}';
const apiUrl = '{backend_url}/api/v1';

async function chatWithBot(message) {{
    const response = await fetch(`${{apiUrl}}/bots/${{botId}}/chat`, {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{ user_input: message }})
    }});
    return await response.json();
}}
</script>"""
    
    render_code_snippet(javascript_snippet, language="html", title="JavaScript API Snippet")
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    st.info("💡 **Quick Setup:** Copy the HTML code above and paste it into your website, or use the JavaScript snippet to integrate with your existing chat interface.")
    
    with st.expander("📖 Integration Instructions"):
        st.markdown("""
        **For Complete Widget:**
        1. Copy the full HTML code above
        2. Save it as `chatbot.html` on your server
        3. Include it in your website via iframe or direct embedding
        
        **For Custom Integration:**
        1. Copy the JavaScript snippet
        2. Add it to your website's `<head>` or before `</body>`
        3. Call `chatWithBot(message)` to interact with your bot
        4. Handle the response in your own UI
        
        **API Endpoint:**
        - POST `{backend_url}/api/v1/bots/{public_id}/chat`
        - Body: `{{"user_input": "your message"}}`
        - Returns: `{{"reply": "bot response", "sources": [...]}}`
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
    
    new_prompt = st.text_area(
        "Update System Prompt",
        value=bot.get('system_prompt', ''),
        height=150,
        help="Modify how your bot behaves and responds"
    )
    
    if st.button("💾 Update Prompt", type="primary"):
        try:
            with st.spinner("Updating..."):
                api_post_json(f"/bots/{bot.get('public_id')}/persona", {
                    "system_prompt": new_prompt
                })
                st.success("✅ Prompt updated successfully!")
                st.rerun()
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    st.markdown("### 📊 Bot Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #0f766e 0%, #14b8a6 100%); color: white; padding: 20px; border-radius: 12px;">
            <div style="font-size: 0.875rem; opacity: 0.9; margin-bottom: 5px;">Documents</div>
            <div style="font-size: 2rem; font-weight: bold;">""" + str(bot.get('documents_count', 0)) + """</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%); color: white; padding: 20px; border-radius: 12px;">
            <div style="font-size: 0.875rem; opacity: 0.9; margin-bottom: 5px;">Platform</div>
            <div style="font-size: 1.5rem; font-weight: bold;">🌐 """ + bot.get('platform', 'website').title() + """</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #dc2626 0%, #f87171 100%); color: white; padding: 20px; border-radius: 12px;">
            <div style="font-size: 0.875rem; opacity: 0.9; margin-bottom: 5px;">Status</div>
            <div style="font-size: 1.5rem; font-weight: bold;">""" + bot.get('status', 'active').title() + """</div>
        </div>
        """, unsafe_allow_html=True)
