(function () {
  const scriptTag = document.currentScript;
  const botId = scriptTag.getAttribute("data-bot-id");

  const scriptSrc = scriptTag.getAttribute("src");
  const baseUrl = scriptSrc.substring(0, scriptSrc.indexOf("/static"));
  const API_URL = `${baseUrl}/api/v1`;

  async function initWidget() {
    try {
      const res = await fetch(`${API_URL}/bots/${botId}/config`);
      if (!res.ok) throw new Error("Bot config not found");
      const config = await res.json();
      renderWidget(config);
    } catch (err) {
      console.error("BotBlocks Widget Error:", err);
      renderWidget({});
    }
  }

  function renderWidget(config) {
    const botName = config.bot_name || "AI Assistant";
    const avatar = config.bot_avatar || "🤖";
    const initialMsg =
      config.initial_message || "Hello! How can I help you?";

    const style = document.createElement("style");
    style.innerHTML = `
      .botblocks-widget {
        position: fixed;
        bottom: 20px;
        right: 20px;
        font-family: "JetBrains Mono", monospace;
        z-index: 9999;
      }

      .botblocks-toggle {
        background: #facc15;
        color: #18181b;
        width: 50px;
        height: 50px;
        border-radius: 2px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 4px 4px 0px #27272a;
        border: 1px solid #18181b;
        transition: transform 0.2s;
      }

      .botblocks-toggle:hover {
        transform: translate(-2px, -2px);
        box-shadow: 6px 6px 0px #18181b;
      }

      .botblocks-chat-window {
        display: none;
        width: 350px;
        height: 500px;
        background: #18181b;
        border: 1px solid #27272a;
        flex-direction: column;
        margin-bottom: 15px;
      }

      .botblocks-header {
        padding: 12px;
        color: #facc15;
        border-bottom: 1px solid #27272a;
        display: flex;
        justify-content: space-between;
        align-items: center;
      }

      .botblocks-messages {
        flex: 1;
        padding: 12px;
        background: #09090b;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 10px;
      }

      .botblocks-input-area {
        display: flex;
        gap: 8px;
        padding: 10px;
        border-top: 1px solid #27272a;
      }

      .botblocks-input {
        flex: 1;
        background: #09090b;
        color: #fafafa;
        border: 1px solid #27272a;
        padding: 8px;
        font-family: monospace;
      }

      .botblocks-send {
        background: #facc15;
        color: #18181b;
        border: none;
        padding: 8px 12px;
        cursor: pointer;
        font-weight: bold;
      }

      .msg {
        max-width: 80%;
        padding: 8px 10px;
        font-size: 13px;
        border: 1px solid #27272a;
      }

      .msg.user {
        align-self: flex-end;
        color: #facc15;
      }

      .msg.bot {
        align-self: flex-start;
        color: #fafafa;
      }
    `;
    document.head.appendChild(style);

    const container = document.createElement("div");
    container.className = "botblocks-widget";
    container.innerHTML = `
      <div class="botblocks-chat-window" id="chat-window">
        <div class="botblocks-header">
          <span>${avatar} ${botName}</span>
          <span id="close-btn" style="cursor:pointer">✕</span>
        </div>
        <div class="botblocks-messages" id="messages-area">
          <div class="msg bot">${initialMsg}</div>
        </div>
        <div class="botblocks-input-area">
          <input id="chat-input" class="botblocks-input" placeholder="Ask something..." />
          <button id="send-btn" class="botblocks-send">Send</button>
        </div>
      </div>

      <div class="botblocks-toggle" id="toggle-btn">
        <img src="${baseUrl}/static/logo.png" width="28" />
      </div>
    `;

    document.body.appendChild(container);
    attachLogic(API_URL, botId);
  }

  function attachLogic(apiUrl, botId) {
    const toggleBtn = document.getElementById("toggle-btn");
    const closeBtn = document.getElementById("close-btn");
    const chatWindow = document.getElementById("chat-window");
    const input = document.getElementById("chat-input");
    const sendBtn = document.getElementById("send-btn");
    const messages = document.getElementById("messages-area");

    toggleBtn.onclick = () => {
      chatWindow.style.display =
        chatWindow.style.display === "flex" ? "none" : "flex";
      input.focus();
    };

    closeBtn.onclick = () => (chatWindow.style.display = "none");

    sendBtn.onclick = sendMessage;
    input.onkeypress = (e) => e.key === "Enter" && sendMessage();

    async function sendMessage() {
      const text = input.value.trim();
      if (!text) return;
      add(text, "user");
      input.value = "";

      const loading = add("Thinking...", "bot");

      try {
        const res = await fetch(`${apiUrl}/chat/web`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ bot_id: botId, message: text }),
        });
        const data = await res.json();
        loading.remove();
        add(data.response, "bot");
      } catch {
        loading.remove();
        add("Connection error", "bot");
      }
    }

    function add(text, type) {
      const div = document.createElement("div");
      div.className = `msg ${type}`;
      div.textContent = text;
      messages.appendChild(div);
      messages.scrollTop = messages.scrollHeight;
      return div;
    }
  }

  initWidget();
})();
