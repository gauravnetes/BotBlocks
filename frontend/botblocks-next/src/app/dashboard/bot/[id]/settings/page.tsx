"use client";

import { useState, useEffect } from "react";
import { getBot, Bot } from "@/lib/api"; // You might need an updateBot function later
import { useParams } from "next/navigation";
import { toast } from "sonner";

export default function SettingsPage() {
    const params = useParams();
    const [bot, setBot] = useState<Bot | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        if (params.id) {
            getBot(params.id as string)
                .then((data) => setBot(data))
                .catch((err) => console.error(err))
                .finally(() => setIsLoading(false));
        }
    }, [params.id]);

    if (isLoading) return <div className="p-8 text-zinc-400">Loading settings...</div>;
    if (!bot) return <div className="p-8 text-red-400">Bot not found</div>;

    return (
        <div className="bg-zinc-900 border border-white/5 rounded-xl p-6">
            <h3 className="text-white font-bold mb-4">Bot Configuration</h3>
            <p className="text-zinc-500 text-sm mb-4">Update your bot&apos;s personality and behavior.</p>
            <textarea
                className="w-full bg-black/20 border border-white/10 rounded-lg p-4 text-white font-mono text-sm h-40 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                defaultValue={bot.system_prompt}
            />
            <div className="mt-4 flex justify-end">
                <button
                    onClick={() => toast.info("Save functionality coming in next update!")}
                    className="bg-white text-black px-6 py-2 rounded-lg font-medium hover:bg-zinc-200"
                >
                    Save Changes
                </button>
            </div>
        </div>
    );
}
