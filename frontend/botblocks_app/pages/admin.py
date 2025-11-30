import streamlit as st
import sys
import os
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from botblocks_app.components.ui import render_stat_card, inject_custom_css
from botblocks_app.utils import api_get, is_demo_mode

def show_admin():
    inject_custom_css()
    
    st.title("📊 Admin & Usage")
    st.markdown("Monitor platform usage and bot activity")
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    try:
        with st.spinner("Loading analytics..."):
            response = api_get("/bots")
            bots = response.get("bots", [])
            
            total_bots = len(bots)
            active_bots = sum(1 for bot in bots if bot.get("status") == "active")
            total_documents = sum(bot.get("documents_count", 0) for bot in bots)
            
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
                    label="Documents Uploaded",
                    value=str(total_documents),
                    icon="📚",
                    color="#7c3aed"
                )
            
            with col4:
                render_stat_card(
                    label="Last 7 Days Activity",
                    value=str(recent_activity),
                    icon="📅",
                    color="#f59e0b"
                )
            
            st.markdown("<br/><br/>", unsafe_allow_html=True)
            
            st.markdown("### 📊 Platform Distribution")
            
            platform_counts = {}
            for bot in bots:
                platform = bot.get("platform", "unknown")
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
            
            st.markdown("### 🤖 Recent Bots")
            
            if bots:
                recent_bots = sorted(bots, key=lambda x: x.get("created_at", ""), reverse=True)[:5]
                
                for bot in recent_bots:
                    status_colors = {
                        "active": "#10b981",
                        "inactive": "#6b7280",
                        "indexing": "#f59e0b",
                        "error": "#ef4444"
                    }
                    
                    status = bot.get("status", "active")
                    status_color = status_colors.get(status, "#6b7280")
                    
                    st.markdown(f"""
                    <div style="background-color: white; padding: 15px 20px; border-radius: 8px; margin: 10px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong style="color: #1e293b;">{bot.get('name', 'Untitled Bot')}</strong>
                            <span style="color: #64748b; font-size: 0.875rem; margin-left: 10px;">
                                {bot.get('platform', 'website').title()}
                            </span>
                        </div>
                        <div>
                            <span style="background-color: {status_color}; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 500; margin-right: 10px;">
                                {status}
                            </span>
                            <span style="color: #94a3b8; font-size: 0.75rem;">
                                {format_relative_time(bot.get('created_at'))}
                            </span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No bots created yet")
            
            st.markdown("<br/><br/>", unsafe_allow_html=True)
            
            st.markdown("### 💾 System Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <h4 style="color: #1e293b; margin-bottom: 15px;">Database</h4>
                    <p style="color: #64748b; margin: 5px 0;"><strong>Type:</strong> PostgreSQL / In-Memory</p>
                    <p style="color: #64748b; margin: 5px 0;"><strong>Status:</strong> <span style="color: #10b981;">● Connected</span></p>
                    <p style="color: #64748b; margin: 5px 0;"><strong>Mode:</strong> """ + ("Demo" if is_demo_mode() else "Production") + """</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <h4 style="color: #1e293b; margin-bottom: 15px;">API Status</h4>
                    <p style="color: #64748b; margin: 5px 0;"><strong>Backend URL:</strong> {os.getenv('BOTBLOCKS_BACKEND', 'localhost:8000')}</p>
                    <p style="color: #64748b; margin: 5px 0;"><strong>Status:</strong> <span style="color: {'#f59e0b' if is_demo_mode() else '#10b981'};">● {'Demo Mode' if is_demo_mode() else 'Connected'}</span></p>
                    <p style="color: #64748b; margin: 5px 0;"><strong>Version:</strong> 1.0.0</p>
                </div>
                """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"❌ Error loading analytics: {str(e)}")

def was_recently_active(created_at: str) -> bool:
    if not created_at:
        return False
    
    try:
        created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        seven_days_ago = datetime.now().astimezone() - timedelta(days=7)
        return created > seven_days_ago
    except:
        return False

def format_relative_time(dt_string: str) -> str:
    if not dt_string:
        return "Unknown"
    
    try:
        dt = datetime.fromisoformat(dt_string.replace("Z", "+00:00"))
        now = datetime.now().astimezone()
        diff = now - dt
        
        if diff.days > 7:
            return f"{diff.days} days ago"
        elif diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"
    except:
        return dt_string
