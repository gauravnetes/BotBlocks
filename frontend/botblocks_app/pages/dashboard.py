import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from botblocks_app.components.ui import render_card, render_platform_badge, inject_custom_css
from botblocks_app.utils import api_get, api_post_json, format_datetime, is_demo_mode

def show_dashboard():
    inject_custom_css()
    
    st.title("📊 Dashboard")
    st.markdown("Manage all your chatbots from one place")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("")
    with col2:
        if st.button("➕ Create New Bot", type="primary", use_container_width=True):
            st.session_state.current_page = "wizard"
            st.rerun()
    with col3:
        if st.button("🔄 Refresh", use_container_width=True):
            if "bots_cache" in st.session_state:
                del st.session_state["bots_cache"]
            st.rerun()
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    try:
        with st.spinner("Loading your bots..."):
            response = api_get("/bots")
            bots = response.get("bots", [])
            
            if is_demo_mode():
                st.info("ℹ️ Running in demo mode. Your bots are stored locally and will be lost when you refresh.")
            
            if not bots:
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
                return
            
            st.markdown(f"**Total Bots:** {len(bots)}")
            st.markdown("<br/>", unsafe_allow_html=True)
            
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

def render_bot_card(bot: dict):
    public_id = bot.get("public_id", "")
    name = bot.get("name", "Untitled Bot")
    description = bot.get("description", "No description")
    status = bot.get("status", "active")
    platform = bot.get("platform", "website")
    last_indexed = bot.get("last_indexed")
    created_at = bot.get("created_at")
    documents_count = bot.get("documents_count", 0)
    
    status_colors = {
        "active": "#10b981",
        "inactive": "#6b7280",
        "indexing": "#f59e0b",
        "error": "#ef4444"
    }
    
    status_color = status_colors.get(status, "#6b7280")
    
    st.markdown(f"""
    <div style="background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 20px; transition: transform 0.2s ease, box-shadow 0.2s ease;">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;">
            <h3 style="color: #1e293b; margin: 0;">{name}</h3>
            <span style="background-color: {status_color}; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 500;">{status}</span>
        </div>
        <p style="color: #64748b; font-size: 0.875rem; margin-bottom: 15px;">{description}</p>
        <div style="margin-bottom: 10px;">
            <span style="background-color: #e0f2fe; color: #0369a1; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 500; margin-right: 5px;">
                🌐 {platform.title()}
            </span>
            {f'<span style="background-color: #fef3c7; color: #92400e; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 500;">📚 {documents_count} docs</span>' if documents_count > 0 else ''}
        </div>
        <p style="color: #94a3b8; font-size: 0.75rem; margin-top: 10px;">
            Created: {format_datetime(created_at)}<br/>
            Last indexed: {format_datetime(last_indexed)}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👁️ View", key=f"view_{public_id}", use_container_width=True):
            st.session_state.current_page = "bot_detail"
            st.session_state.selected_bot_id = public_id
            st.rerun()
    
    with col2:
        if st.button("💬 Test", key=f"test_{public_id}", use_container_width=True):
            st.session_state.current_page = "bot_detail"
            st.session_state.selected_bot_id = public_id
            st.session_state.bot_detail_tab = "chat"
            st.rerun()
    
    with col3:
        if st.button("🔄 Re-index", key=f"reindex_{public_id}", use_container_width=True):
            try:
                api_post_json(f"/bots/{public_id}/index", {})
                st.success("✅ Indexing started!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
