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
    <div style="background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 15px;">
        <h3 style="margin: 0; color: #1e293b;">{title}{status_html}</h3>
        {subtitle_html}
        <p style="color: #475569; margin-top: 10px;">{content}</p>
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
            <div style="background-color: #0f766e; color: white; padding: 12px 16px; border-radius: 18px 18px 4px 18px; max-width: 70%; box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                {message}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-start; margin: 10px 0;">
            <div style="background-color: #f1f5f9; color: #1e293b; padding: 12px 16px; border-radius: 18px 18px 18px 4px; max-width: 70%; box-shadow: 0 1px 2px rgba(0,0,0,0.1);">
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
        <div style="background-color: #e2e8f0; height: 8px; border-radius: 4px; overflow: hidden;">
            <div style="background: linear-gradient(90deg, #0f766e 0%, #14b8a6 100%); height: 100%; width: {progress_percentage}%; transition: width 0.3s ease;"></div>
        </div>
        <p style="text-align: center; color: #64748b; margin-top: 10px; font-size: 0.875rem;">Step {current_step} of {total_steps}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if step_names:
        cols = st.columns(len(step_names))
        for idx, name in enumerate(step_names):
            with cols[idx]:
                color = "#0f766e" if idx + 1 <= current_step else "#cbd5e1"
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="width: 30px; height: 30px; border-radius: 50%; background-color: {color}; color: white; display: flex; align-items: center; justify-content: center; margin: 0 auto; font-weight: bold; font-size: 0.875rem;">
                        {idx + 1}
                    </div>
                    <p style="font-size: 0.75rem; color: #475569; margin-top: 5px;">{name}</p>
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
    <div style="background: linear-gradient(135deg, {color} 0%, {color}dd 100%); color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <div style="font-size: 2rem; margin-bottom: 10px;">{icon}</div>
        <div style="font-size: 2rem; font-weight: bold; margin-bottom: 5px;">{value}</div>
        <div style="font-size: 0.875rem; opacity: 0.9;">{label}</div>
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
    <div style="text-align: center; padding: 60px 20px; background: linear-gradient(135deg, #0f766e 0%, #14b8a6 100%); border-radius: 16px; margin-bottom: 30px;">
        <h1 style="color: white; font-size: 3rem; margin-bottom: 20px; text-shadow: 0 2px 4px rgba(0,0,0,0.1);">{title}</h1>
        <p style="color: white; font-size: 1.25rem; opacity: 0.95; margin-bottom: 30px;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(cta_text, type="primary", use_container_width=True):
            cta_callback()

def render_feature_card(icon: str, title: str, description: str):
    st.markdown(f"""
    <div style="text-align: center; padding: 30px; background-color: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); height: 100%;">
        <div style="font-size: 3rem; margin-bottom: 15px;">{icon}</div>
        <h3 style="color: #1e293b; margin-bottom: 10px;">{title}</h3>
        <p style="color: #64748b; font-size: 0.875rem;">{description}</p>
    </div>
    """, unsafe_allow_html=True)

def render_platform_badge(platform: str, active: bool = False):
    platform_icons = {
        "website": "🌐",
        "telegram": "💬",
        "discord": "🎮"
    }
    
    icon = platform_icons.get(platform.lower(), "📱")
    bg_color = "#0f766e" if active else "#e2e8f0"
    text_color = "white" if active else "#64748b"
    
    st.markdown(f"""
    <span style="background-color: {bg_color}; color: {text_color}; padding: 6px 12px; border-radius: 16px; font-size: 0.875rem; margin-right: 8px; display: inline-block;">
        {icon} {platform.title()}
    </span>
    """, unsafe_allow_html=True)

def inject_custom_css():
    st.markdown("""
    <style>
        .main {
            background-color: #f8fafc;
        }
        
        .stButton>button {
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        .stTextInput>div>div>input {
            border-radius: 8px;
        }
        
        .stTextArea>div>div>textarea {
            border-radius: 8px;
        }
        
        .stSelectbox>div>div>select {
            border-radius: 8px;
        }
        
        div[data-testid="stExpander"] {
            background-color: white;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
        }
        
        .uploadedFile {
            background-color: #f8fafc;
            border-radius: 8px;
            padding: 10px;
        }
        
        .stAlert {
            border-radius: 8px;
        }
        
        h1, h2, h3 {
            color: #1e293b;
        }
        
        .sidebar .sidebar-content {
            background-color: #ffffff;
        }
    </style>
    """, unsafe_allow_html=True)
