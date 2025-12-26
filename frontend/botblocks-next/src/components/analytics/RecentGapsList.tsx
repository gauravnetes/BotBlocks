"use client";

import React from "react";
import { KnowledgeGap } from "@/lib/types/analytics";
import { formatDistanceToNow } from "date-fns";
import { MessageSquare, Clock, AlertTriangle, Hammer } from "lucide-react";

interface RecentGapsListProps {
    gaps: KnowledgeGap[];
    onResolve: (query: string, logId?: number) => void;
}

export function RecentGapsList({ gaps, onResolve }: RecentGapsListProps) {
    if (!gaps.length) {
        return (
            <div className="bg-zinc-900/50 border border-white/5 rounded-xl p-6 h-full flex items-center justify-center animate-in fade-in duration-500">
                <div className="text-center text-zinc-500">
                    <p>No recent gaps found.</p>
                </div>
            </div>
        );
    }

    // Limit to 10
    const displayGaps = gaps.slice(0, 10);

    return (
        <div className="bg-zinc-900/50 border border-white/5 rounded-xl p-6 hover:border-white/10 transition-colors h-full flex flex-col">
            <h3 className="text-lg font-bold text-white mb-6 flex items-center gap-2">
                <AlertTriangle className="w-5 h-5 text-amber-500" />
                Recent Knowledge Gaps
            </h3>

            <div className="space-y-3 overflow-y-auto max-h-[300px] pr-2 scrollbar-thin scrollbar-thumb-zinc-700 scrollbar-track-transparent">
                {displayGaps.map((gap, i) => (
                    <div
                        key={i}
                        className="group flex flex-col gap-2 p-3 rounded-lg border border-white/5 bg-black/20 hover:bg-white/5 hover:border-white/10 transition-all cursor-default"
                    >
                        <div className="flex items-start gap-3">
                            <MessageSquare className="w-4 h-4 text-zinc-600 mt-1 shrink-0 group-hover:text-zinc-400 transition-colors" />
                            <p className="text-sm text-zinc-300 italic font-medium group-hover:text-white transition-colors break-words line-clamp-2">"{gap.query}"</p>
                        </div>

                        <div className="flex items-center justify-between pl-7">
                            <div className="flex items-center gap-1.5 text-xs text-zinc-500">
                                <Clock className="w-3 h-3" />
                                {formatDistanceToNow(new Date(gap.timestamp), { addSuffix: true })}
                            </div>
                            <div className="flex items-center gap-2">
                                <span className={`text-[10px] font-mono font-bold px-1.5 py-0.5 rounded border ${gap.confidence > 0.6 ? "text-green-500 border-green-900 bg-green-900/20" :
                                    gap.confidence > 0.4 ? "text-amber-500 border-amber-900 bg-amber-900/20" :
                                        "text-red-500 border-red-900 bg-red-900/20"
                                    }`}>
                                    CONF: {(gap.confidence * 100).toFixed(0)}%
                                </span>
                                <button
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        onResolve(gap.query);
                                    }}
                                    className="p-1 hover:bg-blue-500/20 text-zinc-500 hover:text-blue-400 rounded transition-colors group/btn"
                                    title="Fix this gap"
                                >
                                    <Hammer className="w-3.5 h-3.5" />
                                </button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
