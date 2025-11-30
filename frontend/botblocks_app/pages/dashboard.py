import streamlit as st
import sys
import os

# Ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from botblocks_app.components.ui import inject_custom_css
from botblocks_app.services import api  # Import the real service
from botblocks_app.utils import format_datetime, is_demo_mode

def show_dashboard():
    inject_custom_css()
    
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

def render_empty_state():
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px; background-color: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
        <div style="font-size: 4rem; margin-bottom: 20px;">🤖</div>
        <h2 style="color: #1e293b; margin-bottom: 10px;">No Bots Yet</h2>
        <p style="color: #64748b; margin-bottom: 30px;">Create your first chatbot to get started!</p>
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
    documents_count = 1 if "RAG" in description else 0 
    
    # Status Colors
    status_colors = {
        "active": "#10b981",
        "inactive": "#6b7280"
    }
    status_color = status_colors.get(status, "#10b981")
    
    # Render HTML Card
    st.markdown(f"""
    <div style="background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 20px; height: 100%;">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;">
            <h3 style="color: #1e293b; margin: 0; font-size: 1.2rem;">{name}</h3>
            <span style="background-color: {status_color}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem;">{status.upper()}</span>
        </div>
        <p style="color: #64748b; font-size: 0.85rem; margin-bottom: 15px; height: 40px; overflow: hidden;">{description}</p>
        <div style="margin-bottom: 15px;">
            <span style="background-color: #e0f2fe; color: #0369a1; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 500; margin-right: 5px;">
                🌐 {platform.upper()}
            </span>
        </div>
        <p style="color: #94a3b8; font-size: 0.7rem; margin-top: 10px;">
            ID: <code style="color: #64748b">{public_id[:8]}...</code>
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
        # For Hackathon, we disable Config
        st.button("⚙️ Config", key=f"conf_{public_id}", disabled=True, use_container_width=True)
    
    with col3:
        # Re-index is a mock action for now
        if st.button("🔄 Re-index", key=f"idx_{public_id}", use_container_width=True):
            st.toast("✅ Re-indexing started (Mock)")