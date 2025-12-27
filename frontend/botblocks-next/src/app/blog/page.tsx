"use client";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import Link from "next/link";
import Image from "next/image";
import { Calendar, User, ArrowRight, Search, Tag, Clock } from "lucide-react";
import { useState } from "react";

// Expanded Blog Data with Real Unsplash Images
const BLOG_POSTS = [
    {
        title: "The Future of AI Chatbots in 2025",
        excerpt: "How Large Language Models are transforming customer support. We explore the shift from static scripts to dynamic, context-aware agents that truly understand human intent.",
        date: "Dec 15, 2024",
        readTime: "5 min read",
        author: "Souvik Rahut",
        category: "AI Trends",
        slug: "future-of-ai-chatbots",
        image: "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&q=80",
        featured: true
    },
    {
        title: "Building Context-Aware Agents",
        excerpt: "A deep dive into RAG (Retrieval-Augmented Generation) and how BotBlocks fetches the right data to answer complex queries without hallucinations.",
        date: "Nov 28, 2024",
        readTime: "8 min read",
        author: "Team BotBlocks",
        category: "Engineering",
        slug: "building-context-aware-agents",
        image: "https://images.unsplash.com/photo-1558494949-efc527753ec9?auto=format&fit=crop&q=80",
        featured: false
    },
    {
        title: "Optimizing Your Bot for Sales",
        excerpt: "Practical tips to train your chatbot to verify leads, recommend products, and convert casual visitors into paying customers effectively.",
        date: "Nov 10, 2024",
        readTime: "6 min read",
        author: "Sarah J.",
        category: "Guides",
        slug: "optimizing-bot-for-sales",
        image: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80",
        featured: false
    },
    {
        title: "No-Code vs. Code-First",
        excerpt: "Why the line between no-code builders and traditional coding is blurring, and how BotBlocks offers the best of both worlds.",
        date: "Oct 22, 2024",
        readTime: "4 min read",
        author: "Alex Rivers",
        category: "Opinion",
        slug: "no-code-vs-code-first",
        image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&q=80",
        featured: false
    },
    {
        title: "Security in the Age of AI",
        excerpt: "Understanding data privacy, SOC2 compliance, and how we keep your knowledge base secure while using powerful LLMs.",
        date: "Oct 05, 2024",
        readTime: "7 min read",
        author: "Security Team",
        category: "Security",
        slug: "security-in-age-of-ai",
        image: "https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&q=80",
        featured: false
    },
    {
        title: "BotBlocks Launch Day",
        excerpt: "A look back at our product launch, the lessons we learned, and what we have planned for the next quarter roadmap.",
        date: "Sep 15, 2024",
        readTime: "3 min read",
        author: "Souvik Rahut",
        category: "Company",
        slug: "botblocks-launch-day",
        image: "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&q=80",
        featured: false
    }
];

const CATEGORIES = ["All", "AI Trends", "Engineering", "Guides", "Security", "Company"];

