# 🤖 BotBlocks

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

> **The WordPress for Chatbots** - Build production-ready AI chatbots in 60 seconds, no coding required.

BotBlocks is a modular, low-code chatbot builder that lets non-developers create sophisticated AI-powered chatbots by simply selecting pre-built functional blocks. Think of it as assembling LEGO blocks instead of writing code.

## 🎯 The Problem

Existing chatbot platforms fall into two extremes:
- **Complex Flow Builders** (like Botpress, Voiceflow) - Powerful but require learning curves with nodes, intents, and entities
- **Simple One-Trick Tools** (like Chatbase, Dante AI) - Easy but limited to basic Q&A functionality

**BotBlocks sits in the sweet spot** - offering modular functionality without the complexity.

## ✨ What Makes BotBlocks Unique

### 1. **Block Assembler, Not Flow Builder**
Instead of dragging nodes and connecting logic flows, users simply check boxes:
- ☑️ Knowledge Base Q&A
- ☑️ Lead Capture
- ☑️ Customer Support
- ☑️ Human Handoff

BotBlocks automatically stitches these blocks together in the backend.

### 2. **Persona-First Design**
Choose your bot's personality upfront:
- 😊 Friendly & Casual
- 💼 Professional & Formal
- 😏 Witty & Sarcastic

No need to craft complex prompts - we handle the system engineering.

### 3. **Built for the 80% Use Case**
Focus on speed and simplicity for common scenarios, not attempting to be everything to everyone.

## 🚀 Features

### Core Components

#### 🤖 Bot Functions
- **General Q&A Bot** - Answers based on your knowledge base using RAG (Retrieval-Augmented Generation)
- **Lead Generation Bot** - Captures user information with customizable fields
- **Customer Support Bot** - Hybrid Q&A with intelligent human handoff
- **Custom Workflows** - Combine multiple blocks for complex scenarios

#### 📚 Knowledge Base Options
- **File Upload** - PDF, TXT, MD, DOCX support
- **Website Scraping** - Extract content from any URL
- **Manual Entry** - Direct text input for Q&A pairs
- **Multi-Source** - Combine different data sources

#### 🎨 Bot Personas
Pre-configured personality templates that automatically adjust:
- Tone and language style
- Response formatting
- Emoji usage
- Formality level

#### 🔌 Platform Integration
- **Telegram** - Fast deployment with webhook support
- **Discord** - Server and DM bot capabilities
- **Web Widget** - Embeddable chat interface for websites
- **API Endpoint** - RESTful API for custom integrations

## 🏗️ Architecture

```
┌─────────────────┐
│   Frontend UI   │ ← User configures bot (Streamlit/Gradio)
│  (The Builder)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Backend API    │ ← Processes config & manages data
│ (Control Plane) │    (FastAPI/Flask)
└────────┬────────┘
         │
         ├─────────────────┐
         ▼                 ▼
┌─────────────────┐  ┌──────────────┐
│  Vector Store   │  │  Bot Engine  │ ← Handles responses
│   (ChromaDB)    │  │ (LangChain)  │    (RAG + LLM)
└─────────────────┘  └──────┬───────┘
                            │
                            ▼
                     ┌──────────────┐
                     │ LLM API      │
                     │ (Gemini/GPT) │
                     └──────────────┘
```

## 🛠️ Tech Stack

| Layer | Technology | Why? |
|-------|-----------|------|
| **Frontend** | Streamlit/Gradio | Rapid Python-based UI development |
| **Backend** | FastAPI | High-performance async API |
| **Vector DB** | ChromaDB | Zero-config, file-based storage |
| **RAG Framework** | LangChain/LlamaIndex | Production-ready RAG pipeline |
| **LLM** | Gemini/OpenAI API | State-of-the-art language models |
| **Embeddings** | text-embedding-ada-002 | Semantic search capability |

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip or conda
- API keys (OpenAI/Gemini)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/gauravnetes/BotBlocks.git
cd BotBlocks

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the application
streamlit run app.py
```

## 🎮 Usage

### Creating Your First Bot (60 Seconds)

1. **Choose Bot Function**
   - Select "General Q&A Bot" for your first bot

2. **Upload Knowledge Base**
   - Drag and drop a PDF file (e.g., your product manual)
   - Or paste a website URL to scrape

3. **Select Persona**
   - Choose "Friendly & Casual" from the dropdown

4. **Pick Platform**
   - Select "Telegram" for instant deployment
   - Paste your Telegram Bot Token

5. **Deploy**
   - Click "Create Bot" and you're live!

### Example Use Cases

**Small Business Owner**
```
Function: Customer Support Bot
Knowledge: FAQ PDF + Website
Persona: Professional
Platform: Web Widget
Result: 24/7 automated support on website
```

**Event Organizer**
```
Function: Lead Generation Bot
Knowledge: Event details document
Persona: Friendly & Casual
Platform: Telegram
Result: Automated attendee registration
```

**Content Creator**
```
Function: Q&A Bot
Knowledge: All blog posts (scraped)
Persona: Witty & Sarcastic
Platform: Discord
Result: Interactive community assistant
```

## 🧪 Development

### Project Structure
```
BotBlocks/
├── app.py                 # Main Streamlit application
├── backend/
│   ├── api.py            # FastAPI endpoints
│   ├── rag_engine.py     # RAG logic
│   └── data_processor.py # Document chunking & embedding
├── bots/
│   ├── telegram_bot.py   # Telegram integration
│   ├── discord_bot.py    # Discord integration
│   └── web_widget.py     # Web embed code
├── models/
│   └── personas.py       # Persona configurations
├── vector_store/         # ChromaDB storage
└── requirements.txt
```

### Adding a New Block Type

```python
# In backend/blocks.py

class CustomBlock(BaseBlock):
    def __init__(self, config):
        self.config = config
    
    async def process(self, message, context):
        # Your block logic here
        return response
```

### Testing

```bash
# Run unit tests
pytest tests/

# Run integration tests
pytest tests/integration/

# Test a specific bot function
python -m tests.test_qa_bot
```

## 🎯 Roadmap

### Phase 1: MVP (Current)
- [x] Basic RAG implementation
- [x] Telegram integration
- [x] Three core personas
- [x] PDF upload support

### Phase 2: Enhancement
- [ ] Discord integration
- [ ] Web widget with customization
- [ ] Advanced lead capture forms
- [ ] Analytics dashboard

### Phase 3: Advanced Features
- [ ] Multi-language support
- [ ] Voice bot capability
- [ ] Integration marketplace (Calendly, Stripe, etc.)
- [ ] A/B testing for personas
- [ ] Conversation analytics

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Contribution Ideas
- Add new platform integrations (WhatsApp, Slack, MS Teams)
- Create additional persona templates
- Improve RAG accuracy with better chunking strategies
- Build a block for appointment booking
- Add multi-language support

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for hackathons, by hackathon enthusiasts
- Inspired by the simplicity of WordPress
- Powered by the open-source AI community

## 📧 Contact

**Gaurav** - [@gauravnetes](https://github.com/gauravnetes)

Project Link: [https://github.com/gauravnetes/BotBlocks](https://github.com/gauravnetes/BotBlocks)

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ for the no-code revolution

</div>
