"use client";
import { useEffect, useState, useRef } from "react";
import { getBot, chatWithBot, Bot } from "@/lib/api";
import { ArrowLeft, MessageSquare, Code, Settings as SettingsIcon, Send, Copy, Check } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";
export default function BotDetailPage() {
  const params = useParams();
  const [bot, setBot] = useState<Bot | null>(null);
  const [activeTab, setActiveTab] = useState<"overview" | "chat" | "embed" | "settings">("overview");
  const [isLoading, setIsLoading] = useState(true);
  // Chat State
  const [messages, setMessages] = useState<{ role: "user" | "bot"; content: string }[]>([]);
  const [input, setInput] = useState("");
  const [isChatting, setIsChatting] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (params.id) {
      getBot(params.id as string)
        .then(setBot)
        .catch((err) => console.error(err))
        .finally(() => setIsLoading(false));
    }
  }, [params.id]);
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);
  const handleSend = async () => {
    if (!input.trim() || !bot) return;
    const userMsg = input;
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMsg }]);
    setIsChatting(true);
    try {
      const response = await chatWithBot(bot.public_id, userMsg);
      setMessages((prev) => [...prev, { role: "bot", content: response }]);
    } catch (error) {
      setMessages((prev) => [...prev, { role: "bot", content: "Error: Could not get response." }]);
    } finally {
      setIsChatting(false);
    }
  };
  if (isLoading) return <div className="p-8 text-zinc-400">Loading bot...</div>;
  if (!bot) return <div className="p-8 text-red-400">Bot not found</div>;
  return (
    <div>
      {/* Header */}
      <div className="flex items-center gap-4 mb-8">
        <Link href="/dashboard" className="p-2 hover:bg-white/5 rounded-lg transition-colors">
          <ArrowLeft className="w-5 h-5 text-zinc-400" />
        </Link>
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            🤖 {bot.name}
          </h1>
          <p className="text-xs text-zinc-500 font-mono">ID: {bot.public_id}</p>
        </div>
      </div>
      {/* Tabs */}
      <div className="flex gap-1 border-b border-white/5 mb-8">
        {[
          { id: "overview", icon: MessageSquare, label: "Overview" },
          { id: "chat", icon: MessageSquare, label: "Test Chat" },
          { id: "embed", icon: Code, label: "Embed" },
          { id: "settings", icon: SettingsIcon, label: "Settings" },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`flex items-center gap-2 px-6 py-3 text-sm font-medium border-b-2 transition-colors ${
              activeTab === tab.id
                ? "border-blue-500 text-blue-500"
                : "border-transparent text-zinc-400 hover:text-white"
            }`}
          >
            <tab.icon className="w-4 h-4" />
            {tab.label}
          </button>
        ))}
      </div>
      {/* Content */}
      <div className="animate-in fade-in duration-300">
        
        {/* OVERVIEW */}
        {activeTab === "overview" && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-zinc-900 border border-white/5 rounded-xl p-6">
              <h3 className="text-zinc-400 text-sm font-bold uppercase mb-4">Status</h3>
              <span className="bg-green-500/10 text-green-500 px-3 py-1 rounded-full text-sm font-bold">
                ACTIVE
              </span>
            </div>
            <div className="bg-zinc-900 border border-white/5 rounded-xl p-6">
              <h3 className="text-zinc-400 text-sm font-bold uppercase mb-4">Platform</h3>
              <span className="text-white text-lg font-medium">
                {bot.platform?.toUpperCase() || "WEB"}
              </span>
            </div>
            <div className="col-span-full bg-zinc-900 border border-white/5 rounded-xl p-6">
              <h3 className="text-zinc-400 text-sm font-bold uppercase mb-4">System Prompt</h3>
              <p className="text-zinc-300 font-mono text-sm bg-black/20 p-4 rounded-lg">
                {bot.system_prompt || "No prompt configured."}
              </p>
            </div>
          </div>
        )}
        {/* CHAT */}
        {activeTab === "chat" && (
          <div className="max-w-3xl mx-auto bg-zinc-900 border border-white/5 rounded-xl overflow-hidden flex flex-col h-[600px]">
            <div ref={scrollRef} className="flex-1 overflow-y-auto p-6 space-y-4">
              {messages.length === 0 && (
                <div className="text-center text-zinc-500 mt-20">
                  <MessageSquare className="w-12 h-12 mx-auto mb-4 opacity-20" />
                  <p>Start a conversation with your bot!</p>
                </div>
              )}
              {messages.map((msg, i) => (
                <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                  <div className={`max-w-[80%] p-4 rounded-2xl ${
                    msg.role === "user" 
                      ? "bg-blue-600 text-white rounded-tr-sm" 
                      : "bg-white/5 text-zinc-200 rounded-tl-sm"
                  }`}>
                    {msg.content}
                  </div>
                </div>
              ))}
              {isChatting && (
                <div className="flex justify-start">
                  <div className="bg-white/5 text-zinc-400 px-4 py-2 rounded-full text-sm animate-pulse">
                    Thinking...
                  </div>
                </div>
              )}
            </div>
            <div className="p-4 border-t border-white/5 bg-zinc-950/50">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleSend()}
                  placeholder="Type a message..."
                  className="flex-1 bg-zinc-800 border-transparent rounded-lg px-4 focus:ring-2 focus:ring-blue-500 focus:outline-none text-white"
                />
                <button 
                  onClick={handleSend}
                  disabled={isChatting || !input.trim()}
                  className="bg-blue-600 p-3 rounded-lg text-white hover:bg-blue-500 disabled:opacity-50"
                >
                  <Send className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>
        )}
        {/* EMBED */}
        {activeTab === "embed" && (
          <div className="space-y-6">
            <div className="bg-zinc-900 border border-white/5 rounded-xl p-6">
              <h3 className="text-white font-bold mb-4">HTML Embed Code</h3>
              <p className="text-zinc-400 text-sm mb-4">
                Copy and paste this code into your website&apos;s <code className="text-blue-400">&lt;body&gt;</code> tag.
              </p>
              <div className="relative group">
                <pre className="bg-black/50 p-4 rounded-lg text-sm text-zinc-300 overflow-x-auto font-mono">
                  {`<script 
  src="http://localhost:8000/static/widget.js" 
  data-bot-id="${bot.public_id}" 
  defer>
</script>`}
                </pre>
                <button 
                  onClick={() => navigator.clipboard.writeText(`<script src="http://localhost:8000/static/widget.js" data-bot-id="${bot.public_id}" defer></script>`)}
                  className="absolute top-2 right-2 bg-white/10 p-2 rounded hover:bg-white/20 text-white opacity-0 group-hover:opacity-100 transition-opacity"
                >
                  <Copy className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        )}
        {/* SETTINGS */}
        {activeTab === "settings" && (
          <div className="bg-zinc-900 border border-white/5 rounded-xl p-6">
            <h3 className="text-white font-bold mb-4">Bot Configuration</h3>
            <p className="text-zinc-500 text-sm mb-4">Update your bot&apos;s personality and behavior.</p>
            <textarea 
              className="w-full bg-black/20 border border-white/10 rounded-lg p-4 text-white font-mono text-sm h-40 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              defaultValue={bot.system_prompt}
            />
            <div className="mt-4 flex justify-end">
              <button className="bg-white text-black px-6 py-2 rounded-lg font-medium hover:bg-zinc-200">
                Save Changes
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}