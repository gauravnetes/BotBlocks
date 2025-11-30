import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from botblocks_app.components.ui import inject_custom_css
from botblocks_app.utils import get_backend_url, is_demo_mode

def show_settings():
    inject_custom_css()
    
    st.title("⚙️ Settings")
    st.markdown("Manage your account and application settings")
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🔑 API Keys", "👤 Account", "💳 Billing"])
    
    with tab1:
        show_api_keys_tab()
    
    with tab2:
        show_account_tab()
    
    with tab3:
        show_billing_tab()

def show_api_keys_tab():
    st.markdown("### 🔑 API Keys & Secrets")
    st.markdown("Manage API keys for integrations and external services")
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #fef3c7; padding: 15px; border-radius: 8px; border-left: 4px solid #f59e0b; margin-bottom: 20px;">
        <strong style="color: #92400e;">⚠️ Security Notice</strong><br/>
        <span style="color: #78350f; font-size: 0.875rem;">
            API keys are stored locally in your browser session. Never share your keys publicly.
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### Backend Configuration")
    
    current_backend = get_backend_url()
    
    if "custom_backend_url" not in st.session_state:
        st.session_state.custom_backend_url = current_backend
    
    new_backend = st.text_input(
        "Backend URL",
        value=st.session_state.custom_backend_url,
        placeholder="http://localhost:8000",
        help="URL of your BotBlocks backend API"
    )
    
    if new_backend != st.session_state.custom_backend_url:
        st.session_state.custom_backend_url = new_backend
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if st.button("💾 Save", type="primary"):
            os.environ["BOTBLOCKS_BACKEND"] = st.session_state.custom_backend_url
            st.success("✅ Backend URL updated!")
            st.info("🔄 Refresh the page to apply changes")
    
    with col2:
        if st.button("🔄 Reset to Default"):
            st.session_state.custom_backend_url = "http://localhost:8000"
            os.environ["BOTBLOCKS_BACKEND"] = "http://localhost:8000"
            st.rerun()
    
    if is_demo_mode():
        st.warning("⚠️ Currently running in demo mode. Backend connection unavailable.")
    else:
        st.success(f"✅ Connected to: {current_backend}")
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    st.markdown("#### Platform API Keys")
    
    with st.expander("Telegram Bot Token", expanded=False):
        telegram_token = st.text_input(
            "Enter your Telegram bot token",
            type="password",
            key="settings_telegram_token",
            placeholder="123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
        )
        st.markdown("Get your token from [@BotFather](https://t.me/botfather) on Telegram")
        
        if telegram_token:
            if st.button("💾 Save Telegram Token"):
                st.success("✅ Token saved locally (session only)")
    
    with st.expander("Discord Bot Token", expanded=False):
        discord_token = st.text_input(
            "Enter your Discord bot token",
            type="password",
            key="settings_discord_token",
            placeholder="Your Discord bot token"
        )
        st.markdown("Get your token from [Discord Developer Portal](https://discord.com/developers/applications)")
        
        if discord_token:
            if st.button("💾 Save Discord Token"):
                st.success("✅ Token saved locally (session only)")
    
    with st.expander("OpenAI API Key (Optional)", expanded=False):
        openai_key = st.text_input(
            "Enter your OpenAI API key",
            type="password",
            key="settings_openai_key",
            placeholder="sk-..."
        )
        st.markdown("Optional: For advanced AI features. Get your key from [OpenAI Platform](https://platform.openai.com)")
        
        if openai_key:
            if st.button("💾 Save OpenAI Key"):
                st.success("✅ Token saved locally (session only)")

