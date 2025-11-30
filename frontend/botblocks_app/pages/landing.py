import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from botblocks_app.components.ui import render_hero_section, render_feature_card, inject_custom_css

def show_landing():
    inject_custom_css()
    
    def navigate_to_wizard():
        st.session_state.current_page = "wizard"
        st.rerun()
    
    render_hero_section(
        title="🤖 BotBlocks",
        subtitle="WordPress for Chatbots - Build intelligent bots in minutes, no coding required",
        cta_text="Get Started - Create Your First Bot",
        cta_callback=navigate_to_wizard
    )
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>Why Choose BotBlocks?</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_feature_card(
            icon="🚀",
            title="Quick Setup",
            description="Create and deploy your chatbot in minutes with our intuitive wizard. No technical expertise required."
        )
    
    with col2:
        render_feature_card(
            icon="📚",
            title="Knowledge-Powered",
            description="Upload PDFs, docs, or URLs. Your bot learns from your content and provides accurate answers."
        )
    
    with col3:
        render_feature_card(
            icon="🌐",
            title="Multi-Platform",
            description="Deploy to Website, Telegram, and Discord. Manage all your bots from one dashboard."
        )
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_feature_card(
            icon="🎨",
            title="Custom Personas",
            description="Choose from pre-built personalities or create your own. Make your bot sound exactly how you want."
        )
    
    with col2:
        render_feature_card(
            icon="💬",
            title="Real-time Chat",
            description="Test your bot instantly with our built-in chat interface. See responses with source citations."
        )
    
    with col3:
        render_feature_card(
            icon="📊",
            title="Analytics Dashboard",
            description="Track usage, monitor conversations, and optimize your bot's performance with detailed insights."
        )
    
    st.markdown("<br/><br/>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-panel" style="padding: 40px; text-align: center;">
        <h2 style="margin-bottom: 20px;">Ready to Build Your Bot?</h2>
        <p style="font-size: 1.125rem; margin-bottom: 30px;">
            Join thousands of users who are already using BotBlocks to power their customer support, 
            sales, and engagement workflows.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Building Now", type="primary", use_container_width=True):
            navigate_to_wizard()
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    with st.expander("📖 How It Works"):
        st.markdown("""
        1. **Name Your Bot** - Give your bot a name and description
        2. **Choose Job Type** - Select RAG (knowledge-based) or Non-RAG (persona-only)
        3. **Upload Knowledge** - Add PDFs, documents, or URLs (for RAG bots)
        4. **Select Persona** - Choose a pre-built personality or customize your own
        5. **Choose Platform** - Deploy to Website, Telegram, or Discord
        6. **Test & Deploy** - Test your bot and get your embed code or platform credentials
        """)
    
    with st.expander("💡 Use Cases"):
        st.markdown("""
        - **Customer Support**: Answer FAQs automatically from your knowledge base
        - **Sales Assistant**: Qualify leads and answer product questions
        - **Internal Documentation**: Help employees find information quickly
        - **Educational Tutors**: Create learning assistants for any subject
        - **Community Management**: Moderate and engage with Discord/Telegram communities
        """)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 0.875rem; opacity: 0.7;'>© 2024 BotBlocks - WordPress for Chatbots</p>", unsafe_allow_html=True)
