"use client";

import { useState, useEffect } from "react";
import { getBot, getWidgetConfig, updateWidgetConfig, Bot } from "@/lib/api";
import { WidgetCustomizer } from "@/components/dashboard/WidgetCustomizer";
import { WidgetPreview } from "@/components/dashboard/WidgetPreview";
import { useParams } from "next/navigation";
import { useAuth } from "@clerk/nextjs";

export default function WidgetPage() {
    const params = useParams();
    const [bot, setBot] = useState<Bot | null>(null);
    const [widgetConfig, setWidgetConfig] = useState<any>(null);
    const [lastWidgetUpdate, setLastWidgetUpdate] = useState(0);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        if (params.id) {
            Promise.all([
                getBot(params.id as string),
                getWidgetConfig(params.id as string)
            ])
                .then(([botData, configData]) => {
                    setBot(botData);
                    setWidgetConfig(configData);
                })
                .catch((err) => console.error(err))
                .finally(() => setIsLoading(false));
        }
    }, [params.id]);

    const { getToken } = useAuth();

    const handleWidgetUpdate = async (config: any) => {
        if (!bot) return;
        const token = await getToken();
        await updateWidgetConfig(bot.public_id, config, token);
        setWidgetConfig(config);
        setLastWidgetUpdate(Date.now());
    };

    if (isLoading) return <div className="p-8 text-zinc-400">Loading widget config...</div>;
    if (!bot || !widgetConfig) return <div className="p-8 text-red-400">Failed to load configuration</div>;

    return (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-[670px]">
            <div className="bg-zinc-900 border border-white/5 rounded-xl p-6 overflow-y-auto">
                <h3 className="text-white font-bold mb-6">Customize Widget</h3>
                <WidgetCustomizer
                    botId={bot.public_id}
                    botName={bot.name}
                    initialConfig={widgetConfig}
                    onUpdate={handleWidgetUpdate}
                />
            </div>
            <div className="h-full">
                <WidgetPreview botId={bot.public_id} lastUpdate={lastWidgetUpdate} />
            </div>
        </div>
    );
}
