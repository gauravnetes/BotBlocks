import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from botblocks_app.components.ui import render_progress_bar, render_file_preview, inject_custom_css, render_platform_badge
from botblocks_app.utils import (
    api_post_json, api_post_multipart, validate_bot_name, validate_telegram_token,
    validate_discord_token, validate_url, save_draft, load_draft, clear_draft,
    get_persona_options, get_platform_options, is_demo_mode
)

def initialize_wizard_state():
    if "wizard_step" not in st.session_state:
        st.session_state.wizard_step = 1
    if "bot_name" not in st.session_state:
        st.session_state.bot_name = ""
    if "bot_description" not in st.session_state:
        st.session_state.bot_description = ""
    if "job_type" not in st.session_state:
        st.session_state.job_type = "RAG"
    if "knowledge_files" not in st.session_state:
        st.session_state.knowledge_files = []
    if "knowledge_url" not in st.session_state:
        st.session_state.knowledge_url = ""
    if "knowledge_text" not in st.session_state:
        st.session_state.knowledge_text = ""
    if "persona_id" not in st.session_state:
        st.session_state.persona_id = "friendly"
    if "custom_prompt" not in st.session_state:
        st.session_state.custom_prompt = ""
    if "selected_platforms" not in st.session_state:
        st.session_state.selected_platforms = ["website"]
    if "telegram_token" not in st.session_state:
        st.session_state.telegram_token = ""
    if "discord_token" not in st.session_state:
        st.session_state.discord_token = ""
    if "show_telegram_token" not in st.session_state:
        st.session_state.show_telegram_token = False
    if "show_discord_token" not in st.session_state:
        st.session_state.show_discord_token = False
    if "created_bot_id" not in st.session_state:
        st.session_state.created_bot_id = None

def show_wizard():
    inject_custom_css()
    initialize_wizard_state()
    
    st.title("🧙 Bot Creation Wizard")
    st.markdown("Follow these steps to create your intelligent chatbot")
    
    step_names = ["Welcome", "Name", "Job Type", "Knowledge", "Persona", "Platform", "Details", "Review"]
    current_step = st.session_state.wizard_step
    
    if st.session_state.job_type == "Non-RAG":
        step_names = ["Welcome", "Name", "Job Type", "Persona", "Platform", "Details", "Review"]
        if current_step > 3:
            current_step = current_step - 1
    
    render_progress_bar(current_step, len(step_names), step_names)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    if st.session_state.wizard_step == 1:
        show_welcome_step()
    elif st.session_state.wizard_step == 2:
        show_name_step()
    elif st.session_state.wizard_step == 3:
        show_job_type_step()
    elif st.session_state.wizard_step == 4:
        if st.session_state.job_type == "RAG":
            show_knowledge_step()
        else:
            show_persona_step()
    elif st.session_state.wizard_step == 5:
        if st.session_state.job_type == "RAG":
            show_persona_step()
        else:
            show_platform_step()
    elif st.session_state.wizard_step == 6:
        if st.session_state.job_type == "RAG":
            show_platform_step()
        else:
            show_platform_details_step()
    elif st.session_state.wizard_step == 7:
        if st.session_state.job_type == "RAG":
            show_platform_details_step()
        else:
            show_review_step()
    elif st.session_state.wizard_step == 8:
        show_review_step()

