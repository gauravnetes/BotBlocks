# 🤖 BotBlocks - WordPress for Chatbots

Build intelligent chatbots in minutes with BotBlocks - a complete Streamlit-based frontend for creating, managing, and deploying AI-powered chatbots across multiple platforms.

## ✨ Features

- **🧙 Multi-Step Bot Wizard**: Intuitive wizard interface for creating bots step-by-step
- **📚 Knowledge-Powered RAG**: Upload PDFs, documents, URLs, or raw text for your bot to learn from
- **🎨 Custom Personas**: Pre-built personalities (Friendly, Professional, Witty, Energetic) or custom prompts
- **🌐 Multi-Platform Deploy**: Deploy to Website, Telegram, and Discord from one dashboard
- **💬 Test Chat Interface**: Real-time chat testing with source citations
- **🔗 Embed Widget Generator**: Auto-generated HTML/JS snippets for website integration
- **📊 Admin Analytics**: Usage metrics, bot statistics, and activity monitoring
- **⚙️ Settings Management**: API key storage, account settings, and billing (placeholder)
- **🎯 Demo Mode**: Works standalone with local fallback when backend is unavailable

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- (Optional) BotBlocks backend API running

### Installation

1. **Clone or download this repository**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment** (optional):
```bash
cp .env.example .env
# Edit .env to set BOTBLOCKS_BACKEND if needed
```

4. **Run the application**:
```bash
streamlit run app.py --server.port 5000
```

5. **Open your browser**:
Navigate to `http://localhost:5000`

## 📁 Project Structure

```
.
├── app.py                          # Main Streamlit application entry point
├── botblocks_app/                  # Application package
│   ├── utils.py                    # API wrappers, validation, demo mode
│   ├── styles.css                  # Custom CSS (navy/teal theme)
│   ├── components/
│   │   └── ui.py                   # Reusable UI components
│   └── pages/
│       ├── landing.py              # Landing/marketing page
│       ├── wizard.py               # Multi-step bot creation wizard
│       ├── dashboard.py            # Bot management dashboard
│       ├── bot_detail.py           # Bot detail, test chat, embed code
│       ├── admin.py                # Analytics and usage stats
│       └── settings.py             # Settings and configuration
├── .streamlit/
│   └── config.toml                 # Streamlit server configuration
├── assets/                         # Static assets (icons, images)
├── .env.example                    # Environment variables template
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── Procfile                        # Deployment configuration
```

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BOTBLOCKS_BACKEND` | `http://localhost:8000` | Backend API URL |
| `OPENAI_API_KEY` | - | (Optional) OpenAI API key for advanced features |

### Backend API Contract

The frontend expects the following API endpoints:

#### Bot Management
- `POST /api/v1/bots/create` - Create a new bot
- `GET /api/v1/bots` - List all bots
- `GET /api/v1/bots/{public_id}` - Get bot details

#### Knowledge & Indexing
- `POST /api/v1/bots/{public_id}/documents` - Upload documents (multipart or JSON)
- `POST /api/v1/bots/{public_id}/index` - Trigger knowledge indexing

#### Configuration
- `POST /api/v1/bots/{public_id}/persona` - Set bot persona/system prompt
- `POST /api/v1/bots/{public_id}/platform` - Configure platform credentials
- `POST /api/v1/bots/{public_id}/blocks` - Add/configure blocks

#### Chat
- `POST /api/v1/bots/{public_id}/chat` - Send chat message and get response

See the detailed API contract in the specification document for request/response schemas.

## 🎨 User Workflow

### 1. Create a Bot (Wizard)

1. **Welcome** - Introduction and draft loading
2. **Name** - Set bot name and description
3. **Job Type** - Choose RAG (knowledge-based) or Non-RAG (persona-only)
4. **Knowledge** (RAG only) - Upload files, provide URLs, or paste text
5. **Persona** - Select pre-built personality or create custom
6. **Platform** - Choose Website, Telegram, and/or Discord
7. **Platform Details** - Enter tokens/credentials for selected platforms
8. **Review & Build** - Review configuration and build bot

### 2. Manage Bots (Dashboard)

- View all created bots in card layout
- See status, platform, document count
- Quick actions: View, Test Chat, Re-index
- Filter and search (coming soon)

### 3. Test & Deploy (Bot Detail)

- **Overview Tab**: Bot information and actions
- **Test Chat Tab**: Real-time chat with source citations
- **Embed Widget Tab**: Copy HTML/JS code for website integration
- **Configuration Tab**: Update system prompt and view stats

