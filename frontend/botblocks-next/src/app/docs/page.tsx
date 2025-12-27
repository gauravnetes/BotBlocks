import Link from "next/link";
import { ArrowRight, Layers, Zap, MessageSquare } from "lucide-react";

export default function DocsIntroPage() {
    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            <div className="border-b border-white/5 pb-10">
                <h1 className="text-4xl md:text-5xl font-black mb-6 tracking-tight">Introduction</h1>
                <p className="text-xl text-zinc-400 leading-relaxed">
                    Welcome to the <strong>BotBlocks</strong> documentation. Learn how to build, train, and deploy intelligent AI agents that understand your business and engage your customers.
                </p>
            </div>

            <div className="prose prose-invert prose-lg max-w-none text-zinc-300">
                <p>
                    BotBlocks is an all-in-one platform for creating custom AI chatbots. We leverage the power of advanced Large Language Models (LLMs) and Vector Databases to provide accurate, context-aware responses based on your own data.
                </p>

                <h3>Why BotBlocks?</h3>
                <ul className="grid grid-cols-1 md:grid-cols-2 gap-4 list-none pl-0">
                    <li className="bg-zinc-900/50 p-4 rounded-xl border border-white/5">
                        <strong className="text-white flex items-center gap-2 mb-2"><Zap className="w-4 h-4 text-yellow-400" /> unmatched Speed</strong>
                        Setup your first bot in minutes, not days. No complex decision trees or coding required.
                    </li>
                    <li className="bg-zinc-900/50 p-4 rounded-xl border border-white/5">
                        <strong className="text-white flex items-center gap-2 mb-2"><Layers className="w-4 h-4 text-blue-400" /> Easy Training</strong>
                        Simply upload a PDF or enter a website URL. We handle the chunking, embedding, and retrieval.
                    </li>
                    <li className="bg-zinc-900/50 p-4 rounded-xl border border-white/5">
                        <strong className="text-white flex items-center gap-2 mb-2"><MessageSquare className="w-4 h-4 text-green-400" /> Natural Chat</strong>
                        Our bots speak naturally in multiple languages, maintaining context throughout the conversation.
                    </li>
                </ul>

                <h3>Next Steps</h3>
                <p>
                    Ready to build? Follow our guides to get started.
                </p>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 not-prose mt-8">
                    <Link href="/docs/quick-start" className="group p-6 bg-indigo-600 hover:bg-indigo-500 rounded-xl transition-all flex items-center justify-between">
                        <div>
                            <h4 className="font-bold text-white text-lg">Quick Start Guide</h4>
                            <p className="text-indigo-200 text-sm mt-1">Deploy in 5 mins</p>
                        </div>
                        <ArrowRight className="w-6 h-6 text-white group-hover:translate-x-1 transition-transform" />
                    </Link>
                    <Link href="/docs/training" className="group p-6 bg-zinc-900 hover:bg-zinc-800 border border-white/10 rounded-xl transition-all flex items-center justify-between">
                        <div>
                            <h4 className="font-bold text-white text-lg">Training Your Bot</h4>
                            <p className="text-zinc-400 text-sm mt-1">Learn about RAG</p>
                        </div>
                        <ArrowRight className="w-6 h-6 text-zinc-400 group-hover:translate-x-1 transition-transform" />
                    </Link>
                </div>
            </div>
        </div>
    );
}
