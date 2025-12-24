"use client";
import { motion } from "framer-motion";
import Link from "next/link";

export function Hero() {
    return (
        <section className="relative flex min-h-screen items-center justify-center pt-20 px-20">
            {/* Background Aura */}
            <div className="absolute top-[-20%] left-1/2 -translate-x-1/2 w-[1000px] h-[800px] bg-blue-500/10 blur-[120px] rounded-full pointer-events-none" />

            <div className="container mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 px-6 items-center relative z-10">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                >
                    <h1 className="text-6xl font-extrabold leading-tight text-white mb-6">
                        Build AI Agents<br />
                        That <span className="text-blue-500">Understand</span>
                    </h1>
                    <p className="text-xl text-zinc-400 mb-8 max-w-lg">
                        The complete platform for building, training, and deploying intelligent chatbots.
                        Connect your data, define your persona, and launch in minutes.
                    </p>
                    <Link href="/dashboard" className="inline-block bg-white text-black px-8 py-3 rounded-lg font-semibold hover:bg-zinc-200 transition-colors">
                        Start Building Free
                    </Link>
                    <p className="text-sm text-zinc-500 mt-4">No credit card required · 14-day free trial</p>
                </motion.div>

                <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.5, delay: 0.2 }}
                    className="relative"
                >
                    {/* Chat Visual Card */}
                    <div className="bg-zinc-900/60 backdrop-blur-xl border border-white/10 rounded-3xl p-6 shadow-2xl">
                        <div className="flex items-center gap-4 mb-6 border-b border-white/5 pb-4">
                            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center text-xl">🤖</div>
                            <div>
                                <div className="font-semibold text-white">Support Bot</div>
                                <div className="flex items-center gap-1.5 text-xs text-green-500">
                                    <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" /> Online
                                </div>
                            </div>
                        </div>
                        <div className="space-y-4">
                            <div className="self-end bg-blue-600 text-white p-3 rounded-2xl rounded-tr-sm max-w-[80%] ml-auto">
                                How do I connect my Notion knowledge base?
                            </div>
                            <div className="self-start bg-white/5 text-zinc-200 p-3 rounded-2xl rounded-tl-sm max-w-[80%] border border-white/5">
                                It's easy! Just go to the "Knowledge" tab, click "Add Source", and select Notion. I'll automatically index your pages. 📚
                            </div>
                        </div>
                    </div>
                </motion.div>
            </div>
        </section>
    );
}