### 4. Monitor (Admin)

- Total bots, active bots, documents uploaded
- Platform distribution charts
- Recent activity and bot list
- System status and API connection info

### 5. Configure (Settings)

- **API Keys**: Backend URL, platform tokens
- **Account**: Profile information, security settings
- **Billing**: Plan comparison and usage metrics (placeholder)

## 🧪 Demo Mode & Testing

### Demo Mode

When the backend is unavailable, the app automatically enters **Demo Mode**:

- ✅ All UI features work
- ✅ Bots created and stored in-memory
- ✅ Wizard flow completes successfully
- ✅ Chat interface returns demo responses
- ⚠️ Data is lost on page refresh
- ℹ️ Demo mode indicator shown in sidebar and relevant pages

Perfect for testing the frontend without backend infrastructure!

### Quick Testing Checklist

**To test with live backend:**
1. Set `BOTBLOCKS_BACKEND` environment variable to your backend URL
2. Ensure backend is running and accessible
3. Check sidebar for "🟢 Connected" status
4. Create a bot through the wizard
5. Test chat functionality with real responses

**To test in demo mode:**
1. Leave `BOTBLOCKS_BACKEND` unset or point to non-existent URL
2. Check sidebar for "🟡 Demo Mode" status
3. Create bots - they'll be stored in memory
4. All features work with simulated responses
5. Note: Data clears on page refresh

**Smoke Test:**
- ✅ Navigate all pages without errors
- ✅ Create bot via wizard (all 8 steps)
- ✅ View bot in dashboard
- ✅ Test chat interface
- ✅ Generate embed code
- ✅ View admin analytics

## 📦 Deployment

### Streamlit Community Cloud

1. Push code to GitHub repository
2. Connect to [share.streamlit.io](https://share.streamlit.io)
3. Set `BOTBLOCKS_BACKEND` in Secrets management
4. Deploy!

### Replit

1. Import project to Replit
2. Set environment variable `BOTBLOCKS_BACKEND`
3. Run command: `streamlit run app.py --server.port 5000`
4. Use built-in Replit deployment

### Heroku / Custom Server

Use the included `Procfile`:

```bash
# Install dependencies
pip install -r requirements.txt

# Run with Procfile
web: streamlit run app.py --server.port $PORT
```

Set environment variables in your hosting platform dashboard.

## 🔐 Security Notes

- **Never commit secrets**: Use environment variables for API keys
- **Token visibility**: Sensitive inputs have show/hide toggles
- **Local storage**: Draft data saved to `/tmp/botblocks_draft.json`
- **Session-based**: API keys stored in session state (not persisted)

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Use a different port
streamlit run app.py --server.port 8501
```

### Backend Connection Failed
- Check `BOTBLOCKS_BACKEND` environment variable
- Verify backend is running and accessible
- App will enter demo mode automatically

### Styling Issues
- Clear browser cache
- Check `.streamlit/config.toml` is present
- Verify CSS is loading in `streamlit/styles.css`

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 📚 Documentation

### API Wrapper Functions (streamlit/utils.py)

```python
# GET request
response = api_get("/bots/{public_id}")

# POST JSON
response = api_post_json("/bots/create", {"name": "My Bot"})

# POST Multipart (file upload)
files = {"file": (filename, fileobj, content_type)}
response = api_post_multipart("/bots/{id}/documents", files=files)
```

### UI Components (streamlit/components/ui.py)

```python
# Render chat bubble
render_chat_bubble("Hello!", is_user=True)

# Progress bar
render_progress_bar(current_step=3, total_steps=7, step_names=[...])

# Code snippet with copy button
render_code_snippet(code, language="html", title="Embed Code")
```

## 🎯 Future Enhancements

- [ ] Real user authentication (OAuth)
- [ ] Conversation history and analytics
- [ ] Advanced bot analytics dashboard
- [ ] Multi-bot comparison
- [ ] A/B testing for personas
- [ ] Export/import bot configurations
- [ ] Template marketplace
- [ ] Real-time collaboration
- [ ] Webhook integrations
- [ ] Custom branding/white-label

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 💬 Support

- 📧 Email: support@botblocks.io
- 💬 Discord: [Join our community](#)
- 🐛 Issues: [GitHub Issues](#)
- 📚 Docs: [Full documentation](#)

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- Icons from Emoji
- Design inspired by modern SaaS platforms

---

**Made with ❤️ by the BotBlocks team**

🤖 WordPress for Chatbots - Build, Deploy, Manage
