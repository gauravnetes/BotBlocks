import os
import streamlit as st
from typing import Optional, List, Dict, Any
import base64
from io import BytesIO
def render_card(title: str, content: str, subtitle: Optional[str] = None, 
                status: Optional[str] = None, actions: Optional[List[Dict[str, Any]]] = None):
    status_colors = {
        "active": "#10b981",
        "inactive": "#6b7280",
        "indexing": "#f59e0b",
        "error": "#ef4444"
    }
    
    status_html = ""
    if status:
        color = status_colors.get(status, "#6b7280")
        status_html = f'<span style="background-color: {color}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; margin-left: 10px;">{status}</span>'
    
    subtitle_html = f'<p style="color: #6b7280; font-size: 0.875rem; margin-top: 5px;">{subtitle}</p>' if subtitle else ""
    
    st.markdown(f"""
    <div class="glass-panel" style="padding: 20px; margin-bottom: 15px;">
        <h3 style="margin: 0; text-transform: uppercase; letter-spacing: 0.05em; font-size: 1.1rem;">{title}{status_html}</h3>
        {subtitle_html}
        <p style="margin-top: 10px; font-size: 0.9rem;">{content}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if actions:
        cols = st.columns(len(actions))
        for idx, action in enumerate(actions):
            with cols[idx]:
                if st.button(action.get("label", "Action"), key=action.get("key")):
                    if "callback" in action:
                        action["callback"]()

def render_chat_bubble(message: str, is_user: bool = True, sources: Optional[List[Dict]] = None):
    if is_user:
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-end; margin: 10px 0;">
            <div class="chat-user" style="max-width: 70%;">
                {message}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-start; margin: 10px 0;">
            <div class="chat-bot" style="max-width: 70%;">
                {message}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if sources:
            with st.expander("📚 View Sources", expanded=False):
                for idx, source in enumerate(sources):
                    st.markdown(f"""
                    <div style="background-color: #e0f2fe; padding: 10px; border-radius: 8px; margin: 5px 0;">
                        <strong>Source {idx + 1}</strong> (Score: {source.get('score', 0):.2f})<br/>
                        <span style="color: #475569; font-size: 0.875rem;">{source.get('text', '')[:200]}...</span>
                    </div>
                    """, unsafe_allow_html=True)

def render_progress_bar(current_step: int, total_steps: int, step_names: Optional[List[str]] = None):
    progress_percentage = (current_step / total_steps) * 100
    
    st.markdown(f"""
    <div style="margin: 20px 0;">
        <div style="background-color: var(--zinc-800); height: 4px; border-radius: 0; overflow: hidden;">
            <div style="background-color: var(--accent); height: 100%; width: {progress_percentage}%; transition: width 0.3s ease;"></div>
        </div>
        <p style="text-align: center; color: var(--text-muted); margin-top: 10px; font-size: 0.75rem; font-family: var(--font-mono);">STEP {current_step} / {total_steps}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if step_names:
        cols = st.columns(len(step_names))
        for idx, name in enumerate(step_names):
            with cols[idx]:
                color = "var(--accent)" if idx + 1 <= current_step else "var(--zinc-700)"
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="width: 24px; height: 24px; border-radius: 2px; background-color: {color}; color: var(--zinc-950); display: flex; align-items: center; justify-content: center; margin: 0 auto; font-weight: bold; font-size: 0.75rem;">
                        {idx + 1}
                    </div>
                    <p style="font-size: 0.7rem; color: var(--text-muted); margin-top: 5px; text-transform: uppercase;">{name}</p>
                </div>
                """, unsafe_allow_html=True)

def render_file_preview(file_name: str, file_size: int, file_type: str = "unknown"):
    icons = {
        "pdf": "📄",
        "txt": "📝",
        "doc": "📃",
        "docx": "📃",
        "unknown": "📎"
    }
    
    icon = icons.get(file_type.lower(), icons["unknown"])
    size_kb = file_size / 1024
    size_str = f"{size_kb:.1f} KB" if size_kb < 1024 else f"{size_kb/1024:.1f} MB"
    
    st.markdown(f"""
    <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; margin: 5px 0; display: flex; align-items: center;">
        <span style="font-size: 2rem; margin-right: 12px;">{icon}</span>
        <div style="flex: 1;">
            <div style="font-weight: 500; color: #1e293b;">{file_name}</div>
            <div style="font-size: 0.75rem; color: #64748b;">{size_str}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_code_snippet(code: str, language: str = "html", title: Optional[str] = None):
    if title:
        st.markdown(f"**{title}**")
    
    st.code(code, language=language)
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("📋 Copy", key=f"copy_{hash(code)}"):
            st.session_state[f"copied_{hash(code)}"] = True
            st.success("Copied to clipboard!")
    
    with col2:
        if st.session_state.get(f"copied_{hash(code)}", False):
            st.markdown('<span style="color: #10b981; font-size: 0.875rem;">✓ Copied!</span>', unsafe_allow_html=True)

def render_stat_card(label: str, value: str, icon: str = "📊", color: str = "#0f766e"):
    st.markdown(f"""
    <div style="background-color: var(--zinc-900); border: 1px solid var(--border-color); color: var(--text-primary); padding: 20px; border-radius: 2px; box-shadow: 4px 4px 0px var(--zinc-800);">
        <div style="font-size: 2rem; margin-bottom: 10px; color: var(--accent);">{icon}</div>
        <div style="font-size: 2rem; font-weight: bold; margin-bottom: 5px; font-family: var(--font-mono);">{value}</div>
        <div style="font-size: 0.875rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em;">{label}</div>
    </div>
    """, unsafe_allow_html=True)

def render_confirm_dialog(message: str, confirm_label: str = "Confirm", cancel_label: str = "Cancel") -> Optional[bool]:
    st.warning(message)
    col1, col2 = st.columns(2)
    with col1:
        if st.button(confirm_label, type="primary"):
            return True
    with col2:
        if st.button(cancel_label):
            return False
    return None

def render_hero_section(title: str, subtitle: str, cta_text: str, cta_callback):
    st.markdown(f"""
    <div class="hero-container animate-fade-in">
        <h1 class="hero-title">{title}</h1>
        <p class="hero-subtitle">>> {subtitle}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(cta_text, type="primary", use_container_width=True):
            cta_callback()

def render_feature_card(icon: str, title: str, description: str):
    st.markdown(f"""
    <div class="glass-panel feature-card">
        <div class="feature-icon">{icon}</div>
        <h3 style="margin-bottom: 10px;">{title}</h3>
        <p style="font-size: 0.875rem;">{description}</p>
    </div>
    """, unsafe_allow_html=True)

def render_platform_badge(platform: str, active: bool = False):
    platform_icons = {
        "website": "🌐",
        "telegram": "💬",
        "discord": "🎮"
    }
    
    icon = platform_icons.get(platform.lower(), "📱")
    bg_color = "var(--accent)" if active else "var(--zinc-800)"
    text_color = "var(--zinc-950)" if active else "var(--text-secondary)"
    
    st.markdown(f"""
    <span style="background-color: {bg_color}; color: {text_color}; padding: 4px 12px; border-radius: 2px; font-size: 0.75rem; margin-right: 8px; display: inline-block; font-family: var(--font-mono); text-transform: uppercase; font-weight: bold;">
        {icon} {platform}
    </span>
    """, unsafe_allow_html=True)

def inject_custom_css():
    css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "styles.css")
    with open(css_file, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
