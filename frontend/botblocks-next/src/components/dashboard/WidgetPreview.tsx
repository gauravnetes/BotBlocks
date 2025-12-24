"use client";
import { useEffect, useState } from 'react';
import { ChatWidget } from '../widget/ChatWidget';
import { getWidgetConfig } from '@/lib/api';

interface WidgetPreviewProps {
    botId: string;
}

export function WidgetPreview({ botId, lastUpdate }: { botId: string, lastUpdate?: number }) {
    const [config, setConfig] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [refreshKey, setRefreshKey] = useState(0);

    const loadConfig = async () => {
        setIsLoading(true);
        try {
            const data = await getWidgetConfig(botId);
            setConfig(data);
        } catch (error) {
            console.error('Failed to load widget config:', error);
        } finally {
            setIsLoading(false);
        }
    };

    // Reload when lastUpdate changes
    useEffect(() => {
        if (lastUpdate) {
            loadConfig();
        }
    }, [lastUpdate]);

    useEffect(() => {
        loadConfig();
    }, [botId]);

    const handleRefresh = () => {
        setRefreshKey(prev => prev + 1);
        loadConfig();
    };

    if (isLoading) {
        return (
            <div className="bg-gradient-to-br from-zinc-900 to-zinc-950 rounded-xl border border-white/10 p-6 h-full flex items-center justify-center">
                <div className="animate-spin text-2xl">⏳</div>
            </div>
        );
    }

    return (
        <div className="h-full flex flex-col">
            {/* Header */}
            <div className="flex items-center justify-between mb-4 px-1">
                <div>
                    <h3 className="text-sm font-bold text-white">Preview</h3>
                    <p className="text-[11px] text-zinc-400">Real-time widget preview</p>
                </div>

                <button
                    onClick={handleRefresh}
                    className="flex items-center gap-1.5 bg-zinc-800/50 hover:bg-zinc-800 text-zinc-300 hover:text-white px-3 py-1.5 rounded-lg text-xs font-medium transition border border-white/5"
                >
                    🔄 Refresh
                </button>
            </div>

            {/* Preview Area */}
            <div className="flex-1 bg-zinc-900/60 border border-white/10 rounded-xl overflow-hidden relative flex items-center justify-center p-4">

                {/* Fake Website Frame - simplified and cleaner */}
                <div className="relative w-full h-full bg-white rounded-lg shadow-2xl overflow-hidden flex flex-col">

                    {/* Browser Bar */}
                    <div className="flex items-center gap-2 px-3 py-2 bg-zinc-100 border-b border-zinc-200 shrink-0">
                        <div className="flex gap-1.5">
                            <span className="w-2.5 h-2.5 bg-red-400 rounded-full" />
                            <span className="w-2.5 h-2.5 bg-yellow-400 rounded-full" />
                            <span className="w-2.5 h-2.5 bg-green-400 rounded-full" />
                        </div>
                        <div className="ml-3 flex-1 bg-white rounded px-2 py-0.5 text-[10px] text-zinc-400 border border-zinc-200 truncate font-mono">
                            example.com
                        </div>
                    </div>

                    {/* Fake Website Content */}
                    <div className="relative flex-1 bg-zinc-50 p-6 md:p-10 overflow-hidden">
                        <div className="max-w-xl space-y-4 opacity-10">
                            <div className="h-4 bg-zinc-400 rounded w-3/4" />
                            <div className="h-4 bg-zinc-400 rounded w-full" />
                            <div className="h-4 bg-zinc-400 rounded w-5/6" />
                            <div className="h-4 bg-zinc-400 rounded w-2/3" />
                            <div className="h-32 bg-zinc-400 rounded w-full mt-8" />
                        </div>

                        {/* Widget Mount Area */}
                        <div className="absolute inset-0 pointer-events-none overflow-hidden">
                            <div className="relative w-full h-full pointer-events-auto">

                                {/* Scale wrapper - simplified for better containment */}
                                <div className="absolute inset-0 flex items-end justify-end">
                                    <div
                                        className="relative w-full h-full"
                                        style={{
                                            transform: "scale(0.70)",
                                            transformOrigin: config?.position === 'bottom-left' ? 'bottom left' : 'bottom right'
                                        }}
                                    >
                                        {config && (
                                            <ChatWidget
                                                botId={botId}
                                                config={config}
                                                previewMode={true}
                                            />
                                        )}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );

}
