import streamlit as st
import sys
import os

# Ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from botblocks_app.components.ui import inject_custom_css, render_code_snippet
from botblocks_app.services import api  # Import the real service
from botblocks_app.utils import format_datetime, is_demo_mode

def show_dashboard():
    inject_custom_css()
    
    # --- Custom Modal Logic (Fallback for older Streamlit) ---
    if st.session_state.get("show_config_modal"):
        bot = st.session_state.get("config_bot_data")
        if bot:
            render_config_modal(bot)
            # Add a spacer to separate modal from dashboard
            st.markdown("<br/>", unsafe_allow_html=True)
            st.markdown("---")

    st.title("📊 Dashboard")
    st.markdown("Manage all your chatbots from one place")
    
    # --- Top Action Bar ---
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.write("") # Spacer
    with col2:
        if st.button("➕ Create New Bot", type="primary", use_container_width=True):
            st.session_state.current_page = "wizard"
            st.rerun()
    with col3:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # --- Fetch Real Data ---
    try:
        with st.spinner("Loading your bots..."):
            bots = api.get_all_bots()
            
            # Empty State
            if not bots:
                render_empty_state()
                return
            
            st.markdown(f"**Total Bots:** {len(bots)}")
            st.markdown("<br/>", unsafe_allow_html=True)
            
            # Grid Layout (2 columns)
            cols_per_row = 2
            for idx in range(0, len(bots), cols_per_row):
                cols = st.columns(cols_per_row)
                for col_idx, col in enumerate(cols):
                    bot_idx = idx + col_idx
                    if bot_idx < len(bots):
                        with col:
                            render_bot_card(bots[bot_idx])
    
    except Exception as e:
        st.error(f"❌ Error loading bots: {str(e)}")
        if is_demo_mode():
            st.info("ℹ️ No backend connection. Running in demo mode.")

def render_config_modal(bot):
    """
    Renders a 'modal-like' section at the top of the page.
    """
    st.markdown("""
    <div class="glass-panel" style="border: 1px solid var(--accent); padding: 20px; background-color: var(--zinc-900);">
        <h3 style="color: var(--accent); margin-top: 0;">🔌 Embed Configuration</h3>
        <p>Use the code below to add this chatbot to your website.</p>
    </div>
    """, unsafe_allow_html=True)
    
    public_id = bot.get("public_id")
    backend_url = "http://localhost:8000"
    
    embed_code = f"""<script
    src="{backend_url}/static/widget.js"
    data-bot-id="{public_id}"
    defer>
</script>"""

    render_code_snippet(embed_code, language="html")
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("❌ Close Panel", type="secondary"):
            del st.session_state["show_config_modal"]
            del st.session_state["config_bot_data"]
            st.rerun()
    with col2:
        st.info("The widget will appear in the bottom-right corner of your site.")

def render_empty_state():
    st.markdown("""
    <div class="glass-panel" style="text-align: center; padding: 60px 20px;">
        <div style="font-size: 4rem; margin-bottom: 20px;">🤖</div>
        <h2 style="margin-bottom: 10px;">No Bots Yet</h2>
        <p style="margin-bottom: 30px;">Create your first chatbot to get started!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Create Your First Bot", type="primary", use_container_width=True):
            st.session_state.current_page = "wizard"
            st.rerun()

def render_bot_card(bot: dict):
    # Safely get data (handling missing fields from our simple backend)
    public_id = bot.get("public_id", "")
    name = bot.get("name", "Untitled Bot")
    # Our backend uses 'system_prompt' but UI expects 'description'
    description = bot.get("description") or bot.get("system_prompt", "No description provided.")[:100] + "..."
    platform = bot.get("platform", "web")
    created_at = bot.get("created_at")
    
    # Mock fields for UI polish (since backend doesn't calculate these yet)
    status = "active" 
    
    # Status Colors
    status_color = "var(--accent)" if status == "active" else "var(--zinc-500)"
    
    # Render HTML Card
    st.markdown(f"""
    <div class="glass-panel" style="padding: 20px; margin-bottom: 20px; height: 100%;">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;">
            <h3 style="margin: 0; font-size: 1.2rem;">{name}</h3>
            <span style="background-color: {status_color}; color: var(--zinc-950); padding: 2px 8px; border-radius: 2px; font-size: 0.7rem; font-weight: bold;">{status.upper()}</span>
        </div>
        <p style="font-size: 0.85rem; margin-bottom: 15px; height: 40px; overflow: hidden;">{description}</p>
        <div style="margin-bottom: 15px;">
            <span style="background-color: var(--zinc-800); color: var(--text-primary); padding: 4px 10px; border-radius: 2px; font-size: 0.75rem; font-weight: 500; margin-right: 5px; border: 1px solid var(--border-color);">
                🌐 {platform.upper()}
            </span>
        </div>
        <p style="color: var(--text-muted); font-size: 0.7rem; margin-top: 10px;">
            ID: <code style="color: var(--accent); background: transparent;">{public_id[:8]}...</code>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Card Actions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💬 Chat", key=f"chat_{public_id}", use_container_width=True):
            st.session_state.current_page = "bot_detail"
            st.session_state.selected_bot = bot # Store the WHOLE bot object
            st.rerun()
    
    with col2:
        if st.button("⚙️ Config", key=f"conf_{public_id}", use_container_width=True):
            # Set session state to show the modal
            st.session_state["show_config_modal"] = True
            st.session_state["config_bot_data"] = bot
            st.rerun()
    
    with col3:
        if st.button("🗑️ Delete", key=f"del_{public_id}", type="secondary", use_container_width=True):
            if api.delete_bot(public_id):
                st.toast(f"✅ Bot '{name}' deleted successfully!")
                # Small delay to let toast show, then rerun
                import time
                time.sleep(1) 
                st.rerun()
            else:
                st.error("Failed to delete bot.")
