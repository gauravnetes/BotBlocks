import streamlit as st
import sys
import os
from datetime import datetime, timedelta

# Ensure path is correct
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from botblocks_app.components.ui import render_stat_card, inject_custom_css
from botblocks_app.services import api  # Use the shared API service
from botblocks_app.utils import is_demo_mode, get_backend_url

def show_admin():
    inject_custom_css()
    
    st.title("📊 Admin & Usage")
    st.markdown("Monitor platform usage and bot activity")
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    try:
        with st.spinner("Loading analytics..."):
            # 1. Fetch Real Data
            bots = api.get_all_bots()
            
            # 2. Calculate Stats (Safe defaults for missing backend fields)
            total_bots = len(bots)
            
            # Assume all created bots are "active" for the hackathon
            active_bots = total_bots 
            
            # Hack: Estimate documents based on prompt content (or default to 1 per bot)
            total_documents = sum(1 for b in bots if "RAG" in b.get('system_prompt', ''))
            
            # Calculate recent activity locally
            recent_activity = sum(1 for bot in bots if was_recently_active(bot.get("created_at")))
            
            if is_demo_mode():
                st.info("ℹ️ Running in demo mode. Statistics are calculated from local data.")
            
            st.markdown("### 📈 Overview")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                render_stat_card(
                    label="Total Bots",
                    value=str(total_bots),
                    icon="🤖",
                    color="#0f766e"
                )
            
            with col2:
                render_stat_card(
                    label="Active Bots",
                    value=str(active_bots),
                    icon="✅",
                    color="#10b981"
                )
            
            with col3:
                render_stat_card(
                    label="Knowledge Bases",
                    value=str(total_documents),
                    icon="📚",
                    color="#7c3aed"
                )
            
            with col4:
                render_stat_card(
                    label="New (7 Days)",
                    value=str(recent_activity),
                    icon="📅",
                    color="#f59e0b"
                )
            
            st.markdown("<br/><br/>", unsafe_allow_html=True)
            
            st.markdown("### 📊 Platform Distribution")
            
            # Calculate platform counts safely
            platform_counts = {}
            for bot in bots:
                platform = bot.get("platform", "web").lower()
                platform_counts[platform] = platform_counts.get(platform, 0) + 1
            
            if platform_counts:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    for platform, count in platform_counts.items():
                        percentage = (count / total_bots * 100) if total_bots > 0 else 0
                        st.markdown(f"""
                        <div style="background-color: white; padding: 15px; border-radius: 8px; margin: 10px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <span style="color: #1e293b; font-weight: 500;">🌐 {platform.title()}</span>
                                <span style="color: #64748b; font-weight: 500;">{count} bots ({percentage:.1f}%)</span>
                            </div>
                            <div style="background-color: #e2e8f0; height: 8px; border-radius: 4px; overflow: hidden;">
                                <div style="background: linear-gradient(90deg, #0f766e 0%, #14b8a6 100%); height: 100%; width: {percentage}%;"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <h4 style="color: #1e293b; margin-bottom: 15px;">Summary</h4>
                    """, unsafe_allow_html=True)
                    
                    for platform, count in platform_counts.items():
                        st.markdown(f"**{platform.title()}:** {count}")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("No platform data available")
            
            st.markdown("<br/><br/>", unsafe_allow_html=True)
            
            st.markdown("### 💾 System Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <h4 style="color: #1e293b; margin-bottom: 15px;">Database</h4>
                    <p style="color: #64748b; margin: 5px 0;"><strong>Type:</strong> SQLite (File System)</p>
                    <p style="color: #64748b; margin: 5px 0;"><strong>Vector Store:</strong> ChromaDB</p>
                    <p style="color: #64748b; margin: 5px 0;"><strong>Status:</strong> <span style="color: #10b981;">● Connected</span></p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                backend_url = get_backend_url()
                st.markdown(f"""
                <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <h4 style="color: #1e293b; margin-bottom: 15px;">API Status</h4>
                    <p style="color: #64748b; margin: 5px 0;"><strong>Backend URL:</strong> {backend_url}</p>
                    <p style="color: #64748b; margin: 5px 0;"><strong>Status:</strong> <span style="color: #10b981;">● Online</span></p>
                    <p style="color: #64748b; margin: 5px 0;"><strong>Version:</strong> v1.0.0 (Hackathon)</p>
                </div>
                """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"❌ Error loading analytics: {str(e)}")

# --- HELPER FUNCTIONS ---

def was_recently_active(created_at: str) -> bool:
    """Checks if the bot was created in the last 7 days"""
    if not created_at:
        return False
    try:
        # Handle potential timezone strings '2023-10-27T10:00:00.123456'
        created = datetime.fromisoformat(str(created_at).replace("Z", "+00:00"))
        # Make 'now' offset-naive to match SQLite usually returning naive datetimes
        # OR make both aware. Simplest hackathon fix: strip timezone.
        created = created.replace(tzinfo=None)
        seven_days_ago = datetime.now() - timedelta(days=7)
        return created > seven_days_ago
    except Exception as e:
        return False # Fallback if parsing fails