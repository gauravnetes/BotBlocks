"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { MessageSquare, Code, Settings, Palette, Book, BarChart3, LayoutDashboard } from "lucide-react";
import { Bot } from "@/lib/api";
import { toast } from "sonner";

interface BotNavProps {
    bot: Bot;
}

export function BotNav({ bot }: BotNavProps) {
    const pathname = usePathname();
    const baseUrl = `/dashboard/bot/${bot.public_id}`;

    const tabs = [
        { id: "overview", path: baseUrl, icon: LayoutDashboard, label: "Overview", exact: true },
        { id: "chat", path: `${baseUrl}/chat`, icon: MessageSquare, label: "Test Chat" },
        { id: "analytics", path: `${baseUrl}/analytics`, icon: BarChart3, label: "Analytics" },
        { id: "knowledge", path: `${baseUrl}/knowledge`, icon: Book, label: "Knowledge" },
        { id: "widget", path: `${baseUrl}/widget`, icon: Palette, label: "Widget Theme" },
        { id: "embed", path: `${baseUrl}/embed`, icon: Code, label: "Embed" },
        { id: "settings", path: `${baseUrl}/settings`, icon: Settings, label: "Settings" },
    ];

    return (
        <div className="flex gap-1 border-b border-white/5 mb-8 overflow-x-auto">
            {tabs.map((tab) => {
                const isActive = tab.exact
                    ? pathname === tab.path
                    : pathname?.startsWith(tab.path);

                return (
                    <Link
                        key={tab.id}
                        href={tab.id === "knowledge" && bot.bot_type !== "rag" ? "#" : tab.path}
                        onClick={(e) => {
                            if (tab.id === "knowledge" && bot.bot_type !== "rag") {
                                e.preventDefault();
                                toast.error("Access Denied", {
                                    description: "Knowledge Base is only available for Knowledge Bots (RAG).",
                                });
                            }
                        }}
                        className={`flex items-center gap-2 px-6 py-3 text-sm font-medium border-b-2 transition-colors whitespace-nowrap ${isActive
                                ? "border-blue-500 text-blue-500"
                                : "border-transparent text-zinc-400 hover:text-white"
                            } ${tab.id === "knowledge" && bot.bot_type !== "rag" ? "opacity-50 cursor-not-allowed" : ""
                            }`}
                    >
                        <tab.icon className="w-4 h-4" />
                        {tab.label}
                    </Link>
                );
            })}
        </div>
    );
}
