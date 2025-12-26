"use client";

import { useState, useRef, useEffect } from "react";
import { chatWithBot, Bot, getBot } from "@/lib/api";
import { MessageSquare, Send } from "lucide-react";
import { useParams } from "next/navigation";

export default function ChatPage() {
    const params = useParams();
    const [messages, setMessages] = useState<{ role: "user" | "bot"; content: string }[]>([]);
    const [input, setInput] = useState("");
    const [isChatting, setIsChatting] = useState(false);
    const scrollRef = useRef<HTMLDivElement>(null);
    const [botId, setBotId] = useState<string>("");

    useEffect(() => {
        if (params.id) {
            setBotId(params.id as string);
        }
    }, [params.id]);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim() || !botId) return;
        const userMsg = input;
        setInput("");
        setMessages((prev) => [...prev, { role: "user", content: userMsg }]);
        setIsChatting(true);
        try {
            const response = await chatWithBot(botId, userMsg);
            setMessages((prev) => [...prev, { role: "bot", content: response }]);
        } catch (error) {
            setMessages((prev) => [...prev, { role: "bot", content: "Error: Could not get response." }]);
        } finally {
            setIsChatting(false);
        }
    };

    return (
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
                        <div className={`max-w-[80%] p-4 rounded-2xl ${msg.role === "user"
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
    );
}