def show_account_tab():
    st.markdown("### 👤 Account Information")
    
    st.markdown("""
    <div style="background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin: 20px 0;">
        <h4 style="color: #1e293b; margin-bottom: 15px;">Profile</h4>
        <p style="color: #64748b; margin: 8px 0;"><strong>Email:</strong> demo@botblocks.io</p>
        <p style="color: #64748b; margin: 8px 0;"><strong>Plan:</strong> <span style="background-color: #0f766e; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem;">Free Tier</span></p>
        <p style="color: #64748b; margin: 8px 0;"><strong>Member Since:</strong> November 2024</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### Update Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Display Name", value="Demo User", placeholder="Your name")
    
    with col2:
        st.text_input("Email", value="demo@botblocks.io", placeholder="your@email.com")
    
    st.text_area("Bio", placeholder="Tell us about yourself...", height=100)
    
    if st.button("💾 Save Changes", type="primary"):
        st.success("✅ Profile updated! (Demo - changes not persisted)")
    
    st.markdown("<br/><br/>", unsafe_allow_html=True)
    
    st.markdown("### 🔒 Security")
    
    with st.expander("Change Password"):
        st.text_input("Current Password", type="password")
        st.text_input("New Password", type="password")
        st.text_input("Confirm New Password", type="password")
        
        if st.button("🔐 Update Password"):
            st.success("✅ Password updated! (Demo)")
    
    with st.expander("Two-Factor Authentication"):
        st.markdown("Enable 2FA for additional security")
        
        if st.checkbox("Enable 2FA", value=False):
            st.info("📱 Scan the QR code with your authenticator app (Demo)")
            st.button("✅ Verify and Enable")
    
    st.markdown("<br/><br/>", unsafe_allow_html=True)
    
    st.markdown("### 🗑️ Danger Zone")
    
    st.markdown("""
    <div style="background-color: #fef2f2; padding: 20px; border-radius: 8px; border-left: 4px solid #ef4444;">
        <strong style="color: #991b1b;">Delete Account</strong><br/>
        <span style="color: #7f1d1d; font-size: 0.875rem;">
            This action cannot be undone. All your bots and data will be permanently deleted.
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    if st.button("🗑️ Delete My Account", type="secondary"):
        st.warning("Account deletion is not available in demo mode")

def show_billing_tab():
    st.markdown("### 💳 Billing & Subscription")
    
    st.markdown("""
    <div style="background-color: #ecfdf5; padding: 20px; border-radius: 12px; border-left: 4px solid #10b981; margin: 20px 0;">
        <strong style="color: #047857;">Current Plan: Free Tier</strong><br/>
        <span style="color: #065f46; font-size: 0.875rem;">
            Upgrade to unlock unlimited bots, advanced analytics, and priority support.
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### Available Plans")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background-color: white; padding: 25px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); height: 400px;">
            <h3 style="color: #1e293b; margin-bottom: 10px;">Free</h3>
            <div style="font-size: 2rem; font-weight: bold; color: #0f766e; margin-bottom: 20px;">$0<span style="font-size: 1rem; color: #64748b;">/mo</span></div>
            <ul style="color: #64748b; font-size: 0.875rem; line-height: 2;">
                <li>✅ Up to 3 bots</li>
                <li>✅ 100 MB storage</li>
                <li>✅ Basic analytics</li>
                <li>✅ Community support</li>
                <li>❌ Custom domains</li>
                <li>❌ Priority support</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.button("Current Plan", disabled=True, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(15, 118, 110, 0.15); border: 2px solid #0f766e; height: 400px;">
            <div style="background-color: #0f766e; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; display: inline-block; margin-bottom: 10px;">POPULAR</div>
            <h3 style="color: #1e293b; margin-bottom: 10px;">Pro</h3>
            <div style="font-size: 2rem; font-weight: bold; color: #0f766e; margin-bottom: 20px;">$29<span style="font-size: 1rem; color: #64748b;">/mo</span></div>
            <ul style="color: #64748b; font-size: 0.875rem; line-height: 2;">
                <li>✅ Up to 25 bots</li>
                <li>✅ 10 GB storage</li>
                <li>✅ Advanced analytics</li>
                <li>✅ Email support</li>
                <li>✅ Custom domains</li>
                <li>✅ API access</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Upgrade to Pro", type="primary", use_container_width=True):
            st.success("✅ Upgrade initiated! (Demo)")
    
    with col3:
        st.markdown("""
        <div style="background-color: white; padding: 25px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); height: 400px;">
            <h3 style="color: #1e293b; margin-bottom: 10px;">Enterprise</h3>
            <div style="font-size: 2rem; font-weight: bold; color: #0f766e; margin-bottom: 20px;">Custom</div>
            <ul style="color: #64748b; font-size: 0.875rem; line-height: 2;">
                <li>✅ Unlimited bots</li>
                <li>✅ Unlimited storage</li>
                <li>✅ White-label option</li>
                <li>✅ Dedicated support</li>
                <li>✅ Custom integrations</li>
                <li>✅ SLA guarantee</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Contact Sales", use_container_width=True):
            st.info("📧 Sales contact coming soon! (Demo)")
    
    st.markdown("<br/><br/>", unsafe_allow_html=True)
    
    st.markdown("#### Payment Method")
    
    st.markdown("""
    <div style="background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin: 20px 0;">
        <h4 style="color: #1e293b; margin-bottom: 15px;">💳 No payment method on file</h4>
        <p style="color: #64748b; font-size: 0.875rem;">Add a payment method to upgrade your plan</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("➕ Add Payment Method"):
        st.info("Payment integration coming soon! (Demo)")
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    st.markdown("#### Usage This Month")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <div style="color: #64748b; font-size: 0.875rem; margin-bottom: 5px;">Bots Created</div>
            <div style="font-size: 2rem; font-weight: bold; color: #0f766e;">0 / 3</div>
            <div style="background-color: #e2e8f0; height: 4px; border-radius: 2px; margin-top: 10px;">
                <div style="background-color: #0f766e; height: 100%; width: 0%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <div style="color: #64748b; font-size: 0.875rem; margin-bottom: 5px;">Storage Used</div>
            <div style="font-size: 2rem; font-weight: bold; color: #0f766e;">0 MB</div>
            <div style="background-color: #e2e8f0; height: 4px; border-radius: 2px; margin-top: 10px;">
                <div style="background-color: #0f766e; height: 100%; width: 0%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <div style="color: #64748b; font-size: 0.875rem; margin-bottom: 5px;">API Calls</div>
            <div style="font-size: 2rem; font-weight: bold; color: #0f766e;">0</div>
            <div style="background-color: #e2e8f0; height: 4px; border-radius: 2px; margin-top: 10px;">
                <div style="background-color: #0f766e; height: 100%; width: 0%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
