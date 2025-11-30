import streamlit as st
import sys
import os
import time
from botblocks_app.services import api  # The bridge to your backend

# Ensure path is correct for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from botblocks_app.components.ui import render_progress_bar, render_file_preview, inject_custom_css
from botblocks_app.utils import (
    validate_bot_name, validate_telegram_token, validate_discord_token, 
    validate_url, save_draft, load_draft, clear_draft,
    get_persona_options, get_platform_options, is_demo_mode
)

# --- STATE MANAGEMENT ---
def initialize_wizard_state():
    defaults = {
        "wizard_step": 1,
        "bot_name": "",
        "bot_description": "",
        "job_type": "RAG",
        "knowledge_files": [],
        "knowledge_url": "",
        "knowledge_text": "",
        "persona_id": "friendly",
        "custom_prompt": "",
        "selected_platforms": ["website"],
        "telegram_token": "",
        "discord_token": "",
        "show_telegram_token": False,
        "show_discord_token": False,
        "created_bot_id": None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def reset_wizard_state():
    keys_to_reset = [
        "wizard_step", "bot_name", "bot_description", "job_type",
        "knowledge_files", "knowledge_url", "knowledge_text",
        "persona_id", "custom_prompt", "selected_platforms",
        "telegram_token", "discord_token", "created_bot_id"
    ]
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]

# --- MAIN CONTROLLER ---
def show_wizard():
    inject_custom_css()
    initialize_wizard_state()
    
    st.title("🧙 Bot Creation Wizard")
    st.markdown("Follow these steps to create your intelligent chatbot")
    
    # Define Steps
    step_names = ["Welcome", "Name", "Job Type", "Knowledge", "Persona", "Platform", "Details", "Review"]
    
    # Adjust steps if Non-RAG
    if st.session_state.job_type == "Non-RAG":
        step_names = ["Welcome", "Name", "Job Type", "Persona", "Platform", "Details", "Review"]
    
    # Progress Bar Logic
    current_step_display = st.session_state.wizard_step
    if st.session_state.job_type == "Non-RAG" and current_step_display > 3:
        current_step_display -= 1 # Adjust visual progress for skipped step
        
    render_progress_bar(current_step_display, len(step_names), step_names)
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # State Machine Routing
    step = st.session_state.wizard_step
    job = st.session_state.job_type
    
    if step == 1: show_welcome_step()
    elif step == 2: show_name_step()
    elif step == 3: show_job_type_step()
    elif step == 4: show_knowledge_step() if job == "RAG" else show_persona_step()
    elif step == 5: show_persona_step() if job == "RAG" else show_platform_step()
    elif step == 6: show_platform_step() if job == "RAG" else show_platform_details_step()
    elif step == 7: show_platform_details_step() if job == "RAG" else show_review_step()
    elif step == 8: show_review_step()

# --- NAVIGATION HELPER ---
def show_navigation_buttons(can_proceed: bool = True):
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.session_state.wizard_step > 1:
            if st.button("⬅️ Back", use_container_width=True):
                st.session_state.wizard_step -= 1
                st.rerun()
    with col2:
        if can_proceed:
            if st.button("Next ➡️", type="primary", use_container_width=True):
                st.session_state.wizard_step += 1
                st.rerun()
        else:
            st.button("Next ➡️", use_container_width=True, disabled=True)

