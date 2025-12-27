"use client";
import { motion } from "framer-motion";
import Link from "next/link";
import { ArrowRight, Sparkles } from "lucide-react";
import { MorphingText } from "./ui/MorphingText";

// Multilingual Greetings in native scripts
// const texts = [
//     "Hello",
//     "नमस्ते", // Hindi
//     "নমস্কার", // Bengali
//     "Bonjour", // French
//     "Hola", // Spanish
//     "こんにちは", // Japanese
//     "안녕하세요", // Korean
//     "Ciao", // Italian
//     "你好", // Chinese
//     "Olá", // Portuguese
// ]
const texts = [
    "नमस्ते",
    "নমস্কার",
    "வணக்கம்",
    "నమస్కారం",
    "नमस्कार",
    "ನಮಸ್ಕಾರ",
    "નમસ્તે",
    "നമസ്കാരം",
    "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ",
    "নমস্কাৰ",
]
export function Hero() {
    return (
        <section className="relative flex min-h-screen items-center pt-20 pb-12 px-6 overflow-hidden">
            {/* Background Aura */}
            <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-indigo-900/10 via-zinc-950 to-zinc-950" />
            <div className="absolute top-[-10%] right-[-5%] w-[600px] h-[600px] bg-indigo-500/10 blur-[100px] rounded-full pointer-events-none" />
            <div className="absolute bottom-[-10%] left-[-5%] w-[500px] h-[500px] bg-blue-500/10 blur-[120px] rounded-full pointer-events-none" />

            <div className="container mx-auto max-w-7xl relative z-10">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-16 items-center">

                    {/* Left Content */}
                    <div className="flex flex-col items-center lg:items-start text-center lg:text-left overflow-visible">
                        <motion.div
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5 }}
                            className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-xs font-semibold text-indigo-300 mb-6 backdrop-blur-sm"
                        >
                            <Sparkles className="w-3 h-3" />
                            BotBlocks v2.0 — The WordPress for AI Chatbots
                        </motion.div>

                        <motion.h1
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: 0.1 }}
                            className="text-5xl sm:text-6xl lg:text-7xl font-black tracking-tighter text-white mb-4 leading-[0.9] flex flex-col items-center lg:items-start w-full"
                        >
                            <span className="opacity-90 text-zinc-400">Build Neural Blocks.</span>
                            <div className="h-[1.5em] flex items-center overflow-visible w-full justify-center lg:justify-start mt-2">
                                <MorphingText
                                    texts={texts}
                                    className="text-white !mx-0 !text-left lg:!text-left flex justify-center lg:justify-start"
                                />
                            </div>
                        </motion.h1>

                        <motion.p
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: 0.2 }}
                            className="text-base sm:text-lg text-zinc-400 mb-8 max-w-lg leading-relaxed mt-2"
                        >
                            The WordPress for AI Chatbots. Build, train, and deploy intelligent,
                            context-aware entities that speak every language and understand every detail.
                        </motion.p>

                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: 0.3 }}
                            className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto"
                        >
                            <Link
                                href="/dashboard"
                                className="group inline-flex items-center justify-center gap-2 bg-white text-black px-10 py-3.5 rounded-full font-bold hover:bg-indigo-50 transition-all hover:translate-y-[-2px] hover:shadow-[0_10px_20px_-10px_rgba(255,255,255,0.3)] shadow-lg"
                            >
                                Start Free
                                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                            </Link>
                            <Link
                                href="#features"
                                className="inline-flex items-center justify-center gap-2 px-10 py-3.5 rounded-full font-medium text-white border border-white/10 hover:bg-white/5 transition-all text-sm uppercase tracking-widest bg-zinc-900/50 backdrop-blur-sm shadow-lg"
                            >
                                See Demo
                            </Link>
                        </motion.div>

                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ delay: 0.5 }}
                            className="flex items-center gap-6 mt-10 opacity-50 grayscale hover:grayscale-0 transition-all"
                        >
                            <div className="flex items-center gap-1.5 text-[10px] font-bold tracking-tighter text-zinc-400 uppercase">
                                <div className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                                Instant Setup
                            </div>
                            <div className="flex items-center gap-1.5 text-[10px] font-bold tracking-tighter text-zinc-400 uppercase">
                                <div className="w-1.5 h-1.5 rounded-full bg-indigo-500" />
                                Global Reach
                            </div>
                        </motion.div>
                    </div>

                    {/* Right Content - Video Container (Compact) */}
                    <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
                        className="relative hidden lg:block"
                    >
                        <div className="relative aspect-video rounded-[2rem] overflow-hidden border border-white/10 shadow-[0_0_50px_rgba(99,102,241,0.2)] bg-zinc-900/50 group">
                            {/* Inner Glow */}
                            <div className="absolute inset-0 bg-gradient-to-tr from-indigo-500/10 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700" />

                            {/* Play Button Visual (Rounded) */}
                            <div className="absolute inset-0 flex items-center justify-center">
                                <div className="w-16 h-16 rounded-full bg-white/5 backdrop-blur-xl flex items-center justify-center border border-white/10 group-hover:scale-110 group-hover:bg-white/10 transition-all duration-500 cursor-pointer shadow-2xl">
                                    <div className="w-0 h-0 border-t-[10px] border-t-transparent border-l-[16px] border-l-white/80 border-b-[10px] border-b-transparent ml-1" />
                                </div>
                            </div>

                            <div className="absolute bottom-4 left-4 right-4 bg-zinc-950/80 backdrop-blur-md p-2.5 rounded-2xl border border-white/5 flex items-center justify-between">
                                <div className="flex items-center gap-2">
                                    <div className="w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse" />
                                    <span className="text-[9px] uppercase font-bold tracking-widest text-zinc-400">BotBlocks.Process</span>
                                </div>
                                <span className="text-[9px] font-mono text-zinc-600 tracking-wide">00:42 / 02:15</span>
                            </div>
                        </div>

                        {/* Abstract Background Shapes */}
                        <div className="absolute -top-6 -right-6 w-32 h-32 bg-indigo-600/10 rounded-full blur-[50px] -z-10 animate-pulse" />
                    </motion.div>
                </div>
            </div>
        </section>
    );
}