def show_welcome_step():
    st.markdown("""
    <div style="background-color: white; padding: 40px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center;">
        <h2 style="color: #1e293b; margin-bottom: 20px;">👋 Welcome to BotBlocks!</h2>
        <p style="color: #64748b; font-size: 1.125rem; line-height: 1.8;">
            We'll guide you through creating your intelligent chatbot step by step.<br/>
            The entire process takes just a few minutes!
        </p>
        <br/>
        <p style="color: #64748b; font-size: 0.875rem;">
            ✨ You can save your progress as a draft at any time<br/>
            🔄 Navigate back and forth between steps<br/>
            📝 All your inputs are preserved until you build
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    draft = load_draft()
    if draft:
        st.info("📄 We found a saved draft from your previous session!")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📂 Load Draft", use_container_width=True):
                st.session_state.update(draft)
                st.success("Draft loaded successfully!")
                st.rerun()
        with col2:
            if st.button("🗑️ Clear Draft", use_container_width=True):
                clear_draft()
                st.success("Draft cleared!")
                st.rerun()
    
    col1, col2 = st.columns([1, 1])
    with col2:
        if st.button("Next ➡️", type="primary", use_container_width=True):
            st.session_state.wizard_step += 1
            st.rerun()

def show_name_step():
    st.markdown("""
    <div style="background-color: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
        <h2 style="color: #1e293b; margin-bottom: 10px;">📝 Name Your Bot</h2>
        <p style="color: #64748b;">Give your bot a memorable name and brief description</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    st.session_state.bot_name = st.text_input(
        "Bot Name *",
        value=st.session_state.bot_name,
        placeholder="e.g., Customer Support Bot",
        help="Choose a descriptive name for your bot"
    )
    
    st.session_state.bot_description = st.text_area(
        "Bot Description (Optional)",
        value=st.session_state.bot_description,
        placeholder="e.g., Helps customers find answers to common questions",
        height=100,
        help="Brief description of what your bot does"
    )
    
    is_valid, error_msg = validate_bot_name(st.session_state.bot_name)
    if st.session_state.bot_name and not is_valid:
        st.error(error_msg)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    show_navigation_buttons(can_proceed=is_valid)

def show_job_type_step():
    st.markdown("""
    <div style="background-color: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
        <h2 style="color: #1e293b; margin-bottom: 10px;">🎯 Choose Bot Job Type</h2>
        <p style="color: #64748b;">Select what you want your bot to do</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #0f766e 0%, #14b8a6 100%); padding: 30px; border-radius: 12px; color: white; height: 250px;">
            <div style="font-size: 3rem; margin-bottom: 15px;">📚</div>
            <h3 style="color: white; margin-bottom: 10px;">RAG Bot</h3>
            <p style="font-size: 0.875rem; line-height: 1.6;">
                Answer questions from your knowledge base. Upload documents, PDFs, or URLs and let your bot provide accurate answers with source citations.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select RAG", use_container_width=True, key="rag_btn"):
            st.session_state.job_type = "RAG"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%); padding: 30px; border-radius: 12px; color: white; height: 250px;">
            <div style="font-size: 3rem; margin-bottom: 15px;">🤖</div>
            <h3 style="color: white; margin-bottom: 10px;">Non-RAG Bot</h3>
            <p style="font-size: 0.875rem; line-height: 1.6;">
                Persona-based chatbot with a specific personality. Perfect for engagement, support, or entertainment without knowledge base requirements.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Non-RAG", use_container_width=True, key="nonrag_btn"):
            st.session_state.job_type = "Non-RAG"
            st.rerun()
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    st.info(f"✅ Currently selected: **{st.session_state.job_type}**")
    
    show_navigation_buttons()

def show_knowledge_step():
    st.markdown("""
    <div style="background-color: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
        <h2 style="color: #1e293b; margin-bottom: 10px;">📚 Provide Knowledge</h2>
        <p style="color: #64748b;">Upload files, provide URLs, or paste text for your bot to learn from</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📄 Upload Files", "🔗 From URL", "📝 Paste Text"])
    
    with tab1:
        uploaded_files = st.file_uploader(
            "Upload PDF or Text files",
            type=["pdf", "txt", "doc", "docx"],
            accept_multiple_files=True,
            help="Upload documents for your bot to learn from"
        )
        
        if uploaded_files:
            st.session_state.knowledge_files = uploaded_files
            st.success(f"✅ {len(uploaded_files)} file(s) uploaded")
            for file in uploaded_files:
                render_file_preview(file.name, file.size, file.name.split(".")[-1])
    
    with tab2:
        url = st.text_input(
            "Enter URL",
            value=st.session_state.knowledge_url,
            placeholder="https://example.com/documentation",
            help="Enter a URL to scrape content from"
        )
        
        if url != st.session_state.knowledge_url:
            st.session_state.knowledge_url = url
        
        if st.session_state.knowledge_url:
            is_valid, error_msg = validate_url(st.session_state.knowledge_url)
            if not is_valid:
                st.error(error_msg)
            else:
                st.success("✅ URL format is valid")
    
    with tab3:
        text = st.text_area(
            "Paste your content here",
            value=st.session_state.knowledge_text,
            placeholder="Paste documentation, FAQs, or any text content...",
            height=300,
            help="Enter text content for your bot to learn from"
        )
        
        if text != st.session_state.knowledge_text:
            st.session_state.knowledge_text = text
        
        if st.session_state.knowledge_text:
            word_count = len(st.session_state.knowledge_text.split())
            st.info(f"📊 Word count: {word_count}")
    
    has_knowledge = (
        st.session_state.knowledge_files or
        st.session_state.knowledge_url or
        st.session_state.knowledge_text
    )
    
    if not has_knowledge:
        st.warning("⚠️ Please provide at least one knowledge source")
    
    st.markdown("<br/>", unsafe_allow_html=True)
    show_navigation_buttons(can_proceed=has_knowledge)

def show_persona_step():
    st.markdown("""
    <div style="background-color: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
        <h2 style="color: #1e293b; margin-bottom: 10px;">🎨 Select Persona</h2>
        <p style="color: #64748b;">Choose how your bot communicates with users</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    personas = get_persona_options()
    
    persona_names = [p["name"] for p in personas]
    current_index = next((i for i, p in enumerate(personas) if p["id"] == st.session_state.persona_id), 0)
    
    selected_persona_name = st.radio(
        "Choose a persona:",
        persona_names,
        index=current_index,
        horizontal=False
    )
    
    selected_persona = next(p for p in personas if p["name"] == selected_persona_name)
    st.session_state.persona_id = selected_persona["id"]
    
    st.markdown(f"""
    <div style="background-color: #f8fafc; padding: 20px; border-radius: 8px; border-left: 4px solid #0f766e; margin: 15px 0;">
        <strong style="color: #1e293b;">Description:</strong><br/>
        <span style="color: #64748b;">{selected_persona["description"]}</span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.persona_id == "custom":
        st.session_state.custom_prompt = st.text_area(
            "Custom System Prompt",
            value=st.session_state.custom_prompt,
            placeholder="Define your bot's personality and behavior...",
            height=150,
            help="Describe how you want your bot to behave"
        )
        
        if not st.session_state.custom_prompt:
            st.warning("⚠️ Please provide a custom prompt for your persona")
    else:
        st.markdown(f"""
        <div style="background-color: #ecfdf5; padding: 15px; border-radius: 8px; margin-top: 15px;">
            <strong style="color: #047857;">System Prompt Preview:</strong><br/>
            <span style="color: #065f46; font-size: 0.875rem;">{selected_persona["prompt"]}</span>
        </div>
        """, unsafe_allow_html=True)
    
    can_proceed = st.session_state.persona_id != "custom" or st.session_state.custom_prompt
    
    st.markdown("<br/>", unsafe_allow_html=True)
    show_navigation_buttons(can_proceed=can_proceed)

def show_platform_step():
    st.markdown("""
    <div style="background-color: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
        <h2 style="color: #1e293b; margin-bottom: 10px;">🌐 Choose Platform(s)</h2>
        <p style="color: #64748b;">Select where you want to deploy your bot (you can choose multiple)</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    platforms = get_platform_options()
    
    st.markdown("**Available Platforms:**")
    
    for platform in platforms:
        is_selected = platform["id"] in st.session_state.selected_platforms
        
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"""
            <div style="background-color: {'#ecfdf5' if is_selected else '#f8fafc'}; padding: 20px; border-radius: 8px; border: 2px solid {'#0f766e' if is_selected else '#e2e8f0'}; margin: 10px 0;">
                <div style="font-size: 2rem; margin-bottom: 10px;">{platform["icon"]}</div>
                <h4 style="color: #1e293b; margin: 5px 0;">{platform["name"]}</h4>
                <p style="color: #64748b; font-size: 0.875rem;">{platform["description"]}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.checkbox("Select", value=is_selected, key=f"platform_{platform['id']}"):
                if platform["id"] not in st.session_state.selected_platforms:
                    st.session_state.selected_platforms.append(platform["id"])
            else:
                if platform["id"] in st.session_state.selected_platforms:
                    st.session_state.selected_platforms.remove(platform["id"])
    
    if not st.session_state.selected_platforms:
        st.warning("⚠️ Please select at least one platform")
    else:
        st.success(f"✅ Selected: {', '.join([p.title() for p in st.session_state.selected_platforms])}")
    
    st.markdown("<br/>", unsafe_allow_html=True)
    show_navigation_buttons(can_proceed=len(st.session_state.selected_platforms) > 0)

def show_platform_details_step():
    st.markdown("""
    <div style="background-color: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
        <h2 style="color: #1e293b; margin-bottom: 10px;">🔧 Platform Configuration</h2>
        <p style="color: #64748b;">Enter credentials for your selected platforms</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    needs_config = any(p in st.session_state.selected_platforms for p in ["telegram", "discord"])
    
    if "website" in st.session_state.selected_platforms:
        st.markdown("""
        <div style="background-color: #ecfdf5; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
            <h4 style="color: #047857; margin-bottom: 10px;">🌐 Website Integration</h4>
            <p style="color: #065f46; font-size: 0.875rem;">
                No configuration needed! After creating your bot, you'll receive an embed code 
                to add the chat widget to your website.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    if "telegram" in st.session_state.selected_platforms:
        st.markdown("### 💬 Telegram Configuration")
        
        token_type = "password" if not st.session_state.show_telegram_token else "text"
        st.session_state.telegram_token = st.text_input(
            "Telegram Bot Token *",
            value=st.session_state.telegram_token,
            type=token_type,
            placeholder="123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
            help="Get your bot token from @BotFather on Telegram"
        )
        
        st.checkbox("Show token", key="show_telegram_token")
        
        if st.session_state.telegram_token:
            is_valid, error_msg = validate_telegram_token(st.session_state.telegram_token)
            if not is_valid:
                st.error(error_msg)
        
        st.info("💡 Create a bot with @BotFather on Telegram to get your token")
        st.markdown("<br/>", unsafe_allow_html=True)
    
    if "discord" in st.session_state.selected_platforms:
        st.markdown("### 🎮 Discord Configuration")
        
        token_type = "password" if not st.session_state.show_discord_token else "text"
        st.session_state.discord_token = st.text_input(
            "Discord Bot Token *",
            value=st.session_state.discord_token,
            type=token_type,
            placeholder="Your Discord bot token",
            help="Get your bot token from Discord Developer Portal"
        )
        
        st.checkbox("Show token", key="show_discord_token")
        
        if st.session_state.discord_token:
            is_valid, error_msg = validate_discord_token(st.session_state.discord_token)
            if not is_valid:
                st.error(error_msg)
        
        st.info("💡 Create a bot in Discord Developer Portal to get your token")
    
    can_proceed = True
    if "telegram" in st.session_state.selected_platforms:
        is_valid, _ = validate_telegram_token(st.session_state.telegram_token)
        can_proceed = can_proceed and is_valid
    
    if "discord" in st.session_state.selected_platforms:
        is_valid, _ = validate_discord_token(st.session_state.discord_token)
        can_proceed = can_proceed and is_valid
    
    st.markdown("<br/>", unsafe_allow_html=True)
    show_navigation_buttons(can_proceed=can_proceed)

def show_review_step():
    st.markdown("""
    <div style="background-color: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
        <h2 style="color: #1e293b; margin-bottom: 10px;">✅ Review & Build</h2>
        <p style="color: #64748b;">Review your configuration before building your bot</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    st.markdown("### 📋 Bot Configuration Summary")
    
    st.markdown(f"""
    <div style="background-color: white; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; margin: 10px 0;">
        <strong>Bot Name:</strong> {st.session_state.bot_name}<br/>
        <strong>Description:</strong> {st.session_state.bot_description or 'None'}<br/>
        <strong>Job Type:</strong> {st.session_state.job_type}<br/>
        <strong>Persona:</strong> {st.session_state.persona_id.title()}<br/>
        <strong>Platforms:</strong> {', '.join([p.title() for p in st.session_state.selected_platforms])}
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.job_type == "RAG":
        st.markdown("### 📚 Knowledge Sources")
        knowledge_count = 0
        if st.session_state.knowledge_files:
            st.markdown(f"- **Files:** {len(st.session_state.knowledge_files)} uploaded")
            knowledge_count += len(st.session_state.knowledge_files)
        if st.session_state.knowledge_url:
            st.markdown(f"- **URL:** {st.session_state.knowledge_url}")
            knowledge_count += 1
        if st.session_state.knowledge_text:
            st.markdown(f"- **Text:** {len(st.session_state.knowledge_text)} characters")
            knowledge_count += 1
        
        if knowledge_count == 0:
            st.warning("⚠️ No knowledge sources configured")
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("💾 Save as Draft", use_container_width=True):
            draft_data = {
                "bot_name": st.session_state.bot_name,
                "bot_description": st.session_state.bot_description,
                "job_type": st.session_state.job_type,
                "knowledge_url": st.session_state.knowledge_url,
                "knowledge_text": st.session_state.knowledge_text,
                "persona_id": st.session_state.persona_id,
                "custom_prompt": st.session_state.custom_prompt,
                "selected_platforms": st.session_state.selected_platforms,
                "telegram_token": st.session_state.telegram_token,
                "discord_token": st.session_state.discord_token,
            }
            if save_draft(draft_data):
                st.success("✅ Draft saved successfully!")
            else:
                st.error("❌ Failed to save draft")
    
    with col2:
        if st.button("🚀 Build Bot", type="primary", use_container_width=True):
            build_bot()
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Back", use_container_width=True):
            st.session_state.wizard_step -= 1
            st.rerun()

def build_bot():
    with st.spinner("🔨 Building your bot..."):
        try:
            persona = next(p for p in get_persona_options() if p["id"] == st.session_state.persona_id)
            system_prompt = st.session_state.custom_prompt if st.session_state.persona_id == "custom" else persona["prompt"]
            
            main_platform = st.session_state.selected_platforms[0]
            
            response = api_post_json("/bots/create", {
                "name": st.session_state.bot_name,
                "description": st.session_state.bot_description,
                "platform": main_platform,
                "system_prompt": system_prompt
            })
            
            bot = response.get("bot", {})
            public_id = bot.get("public_id")
            
            if not public_id:
                st.error("❌ Failed to create bot: No public_id returned")
                return
            
            st.session_state.created_bot_id = public_id
            
            if st.session_state.job_type == "RAG":
                if st.session_state.knowledge_files:
                    for file in st.session_state.knowledge_files:
                        files = {"file": (file.name, file.getvalue(), file.type)}
                        api_post_multipart(f"/bots/{public_id}/documents", files=files)
                
                if st.session_state.knowledge_url:
                    api_post_json(f"/bots/{public_id}/documents", {
                        "url": st.session_state.knowledge_url,
                        "meta": {}
                    })
                
                if st.session_state.knowledge_text:
                    api_post_json(f"/bots/{public_id}/documents", {
                        "text": st.session_state.knowledge_text,
                        "meta": {}
                    })
                
                api_post_json(f"/bots/{public_id}/index", {})
            
            api_post_json(f"/bots/{public_id}/persona", {
                "persona_id": st.session_state.persona_id,
                "system_prompt": system_prompt
            })
            
            for platform in st.session_state.selected_platforms:
                platform_details = {}
                if platform == "telegram":
                    platform_details["token"] = st.session_state.telegram_token
                elif platform == "discord":
                    platform_details["token"] = st.session_state.discord_token
                
                api_post_json(f"/bots/{public_id}/platform", {
                    "platform": platform,
                    "details": platform_details
                })
            
            st.balloons()
            st.success(f"✅ Bot '{st.session_state.bot_name}' created successfully!")
            
            if is_demo_mode():
                st.info("ℹ️ Running in demo mode. Connect to backend to persist your bot.")
            
            clear_draft()
            
            st.markdown(f"""
            <div style="background-color: #ecfdf5; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #047857;">🎉 Success!</h3>
                <p style="color: #065f46;">Your bot has been created and is ready to use!</p>
                <strong>Bot ID:</strong> <code>{public_id}</code>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📊 Go to Dashboard", use_container_width=True):
                    st.session_state.current_page = "dashboard"
                    reset_wizard_state()
                    st.rerun()
            with col2:
                if st.button("🔍 View Bot Details", use_container_width=True):
                    st.session_state.current_page = "bot_detail"
                    st.session_state.selected_bot_id = public_id
                    reset_wizard_state()
                    st.rerun()
        
        except Exception as e:
            st.error(f"❌ Error building bot: {str(e)}")

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