export default function BlogPage() {
    const [selectedCategory, setSelectedCategory] = useState("All");
    const [searchQuery, setSearchQuery] = useState("");

    const filteredPosts = BLOG_POSTS.filter(post => {
        const matchesCategory = selectedCategory === "All" || post.category === selectedCategory;
        const matchesSearch = post.title.toLowerCase().includes(searchQuery.toLowerCase()) || post.excerpt.toLowerCase().includes(searchQuery.toLowerCase());
        return matchesCategory && matchesSearch;
    });

    const featuredPost = BLOG_POSTS.find(post => post.featured);
    const regularPosts = filteredPosts.filter(post => post !== featuredPost);

    return (
        <main className="min-h-screen bg-zinc-950 text-white selection:bg-indigo-500/30">
            <Navbar />

            <div className="pt-32 pb-20 px-6">
                <div className="container mx-auto max-w-6xl">

                    {/* Header */}
                    <div className="text-center max-w-3xl mx-auto mb-16">
                        <span className="inline-block px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-bold uppercase tracking-wider mb-4 animate-in fade-in slide-in-from-bottom-2">
                            The Blog
                        </span>
                        <h1 className="text-4xl md:text-5xl font-black tracking-tight mb-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
                            Insights & Updates
                        </h1>
                        <p className="text-lg text-zinc-400 animate-in fade-in slide-in-from-bottom-6 duration-700">
                            Thoughts on AI, engineering, and the future of customer experience.
                        </p>
                    </div>

                    {/* Featured Post */}
                    {featuredPost && selectedCategory === "All" && !searchQuery && (
                        <div className="mb-20 animate-in fade-in duration-700">
                            <Link href="#" className="group relative block w-full rounded-3xl overflow-hidden aspect-[21/9] md:aspect-[2.5/1]">
                                <Image
                                    src={featuredPost.image}
                                    alt={featuredPost.title}
                                    fill
                                    className="object-cover transition-transform duration-700 group-hover:scale-105"
                                    priority
                                />
                                <div className="absolute inset-0 bg-gradient-to-t from-black via-black/50 to-transparent" />
                                <div className="absolute bottom-0 left-0 p-8 md:p-12 max-w-2xl">
                                    <div className="flex items-center gap-4 text-xs font-bold uppercase tracking-widest text-indigo-400 mb-4">
                                        <span className="px-2 py-1 bg-indigo-500/20 rounded border border-indigo-500/30 backdrop-blur-sm">Featured</span>
                                        <span>{featuredPost.category}</span>
                                    </div>
                                    <h2 className="text-3xl md:text-5xl font-black text-white mb-4 leading-tight group-hover:text-indigo-200 transition-colors">
                                        {featuredPost.title}
                                    </h2>
                                    <p className="text-zinc-300 text-lg md:text-xl mb-6 line-clamp-2">
                                        {featuredPost.excerpt}
                                    </p>
                                    <div className="flex items-center gap-6 text-sm text-zinc-400 font-medium">
                                        <div className="flex items-center gap-2"><User className="w-4 h-4" /> {featuredPost.author}</div>
                                        <div className="flex items-center gap-2"><Clock className="w-4 h-4" /> {featuredPost.readTime}</div>
                                        <div className="flex items-center gap-2"><Calendar className="w-4 h-4" /> {featuredPost.date}</div>
                                    </div>
                                </div>
                            </Link>
                        </div>
                    )}

                    {/* Filters & Search */}
                    <div className="sticky top-24 z-30 bg-zinc-950/80 backdrop-blur-md py-4 mb-10 border-b border-white/5 flex flex-col md:flex-row items-center justify-between gap-4">
                        <div className="flex items-center gap-2 overflow-x-auto w-full md:w-auto pb-2 md:pb-0 scrollbar-hide">
                            {CATEGORIES.map(category => (
                                <button
                                    key={category}
                                    onClick={() => setSelectedCategory(category)}
                                    className={`px-4 py-2 rounded-full text-sm font-medium transition-all whitespace-nowrap ${selectedCategory === category
                                            ? "bg-white text-black"
                                            : "bg-zinc-900 text-zinc-400 hover:text-white hover:bg-zinc-800"
                                        }`}
                                >
                                    {category}
                                </button>
                            ))}
                        </div>
                        <div className="relative w-full md:w-auto">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-500" />
                            <input
                                type="text"
                                placeholder="Search articles..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="w-full md:w-64 bg-zinc-900 border border-white/10 rounded-full py-2 pl-10 pr-4 text-sm text-white placeholder:text-zinc-600 focus:outline-none focus:border-indigo-500/50 transition-colors"
                            />
                        </div>
                    </div>

                    {/* Posts Grid */}
                    {regularPosts.length > 0 ? (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                            {regularPosts.map((post, i) => (
                                <Link
                                    key={i}
                                    href="#"
                                    className="group flex flex-col bg-zinc-900/50 border border-white/5 rounded-2xl overflow-hidden hover:border-indigo-500/30 hover:bg-zinc-900 transition-all hover:-translate-y-1 duration-300"
                                >
                                    <div className="aspect-[16/10] relative overflow-hidden bg-zinc-800">
                                        <Image
                                            src={post.image}
                                            alt={post.title}
                                            fill
                                            className="object-cover group-hover:scale-105 transition-transform duration-500"
                                        />
                                        <div className="absolute top-4 left-4">
                                            <span className="px-3 py-1 rounded-full bg-black/60 backdrop-blur-md border border-white/10 text-[10px] font-bold uppercase tracking-wider text-white">
                                                {post.category}
                                            </span>
                                        </div>
                                    </div>
                                    <div className="p-6 md:p-8 flex-1 flex flex-col">
                                        <div className="flex items-center gap-4 text-xs text-zinc-500 mb-4 font-medium">
                                            <div className="flex items-center gap-1.5"><Calendar className="w-3 h-3" /> {post.date}</div>
                                            <div className="flex items-center gap-1.5"><Clock className="w-3 h-3" /> {post.readTime}</div>
                                        </div>
                                        <h3 className="text-xl font-bold text-white mb-3 group-hover:text-indigo-400 transition-colors line-clamp-2">
                                            {post.title}
                                        </h3>
                                        <p className="text-sm text-zinc-400 mb-6 flex-1 line-clamp-3 leading-relaxed">
                                            {post.excerpt}
                                        </p>
                                        <div className="flex items-center gap-3 mt-auto">
                                            <div className="w-8 h-8 rounded-full bg-indigo-500/20 flex items-center justify-center text-indigo-300 text-xs font-bold">
                                                {post.author.charAt(0)}
                                            </div>
                                            <span className="text-xs font-medium text-zinc-400">{post.author}</span>
                                            <ArrowRight className="w-4 h-4 text-zinc-600 ml-auto group-hover:text-indigo-400 group-hover:translate-x-1 transition-all" />
                                        </div>
                                    </div>
                                </Link>
                            ))}
                        </div>
                    ) : (
                        <div className="text-center py-20 bg-zinc-900/30 rounded-3xl border border-white/5">
                            <Tag className="w-12 h-12 text-zinc-600 mx-auto mb-4" />
                            <h3 className="text-xl font-bold text-white mb-2">No articles found</h3>
                            <p className="text-zinc-500">Try searching for something else or change the category.</p>
                            <button
                                onClick={() => { setSelectedCategory("All"); setSearchQuery(""); }}
                                className="mt-6 text-indigo-400 hover:text-indigo-300 text-sm font-semibold"
                            >
                                Clear filters
                            </button>
                        </div>
                    )}
                </div>
            </div>

            <Footer />
        </main>
    );
}
