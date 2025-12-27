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
                    className="relative hidden lg:block"
                >
                    {/* Vacant space for LandingBot placement reference if needed, or just empty */}
                    <div className="min-h-[600px] w-full" />
                </motion.div>
            </div>
        </section>
    );
}