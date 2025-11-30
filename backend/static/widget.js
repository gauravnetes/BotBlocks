(function () {
    // 1. Get the bot ID from the script tag attributes
    const scriptTag = document.currentScript;
    const botId = scriptTag.getAttribute('data-bot-id');

    // ⚠️ IMPORTANT: Point this to your backend URL
    // For local dev, use http://localhost:8000/api/v1/chat/web
    const API_URL = "http://localhost:8000/api/v1/chat/web";

    // 2. Inject CSS styles dynamically
    const style = document.createElement('style');
    style.innerHTML = `
        .botblocks-widget { position: fixed; bottom: 20px; right: 20px; font-family: 'JetBrains Mono', 'Courier New', monospace; z-index: 9999; }
        
        /* Toggle Button */
        .botblocks-toggle { 
            background: #facc15; color: #18181b; width: 60px; height: 60px; 
            border-radius: 2px; cursor: pointer; display: flex; align-items: center; 
            justify-content: center; box-shadow: 4px 4px 0px #27272a; border: 1px solid #18181b;
            transition: transform 0.2s; 
        }
        .botblocks-toggle:hover { transform: translate(-2px, -2px); box-shadow: 6px 6px 0px #18181b; }
        .botblocks-toggle:active { transform: translate(2px, 2px); box-shadow: 0px 0px 0px #18181b; }
        
        /* Chat Window */
        .botblocks-chat-window { 
            display: none; width: 350px; height: 500px; background: #18181b; 
            border-radius: 2px; box-shadow: 0 5px 20px rgba(0,0,0,0.5); 
            flex-direction: column; overflow: hidden; margin-bottom: 20px; 
            border: 1px solid #27272a;
        }
        
        /* Header */
        .botblocks-header { 
            background: #18181b; color: #facc15; padding: 15px; font-weight: bold; 
            display: flex; justify-content: space-between; align-items: center; 
            border-bottom: 1px solid #27272a; letter-spacing: 0.05em;
        }
        
        /* Messages Area */
        .botblocks-messages { 
            flex: 1; padding: 15px; overflow-y: auto; background: #09090b; 
            display: flex; flex-direction: column; gap: 10px; 
        }
        
        /* Input Area */
        .botblocks-input-area { 
            padding: 15px; border-top: 1px solid #27272a; display: flex; gap: 10px; background: #18181b;
        }
        .botblocks-input { 
            flex: 1; padding: 10px; border: 1px solid #27272a; border-radius: 2px; outline: none; 
            background: #09090b; color: #fafafa; font-family: monospace;
        }
        .botblocks-input:focus { border-color: #facc15; }
        
        .botblocks-send { 
            background: #facc15; color: #18181b; border: 1px solid #facc15; padding: 10px 15px; 
            border-radius: 2px; cursor: pointer; font-weight: bold; font-family: monospace; text-transform: uppercase;
        }
        .botblocks-send:hover { background: #eab308; }
        
        /* Bubbles */
        .msg { max-width: 80%; padding: 10px 14px; border-radius: 2px; font-size: 14px; line-height: 1.4; }
        .msg.user { background: #27272a; color: #facc15; align-self: flex-end; border: 1px solid #facc15; }
        .msg.bot { background: #18181b; color: #fafafa; align-self: flex-start; border: 1px solid #27272a; }
        
        /* Loading Animation */
        .typing { font-style: italic; color: #71717a; font-size: 12px; margin-left: 10px; }
        
        /* Scrollbar */
        .botblocks-messages::-webkit-scrollbar { width: 8px; }
        .botblocks-messages::-webkit-scrollbar-track { background: #09090b; }
        .botblocks-messages::-webkit-scrollbar-thumb { background: #27272a; border: 1px solid #09090b; }
    `;
    document.head.appendChild(style);

    // 3. Create the Widget HTML
    const widgetContainer = document.createElement('div');
    widgetContainer.className = 'botblocks-widget';
    widgetContainer.innerHTML = `
        <div class="botblocks-chat-window" id="chat-window">
            <div class="botblocks-header">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <img src="http://localhost:8000/static/logo.png" alt="BotLogo" style="width: 24px; height: 24px;">
                    <span>BOTBLOCKS AI</span>
                </div>
                <span id="close-btn" class="close-icon" style="cursor: pointer;">✕</span>
            </div>
            
            <div class="botblocks-messages" id="messages-area">
                <div class="msg bot">
                    Hello! I am ready to assist.
                </div>
            </div>
            
            <div class="botblocks-input-area">
                <input type="text" class="botblocks-input" id="chat-input" placeholder="Type command...">
                <button class="botblocks-send" id="send-btn">SEND</button>
            </div>
        </div>

        <div class="botblocks-toggle" id="toggle-btn">
            <img src="http://localhost:8000/static/logo.png" style="width: 20px; height: 20px;"> 
        </div>
    `;
    document.body.appendChild(widgetContainer);

    // 4. Widget Logic (Open/Close/Send)
    const toggleBtn = document.getElementById('toggle-btn');
    const closeBtn = document.getElementById('close-btn');
    const chatWindow = document.getElementById('chat-window');
    const input = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const messagesArea = document.getElementById('messages-area');

    toggleBtn.addEventListener('click', () => {
        const isHidden = chatWindow.style.display === 'none' || chatWindow.style.display === '';
        chatWindow.style.display = isHidden ? 'flex' : 'none';
        if (isHidden) input.focus();
    });

    closeBtn.addEventListener('click', () => {
        chatWindow.style.display = 'none';
    });

    async function sendMessage() {
        const text = input.value.trim();
        if (!text) return;

        // User Message
        addMessage(text, 'user');
        input.value = '';

        // Loading State
        const loadingId = addMessage('Thinking...', 'bot typing');

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ bot_id: botId, message: text })
            });
            const data = await response.json();

            // Replace Loading with Answer
            document.getElementById(loadingId).remove();
            addMessage(data.response, 'bot');
        } catch (err) {
            document.getElementById(loadingId).remove();
            addMessage("Error connecting to server.", 'bot');
            console.error(err);
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    function addMessage(text, className) {
        const div = document.createElement('div');
        div.className = `msg ${className}`;
        div.textContent = text;
        div.id = 'msg-' + Date.now();
        messagesArea.appendChild(div);
        messagesArea.scrollTop = messagesArea.scrollHeight;
        return div.id;
    }
})();