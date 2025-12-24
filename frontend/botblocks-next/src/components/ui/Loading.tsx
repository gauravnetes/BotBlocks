"use client";
import { motion } from "framer-motion";

export function Loading() {
    return (
        <div className="flex flex-col items-center justify-center h-64 space-y-8">
            <div className="relative flex items-center justify-center">
                {/* Outer pulsing ring */}
                <motion.div
                    className="absolute w-24 h-24 border-2 border-blue-500/30 rounded-full"
                    animate={{ scale: [1, 1.2, 1], opacity: [0.5, 0, 0.5] }}
                    transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
                />
                {/* Middle pulsing ring */}
                <motion.div
                    className="absolute w-16 h-16 border-2 border-blue-500/50 rounded-full"
                    animate={{ scale: [1, 1.1, 1], opacity: [0.8, 0.2, 0.8] }}
                    transition={{ duration: 2, repeat: Infinity, ease: "easeInOut", delay: 0.2 }}
                />
                {/* Inner core */}
                <motion.div
                    className="w-3 h-3 bg-blue-500 rounded-full shadow-[0_0_15px_rgba(59,130,246,0.8)]"
                    animate={{ scale: [1, 1.5, 1] }}
                    transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
                />
            </div>
            <motion.p
                className="text-zinc-400 font-medium tracking-widest text-sm uppercase"
                animate={{ opacity: [0.4, 1, 0.4] }}
                transition={{ duration: 2, repeat: Infinity }}
            >
                Loading
            </motion.p>
        </div>
    );
}