# --- STEP 1: WELCOME ---
def show_welcome_step():
    st.markdown("""
    <div class="glass-panel" style="padding: 40px; text-align: center;">
        <h2 style="margin-bottom: 20px;">👋 Welcome to BotBlocks!</h2>
        <p style="font-size: 1.125rem;">We'll guide you through creating your intelligent chatbot step by step.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br/>", unsafe_allow_html=True)
    
    draft = load_draft()
    if draft:
        st.info("📄 Found a saved draft!")
        if st.button("📂 Load Draft", use_container_width=True):
            st.session_state.update(draft)
            st.rerun()
            
    col1, col2 = st.columns([1, 1])
    with col2:
        if st.button("Start ➡️", type="primary", use_container_width=True):
            st.session_state.wizard_step += 1
            st.rerun()

# --- STEP 2: NAME ---
def show_name_step():
    st.header("📝 Name Your Bot")
    st.session_state.bot_name = st.text_input("Bot Name *", value=st.session_state.bot_name)
    st.session_state.bot_description = st.text_area("Description", value=st.session_state.bot_description)
    
    is_valid, error_msg = validate_bot_name(st.session_state.bot_name)
    if st.session_state.bot_name and not is_valid:
        st.error(error_msg)
        
    show_navigation_buttons(can_proceed=is_valid)

# --- STEP 3: JOB TYPE ---
def show_job_type_step():
    st.header("🎯 Choose Job Type")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("📚 **RAG Bot**\n\nAnswers questions based on uploaded documents.")
        if st.button("Select RAG", use_container_width=True, type="primary" if st.session_state.job_type == "RAG" else "secondary"):
            st.session_state.job_type = "RAG"
            st.rerun()
            
    with col2:
        st.info("🤖 **Persona Bot**\n\nChits-chats with a specific personality.")
        if st.button("Select Non-RAG", use_container_width=True, type="primary" if st.session_state.job_type == "Non-RAG" else "secondary"):
            st.session_state.job_type = "Non-RAG"
            st.rerun()
            
    show_navigation_buttons()

# --- STEP 4: KNOWLEDGE (RAG ONLY) ---
def show_knowledge_step():
    st.header("📚 Add Knowledge")
    uploaded_files = st.file_uploader("Upload PDF/TXT", type=["pdf", "txt"], accept_multiple_files=True)
    
    if uploaded_files:
        st.session_state.knowledge_files = uploaded_files
        st.success(f"✅ {len(uploaded_files)} files selected")
    
    st.divider()
    st.caption("Note: URL and Text Input are disabled for this hackathon demo.")
    
    has_knowledge = len(st.session_state.knowledge_files) > 0
    show_navigation_buttons(can_proceed=has_knowledge)

# --- STEP 5: PERSONA ---
def show_persona_step():
    st.header("🎨 Select Persona")
    personas = get_persona_options()
    names = [p["name"] for p in personas]
    
    # Find current selection index
    try:
        idx = next(i for i, p in enumerate(personas) if p["id"] == st.session_state.persona_id)
    except StopIteration:
        idx = 0

    selection = st.radio("Choose Persona", names, index=idx)
    selected_obj = next(p for p in personas if p["name"] == selection)
    st.session_state.persona_id = selected_obj["id"]
    
    if st.session_state.persona_id == "custom":
        st.session_state.custom_prompt = st.text_area("Custom System Prompt", value=st.session_state.custom_prompt)
    else:
        st.info(f"**Prompt Preview:** {selected_obj['prompt']}")

    can_proceed = st.session_state.persona_id != "custom" or st.session_state.custom_prompt
    show_navigation_buttons(can_proceed=can_proceed)

# --- STEP 6: PLATFORM ---
def show_platform_step():
    st.header("🌐 Choose Platform")
    
    platforms = get_platform_options()
    for p in platforms:
        checked = p["id"] in st.session_state.selected_platforms
        if st.checkbox(f"{p['icon']} {p['name']}", value=checked, key=p['id']):
            if p["id"] not in st.session_state.selected_platforms:
                st.session_state.selected_platforms.append(p["id"])
        else:
            if p["id"] in st.session_state.selected_platforms:
                st.session_state.selected_platforms.remove(p["id"])
                
    show_navigation_buttons(can_proceed=len(st.session_state.selected_platforms) > 0)

# --- STEP 7: DETAILS ---
def show_platform_details_step():
    st.header("🔧 Configuration")
    
    if "telegram" in st.session_state.selected_platforms:
        st.subheader("Telegram")
        st.session_state.telegram_token = st.text_input("Bot Token", value=st.session_state.telegram_token, type="password")
        
    if "discord" in st.session_state.selected_platforms:
        st.subheader("Discord")
        st.session_state.discord_token = st.text_input("Bot Token", value=st.session_state.discord_token, type="password")
        
    if "website" in st.session_state.selected_platforms:
        st.info("🌐 Website: No config needed. You will get an embed code after building.")

    show_navigation_buttons()

# --- STEP 8: REVIEW & BUILD ---
def show_review_step():
    st.header("✅ Review & Build")
    
    # Summary Card
    st.markdown(f"""
    <div class="glass-panel" style="padding: 20px; margin: 10px 0;">
        <strong>Bot Name:</strong> {st.session_state.bot_name}<br/>
        <strong>Job Type:</strong> {st.session_state.job_type}<br/>
        <strong>Persona:</strong> {st.session_state.persona_id.title()}<br/>
        <strong>Platforms:</strong> {', '.join(st.session_state.selected_platforms).title()}
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.job_type == "RAG":
        st.write(f"**Files:** {len(st.session_state.knowledge_files)} uploaded")

    st.markdown("<br/>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("💾 Save Draft", use_container_width=True):
            # Simple draft logic
            if save_draft(dict(st.session_state)):
                st.success("Draft saved!")
            else:
                st.error("Could not save draft.")

    # THE BUILD BUTTON connects to build_bot()
    with col2:
        if st.button("🚀 Build Bot", type="primary", use_container_width=True):
            build_bot()

    st.markdown("<br/>", unsafe_allow_html=True)
    if st.button("⬅️ Back", use_container_width=True):
        st.session_state.wizard_step -= 1
        st.rerun()

# --- CORE LOGIC: BUILD BOT ---
def build_bot():
    with st.spinner("🔨 Building your bot..."):
        try:
            # 1. Resolve System Prompt
            if st.session_state.persona_id == "custom":
                system_prompt = st.session_state.custom_prompt
            else:
                # Find prompt from options
                personas = get_persona_options()
                try:
                    p = next(x for x in personas if x["id"] == st.session_state.persona_id)
                    system_prompt = p["prompt"]
                except StopIteration:
                    system_prompt = "You are a helpful assistant."

            # 2. Resolve Platform & Token
            main_platform = "web"
            if st.session_state.selected_platforms:
                main_platform = st.session_state.selected_platforms[0]
            
            token = None
            if main_platform == "telegram":
                token = st.session_state.telegram_token
            elif main_platform == "discord":
                token = st.session_state.discord_token

            # 3. Call Backend to Create Bot
            new_bot = api.create_bot(
                name=st.session_state.bot_name,
                system_prompt=system_prompt,
                platform=main_platform,
                platform_token=token
            )
            
            if not new_bot:
                st.error("❌ Failed to create bot on server.")
                return

            public_id = new_bot.get("public_id")
            st.session_state.created_bot_id = public_id

            # 4. Upload Knowledge (RAG Only)
            if st.session_state.job_type == "RAG" and st.session_state.knowledge_files:
                progress_text = st.empty()
                total = len(st.session_state.knowledge_files)
                for i, file_obj in enumerate(st.session_state.knowledge_files):
                    progress_text.text(f"📚 Ingesting file {i+1}/{total}...")
                    api.upload_knowledge(public_id, file_obj)
                progress_text.empty()

            # 5. Success & Redirect
            st.balloons()
            st.success("Bot Created Successfully!")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📊 Go to Dashboard", use_container_width=True):
                    st.session_state.current_page = "dashboard"
                    reset_wizard_state()
                    st.rerun()
            with col2:
                if st.button("🔍 View Bot Details", use_container_width=True):
                    st.session_state.current_page = "bot_detail"
                    st.session_state.selected_bot = new_bot
                    reset_wizard_state()
                    st.rerun()
        
        except Exception as e:
            st.error(f"❌ Error building bot: {str(e)}")