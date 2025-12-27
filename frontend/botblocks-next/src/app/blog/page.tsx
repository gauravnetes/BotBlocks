"use client";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import Link from "next/link";
import { Calendar, User, ArrowRight } from "lucide-react";

const BLOG_POSTS = [
    {
        title: "The Future of AI Chatbots in 2025",
        excerpt: "How Large Language Models are transforming customer support and what to expect in the coming years.",
        date: "Dec 15, 2024",
        author: "Souvik Rahut",
        category: "AI Trends",
        slug: "future-of-ai-chatbots"
    },
    {
        title: "Building Context-Aware Agents",
        excerpt: "A deep dive into RAG (Retrieval-Augmented Generation) and how BotBlocks fetches the right data.",
        date: "Nov 28, 2024",
        author: "Team BotBlocks",
        category: "Engineering",
        slug: "building-context-aware-agents"
    },
    {
        title: "Optimizing Your Bot for Sales",
        excerpt: "Tips and tricks to train your chatbot to convert visitors into paying customers effectively.",
        date: "Nov 10, 2024",
        author: "Sarah J.",
        category: "Guides",
        slug: "optimizing-bot-for-sales"
    }
];

export default function BlogPage() {
    return (
        <main className="min-h-screen bg-zinc-950 text-white selection:bg-indigo-500/30">
            <Navbar />

            <div className="pt-32 pb-20 px-6">
                <div className="container mx-auto max-w-6xl">
                    <div className="text-center max-w-3xl mx-auto mb-20">
                        <span className="inline-block px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-bold uppercase tracking-wider mb-4">
                            The Blog
                        </span>
                        <h1 className="text-4xl md:text-5xl font-black tracking-tight mb-6">
                            Latest from BotBlocks
                        </h1>
                        <p className="text-lg text-zinc-400">
                            Insights, updates, and guides from the team.
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        {BLOG_POSTS.map((post, i) => (
                            <Link
                                key={i}
                                href="#"
                                className="group flex flex-col bg-zinc-900 border border-white/5 rounded-2xl overflow-hidden hover:border-indigo-500/30 transition-all hover:-translate-y-1"
                            >
                                <div className="aspect-video bg-zinc-800 relative overflow-hidden">
                                    <div className={`absolute inset-0 bg-gradient-to-br ${i === 0 ? 'from-indigo-600 to-purple-800' : i === 1 ? 'from-blue-600 to-cyan-800' : 'from-emerald-600 to-teal-800'} opacity-50 group-hover:opacity-60 transition-opacity`} />
                                    <div className="absolute inset-0 flex items-center justify-center p-6 text-center">
                                        <span className="text-2xl font-bold text-white/20 uppercase tracking-widest">{post.category}</span>
                                    </div>
                                </div>
                                <div className="p-8 flex-1 flex flex-col">
                                    <div className="flex items-center gap-4 text-xs text-zinc-500 mb-4">
                                        <div className="flex items-center gap-1.5"><Calendar className="w-3 h-3" /> {post.date}</div>
                                        <div className="flex items-center gap-1.5"><User className="w-3 h-3" /> {post.author}</div>
                                    </div>
                                    <h3 className="text-xl font-bold text-white mb-3 group-hover:text-indigo-400 transition-colors">
                                        {post.title}
                                    </h3>
                                    <p className="text-sm text-zinc-400 mb-6 flex-1">
                                        {post.excerpt}
                                    </p>
                                    <div className="flex items-center text-sm font-semibold text-white mt-auto group-hover:gap-2 transition-all">
                                        Read Article <ArrowRight className="w-4 h-4 ml-2" />
                                    </div>
                                </div>
                            </Link>
                        ))}
                    </div>
                </div>
            </div>

            <Footer />
        </main>
    );
}
