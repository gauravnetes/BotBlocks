"use client";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { Check } from "lucide-react";

export default function PricingPage() {
    return (
        <main className="min-h-screen bg-zinc-950 text-white selection:bg-indigo-500/30">
            <Navbar />

            <div className="pt-32 pb-20 px-6">
                <div className="container mx-auto max-w-6xl">
                    <div className="text-center max-w-3xl mx-auto mb-16">
                        <h1 className="text-4xl md:text-5xl font-black tracking-tight mb-6">
                            Simple, Transparent Pricing
                        </h1>
                        <p className="text-lg text-zinc-400">
                            Start for free and scale as you grow. No hidden fees.
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        {/* Free Tier */}
                        <div className="p-8 rounded-2xl bg-zinc-900 border border-white/5 flex flex-col hover:border-white/10 transition-colors">
                            <div className="mb-8">
                                <h3 className="text-lg font-semibold text-zinc-200">Starter</h3>
                                <div className="mt-4 flex items-baseline">
                                    <span className="text-4xl font-bold text-white">$0</span>
                                    <span className="ml-2 text-zinc-500">/month</span>
                                </div>
                                <p className="mt-4 text-sm text-zinc-400">Perfect for trying out BotBlocks.</p>
                            </div>
                            <ul className="space-y-4 mb-8 flex-1">
                                <li className="flex items-center gap-3 text-sm text-zinc-300">
                                    <Check className="w-4 h-4 text-indigo-400" /> 1 Chatbot
                                </li>
                                <li className="flex items-center gap-3 text-sm text-zinc-300">
                                    <Check className="w-4 h-4 text-indigo-400" /> 50 Messages/mo
                                </li>
                                <li className="flex items-center gap-3 text-sm text-zinc-300">
                                    <Check className="w-4 h-4 text-indigo-400" /> Basic Analytics
                                </li>
                            </ul>
                            <button className="w-full py-3 rounded-lg bg-zinc-800 text-white font-semibold hover:bg-zinc-700 transition-colors">
                                Get Started
                            </button>
                        </div>

                        {/* Pro Tier */}
                        <div className="p-8 rounded-2xl bg-zinc-900 border border-indigo-500/30 ring-1 ring-indigo-500/30 flex flex-col relative overflow-hidden">
                            <div className="absolute top-0 right-0 bg-indigo-500 text-white text-xs font-bold px-3 py-1 rounded-bl-lg">
                                POPULAR
                            </div>
                            <div className="mb-8">
                                <h3 className="text-lg font-semibold text-white">Pro</h3>
                                <div className="mt-4 flex items-baseline">
                                    <span className="text-4xl font-bold text-white">$29</span>
                                    <span className="ml-2 text-zinc-500">/month</span>
                                </div>
                                <p className="mt-4 text-sm text-zinc-400">For growing businesses.</p>
                            </div>
                            <ul className="space-y-4 mb-8 flex-1">
                                <li className="flex items-center gap-3 text-sm text-zinc-300">
                                    <Check className="w-4 h-4 text-indigo-400" /> 5 Chatbots
                                </li>
                                <li className="flex items-center gap-3 text-sm text-zinc-300">
                                    <Check className="w-4 h-4 text-indigo-400" /> 2,000 Messages/mo
                                </li>
                                <li className="flex items-center gap-3 text-sm text-zinc-300">
                                    <Check className="w-4 h-4 text-indigo-400" /> Advanced Analytics
                                </li>
                                <li className="flex items-center gap-3 text-sm text-zinc-300">
                                    <Check className="w-4 h-4 text-indigo-400" /> Remove Branding
                                </li>
                            </ul>
                            <button className="w-full py-3 rounded-lg bg-indigo-600 text-white font-semibold hover:bg-indigo-500 transition-colors">
                                Upgrade Now
                            </button>
                        </div>

                        {/* Enterprise Tier */}
                        <div className="p-8 rounded-2xl bg-zinc-900 border border-white/5 flex flex-col hover:border-white/10 transition-colors">
                            <div className="mb-8">
                                <h3 className="text-lg font-semibold text-zinc-200">Enterprise</h3>
                                <div className="mt-4 flex items-baseline">
                                    <span className="text-4xl font-bold text-white">Custom</span>
                                </div>
                                <p className="mt-4 text-sm text-zinc-400">For large scale needs.</p>
                            </div>
                            <ul className="space-y-4 mb-8 flex-1">
                                <li className="flex items-center gap-3 text-sm text-zinc-300">
                                    <Check className="w-4 h-4 text-indigo-400" /> Unlimited Chatbots
                                </li>
                                <li className="flex items-center gap-3 text-sm text-zinc-300">
                                    <Check className="w-4 h-4 text-indigo-400" /> Unlimited Messages
                                </li>
                                <li className="flex items-center gap-3 text-sm text-zinc-300">
                                    <Check className="w-4 h-4 text-indigo-400" /> Custom Training
                                </li>
                                <li className="flex items-center gap-3 text-sm text-zinc-300">
                                    <Check className="w-4 h-4 text-indigo-400" /> SLA Support
                                </li>
                            </ul>
                            <button className="w-full py-3 rounded-lg bg-zinc-800 text-white font-semibold hover:bg-zinc-700 transition-colors">
                                Contact Sales
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <Footer />
        </main>
    );
}
