import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "botblocks_app"))

from botblocks_app.pages import landing, wizard, dashboard, bot_detail, admin, settings
from botblocks_app.components.ui import inject_custom_css

from dotenv import load_dotenv
load_dotenv()

# 2. Setup System Path
# This ensures Python can find your 'botblocks_app' folder
sys.path.append(os.path.join(os.path.dirname(__file__), "botblocks_app"))


st.set_page_config(
    page_title="BotBlocks - WordPress for Chatbots",

    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_custom_css()

if "current_page" not in st.session_state:
    st.session_state.current_page = "landing"

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 10px; margin-bottom: 20px;">
        <h1 style="color: #0f766e; margin: 0; font-size: 2rem;">🤖 BotBlocks</h1>
        <p style="color: #64748b; font-size: 0.875rem; margin: 5px 0;">WordPress for Chatbots</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🧭 Navigation")
    
    pages = {
        "landing": {"name": "🏠 Home", "icon": "🏠"},
        "wizard": {"name": "🧙 Create Bot", "icon": "🧙"},
        "dashboard": {"name": "📊 Dashboard", "icon": "📊"},
        "admin": {"name": "📈 Analytics", "icon": "📈"},
        "settings": {"name": "⚙️ Settings", "icon": "⚙️"}
    }
    
    for page_id, page_info in pages.items():
        is_active = st.session_state.current_page == page_id
        
        if st.button(
            page_info["name"],
            key=f"nav_{page_id}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.current_page = page_id
            if "bot_detail_tab" in st.session_state:
                del st.session_state["bot_detail_tab"]
            st.rerun()
    
    st.markdown("<br/><br/>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 💡 Quick Links")
    
    st.markdown("""
    <div style="padding: 10px; background-color: #f8fafc; border-radius: 8px; margin: 10px 0;">
        <p style="font-size: 0.875rem; color: #64748b; margin: 5px 0;">
            📚 <a href="#" style="color: #0f766e; text-decoration: none;">Documentation</a><br/>
            💬 <a href="#" style="color: #0f766e; text-decoration: none;">Support</a><br/>
            🐛 <a href="#" style="color: #0f766e; text-decoration: none;">Report Bug</a><br/>
            ⭐ <a href="#" style="color: #0f766e; text-decoration: none;">GitHub</a>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    from botblocks_app.utils import get_backend_url, is_demo_mode
    
    backend_status = "🟡 Demo Mode" if is_demo_mode() else "🟢 Connected"
    backend_url = get_backend_url()
    
    st.markdown(f"""
    <div style="padding: 10px; background-color: {'#fef3c7' if is_demo_mode() else '#ecfdf5'}; border-radius: 8px; font-size: 0.75rem;">
        <strong style="color: #1e293b;">Backend Status</strong><br/>
        <span style="color: #64748b;">{backend_status}</span><br/>
        <span style="color: #94a3b8; font-size: 0.65rem;">{backend_url}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.75rem;'>© 2024 BotBlocks</p>", unsafe_allow_html=True)

if st.session_state.current_page == "landing":
    landing.show_landing()
elif st.session_state.current_page == "wizard":
    wizard.show_wizard()
elif st.session_state.current_page == "dashboard":
    dashboard.show_dashboard()
elif st.session_state.current_page == "bot_detail":
    bot_detail.show_bot_detail()
elif st.session_state.current_page == "admin":
    admin.show_admin()
elif st.session_state.current_page == "settings":
    settings.show_settings()
else:
    landing.show_landing()
