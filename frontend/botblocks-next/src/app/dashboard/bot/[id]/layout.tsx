import { getBot } from "@/lib/api";
import { ArrowLeft } from "lucide-react";
import Link from "next/link";
import { BotNav } from "@/components/dashboard/BotNav";

interface BotLayoutProps {
    children: React.ReactNode;
    params: Promise<{ id: string }>;
}

export default async function BotLayout({ children, params }: BotLayoutProps) {
    const resolvedParams = await params;
    const bot = await getBot(resolvedParams.id);

    if (!bot) {
        return <div className="p-8 text-red-500">Bot not found</div>;
    }

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
                        {bot.bot_type === "persona" && (
                            <span className="text-xs bg-purple-500/10 text-purple-400 px-2 py-0.5 rounded border border-purple-500/20 uppercase font-bold">Persona</span>
                        )}
                        {bot.bot_type === "rag" && (
                            <span className="text-xs bg-amber-500/10 text-amber-400 px-2 py-0.5 rounded border border-amber-500/20 uppercase font-bold">RAG</span>
                        )}
                    </h1>
                    <p className="text-xs text-zinc-500 font-mono">ID: {bot.public_id}</p>
                </div>
            </div>

            {/* Navigation */}
            <BotNav bot={bot} />

            {/* Page Content */}
            <div className="animate-in fade-in duration-300">
                {children}
            </div>
        </div>
    );
}
