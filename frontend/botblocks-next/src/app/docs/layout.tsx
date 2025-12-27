"use client";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Book, Zap, Layers, Settings, Code, Terminal, FileText } from "lucide-react";

export default function DocsLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const pathname = usePathname();

    const isActive = (path: string) => pathname === path;

    return (
        <main className="min-h-screen bg-zinc-950 text-white selection:bg-indigo-500/30">
            <Navbar />

            <div className="pt-24 pb-12 px-6">
                <div className="container mx-auto max-w-7xl flex flex-col md:flex-row gap-12">

                    {/* Persistent Sidebar */}
                    <aside className="w-full md:w-64 flex-shrink-0 hidden md:block">
                        <div className="sticky top-32 space-y-10">
                            <div>
                                <h3 className="text-xs font-bold text-zinc-400 uppercase tracking-widest mb-4 pl-3 border-l-2 border-indigo-500">Getting Started</h3>
                                <ul className="space-y-1">
                                    <li>
                                        <Link
                                            href="/docs"
                                            className={`flex items-center gap-2 py-1.5 px-3 text-sm font-medium rounded-md transition-colors ${isActive('/docs') ? 'bg-indigo-500/10 text-indigo-400' : 'text-zinc-400 hover:text-white'}`}
                                        >
                                            <Book className="w-4 h-4" /> Introduction
                                        </Link>
                                    </li>
                                    <li>
                                        <Link
                                            href="/docs/quick-start"
                                            className={`flex items-center gap-2 py-1.5 px-3 text-sm font-medium rounded-md transition-colors ${isActive('/docs/quick-start') ? 'bg-indigo-500/10 text-indigo-400' : 'text-zinc-400 hover:text-white'}`}
                                        >
                                            <Zap className="w-4 h-4" /> Quick Start
                                        </Link>
                                    </li>
                                </ul>
                            </div>

                            <div>
                                <h3 className="text-xs font-bold text-zinc-400 uppercase tracking-widest mb-4 pl-3 border-l-2 border-zinc-700">Guides</h3>
                                <ul className="space-y-1">
                                    <li>
                                        <Link
                                            href="/docs/training"
                                            className={`flex items-center gap-2 py-1.5 px-3 text-sm font-medium rounded-md transition-colors ${isActive('/docs/training') ? 'bg-indigo-500/10 text-indigo-400' : 'text-zinc-400 hover:text-white'}`}
                                        >
                                            <Layers className="w-4 h-4" /> Training (RAG)
                                        </Link>
                                    </li>
                                    <li>
                                        <Link
                                            href="/docs/customization"
                                            className={`flex items-center gap-2 py-1.5 px-3 text-sm font-medium rounded-md transition-colors ${isActive('/docs/customization') ? 'bg-indigo-500/10 text-indigo-400' : 'text-zinc-400 hover:text-white'}`}
                                        >
                                            <Settings className="w-4 h-4" /> Customization
                                        </Link>
                                    </li>
                                    <li>
                                        <Link
                                            href="/docs/embedding"
                                            className={`flex items-center gap-2 py-1.5 px-3 text-sm font-medium rounded-md transition-colors ${isActive('/docs/embedding') ? 'bg-indigo-500/10 text-indigo-400' : 'text-zinc-400 hover:text-white'}`}
                                        >
                                            <Code className="w-4 h-4" /> embedding
                                        </Link>
                                    </li>
                                </ul>
                            </div>

                            <div>
                                <h3 className="text-xs font-bold text-zinc-400 uppercase tracking-widest mb-4 pl-3 border-l-2 border-zinc-700">Developers</h3>
                                <ul className="space-y-1">
                                    <li>
                                        <Link
                                            href="/docs/api"
                                            className={`flex items-center gap-2 py-1.5 px-3 text-sm font-medium rounded-md transition-colors ${isActive('/docs/api') ? 'bg-indigo-500/10 text-indigo-400' : 'text-zinc-400 hover:text-white'}`}
                                        >
                                            <Terminal className="w-4 h-4" /> API Reference
                                        </Link>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </aside>

                    {/* Main Content Area */}
                    <div className="flex-1 max-w-4xl min-h-[60vh]">
                        {children}
                    </div>

                </div>
            </div>

            <Footer />
        </main>
    );
}
