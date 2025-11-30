(function() {
    // 1. Get the bot ID from the script tag attributes
    const scriptTag = document.currentScript;
    const botId = scriptTag.getAttribute('data-bot-id');
    
    // ⚠️ IMPORTANT: Point this to your backend URL
    // For local dev, use http://localhost:8000/api/v1/chat/web
    const API_URL = "http://localhost:8000/api/v1/chat/web"; 

    // 2. Inject CSS styles dynamically
    const style = document.createElement('style');
    style.innerHTML = `
        .botblocks-widget { position: fixed; bottom: 20px; right: 20px; font-family: 'Segoe UI', sans-serif; z-index: 9999; }
        
        /* Toggle Button */
        .botblocks-toggle { 
            background: #0f766e; color: #fff; width: 60px; height: 60px; 
            border-radius: 50%; cursor: pointer; display: flex; align-items: center; 
            justify-content: center; box-shadow: 0 4px 12px rgba(0,0,0,0.15); 
            transition: transform 0.3s; 
        }
        .botblocks-toggle:hover { transform: scale(1.1); }
        
        /* Chat Window */
        .botblocks-chat-window { 
            display: none; width: 350px; height: 500px; background: #fff; 
            border-radius: 12px; box-shadow: 0 5px 20px rgba(0,0,0,0.2); 
            flex-direction: column; overflow: hidden; margin-bottom: 20px; 
            border: 1px solid #e2e8f0;
        }
        
        /* Header */
        .botblocks-header { 
            background: #0f766e; color: #fff; padding: 15px; font-weight: bold; 
            display: flex; justify-content: space-between; align-items: center; 
        }
        
        /* Messages Area */
        .botblocks-messages { 
            flex: 1; padding: 15px; overflow-y: auto; background: #f8fafc; 
            display: flex; flex-direction: column; gap: 10px; 
        }
        
        /* Input Area */
        .botblocks-input-area { 
            padding: 15px; border-top: 1px solid #eee; display: flex; gap: 10px; background: white;
        }
        .botblocks-input { 
            flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 6px; outline: none; 
        }
        .botblocks-send { 
            background: #0f766e; color: #fff; border: none; padding: 10px 15px; 
            border-radius: 6px; cursor: pointer; font-weight: bold;
        }
        
        /* Bubbles */
        .msg { max-width: 80%; padding: 10px 14px; border-radius: 10px; font-size: 14px; line-height: 1.4; }
        .msg.user { background: #0f766e; color: #fff; align-self: flex-end; border-bottom-right-radius: 2px; }
        .msg.bot { background: #e2e8f0; color: #1e293b; align-self: flex-start; border-bottom-left-radius: 2px; }
        
        /* Loading Animation */
        .typing { font-style: italic; color: #94a3b8; font-size: 12px; margin-left: 10px; }
    `;
    document.head.appendChild(style);

    // 3. Create the Widget HTML
    const widgetContainer = document.createElement('div');
    widgetContainer.className = 'botblocks-widget';
    widgetContainer.innerHTML = `
        <div class="botblocks-chat-window" id="chat-window">
            <div class="botblocks-header">
                <span>AI Assistant</span>
                <span style="cursor:pointer; font-size: 18px;" id="close-btn">✕</span>
            </div>
            <div class="botblocks-messages" id="messages-area">
                <div class="msg bot">Hello! I can answer questions about the project report.</div>
            </div>
            <div class="botblocks-input-area">
                <input type="text" class="botblocks-input" id="chat-input" placeholder="Ask a question...">
                <button class="botblocks-send" id="send-btn">Send</button>
            </div>
        </div>
        <div class="botblocks-toggle" id="toggle-btn">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
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