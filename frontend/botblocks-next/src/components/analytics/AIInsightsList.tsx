"use client";

import React, { useState } from "react";
import { AIInsight } from "@/lib/types/analytics";
import { AlertCircle, TrendingUp, CheckCircle, RefreshCcw, ChevronDown, ChevronUp, Plus } from "lucide-react";
import { toast } from "sonner";
import { cn } from "@/lib/utils";

interface AIInsightsListProps {
    insights: AIInsight[];
    onRefresh: () => void;
    refreshing: boolean;
    onResolve: (query: string) => void;
}

export function AIInsightsList({ insights, onRefresh, refreshing, onResolve }: AIInsightsListProps) {
    const [expanded, setExpanded] = useState<number | null>(null);

    const getPriorityColor = (p: string) => {
        switch (p) {
            case "high": return "text-red-400 border-red-400/20 bg-red-400/10";
            case "medium": return "text-amber-400 border-amber-400/20 bg-amber-400/10";
            case "low": return "text-blue-400 border-blue-400/20 bg-blue-400/10";
            default: return "text-zinc-400 border-zinc-500/20 bg-zinc-500/10";
        }
    };

    if (!insights.length) {
        return (
            <div className="bg-zinc-900/50 border border-white/5 rounded-xl p-8 text-center hover:border-white/10 transition-colors animate-in fade-in duration-500">
                <div className="w-12 h-12 bg-green-500/10 rounded-full flex items-center justify-center mx-auto mb-4 animate-pulse">
                    <CheckCircle className="w-6 h-6 text-green-500" />
                </div>
                <h3 className="text-white font-medium mb-2">All Good!</h3>
                <p className="text-zinc-400 text-sm mb-6">No specific improvement opportunities found yet.</p>
                <button
                    onClick={onRefresh}
                    disabled={refreshing}
                    className="text-sm text-blue-400 hover:text-blue-300 flex items-center gap-2 mx-auto disabled:opacity-50 transition-colors"
                >
                    <RefreshCcw className={`w-4 h-4 ${refreshing ? "animate-spin" : ""}`} />
                    Force Re-analysis
                </button>
            </div>
        );
    }

    return (
        <div className="bg-zinc-900/50 border border-white/5 rounded-xl p-6 hover:border-white/10 transition-colors">
            <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <TrendingUp className="w-5 h-5 text-purple-400" />
                    AI Insights
                </h3>
                <button
                    onClick={onRefresh}
                    disabled={refreshing}
                    className="p-2 hover:bg-white/5 rounded-lg text-zinc-400 hover:text-white transition-colors disabled:opacity-50"
                    title="Refresh Insights"
                >
                    <RefreshCcw className={`w-4 h-4 ${refreshing ? "animate-spin" : ""}`} />
                </button>
            </div>

            <div className="space-y-4">
                {insights.map((insight, i) => (
                    <div
                        key={i}
                        className="border border-white/5 rounded-lg bg-black/20 overflow-hidden hover:border-white/10 transition-colors animate-in slide-in-from-bottom-2 duration-300"
                        style={{ animationDelay: `${i * 100}ms` }}
                    >
                        <div
                            className="p-4 cursor-pointer hover:bg-white/5 transition-colors"
                            onClick={() => setExpanded(expanded === i ? null : i)}
                        >
                            <div className="flex items-start justify-between gap-4">
                                <div className="flex gap-3">
                                    <AlertCircle className={`w-5 h-5 mt-0.5 shrink-0 ${insight.priority === 'high' ? 'text-red-400' :
                                        insight.priority === 'medium' ? 'text-amber-400' : 'text-blue-400'
                                        }`} />
                                    <div>
                                        <h4 className="text-white font-medium text-sm leading-6">{insight.topic}</h4>
                                        <p className="text-zinc-400 text-xs mt-1 pr-4 leading-5">{insight.advice}</p>
                                    </div>
                                </div>
                                <div className="flex flex-col items-end gap-2 shrink-0">
                                    <span className={cn("text-[10px] uppercase font-bold px-2 py-0.5 rounded border whitespace-nowrap", getPriorityColor(insight.priority))}>
                                        {insight.priority}
                                    </span>
                                    {expanded === i ? <ChevronUp className="w-4 h-4 text-zinc-500" /> : <ChevronDown className="w-4 h-4 text-zinc-500" />}
                                </div>
                            </div>
                        </div>

                        {expanded === i && (
                            <div className="px-4 pb-4 pt-0 pl-12 animate-in fade-in slide-in-from-top-1 duration-200">
                                <div className="border-t border-white/5 my-3"></div>
                                <p className="text-[10px] font-bold text-zinc-500 uppercase tracking-wider mb-2">Failed User Queries:</p>
                                <div className="space-y-2 mb-4">
                                    {insight.sample_queries.map((q, idx) => (
                                        <div key={idx} className="flex items-center justify-between text-xs text-zinc-300 bg-white/5 px-2 py-1.5 rounded border border-white/5 font-mono group">
                                            <span>"{q}"</span>
                                            <button
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    onResolve(q);
                                                }}
                                                className="opacity-0 group-hover:opacity-100 p-1 hover:bg-blue-500/20 text-blue-400 rounded transition-all"
                                                title="Fix this query"
                                            >
                                                <Plus className="w-3 h-3" />
                                            </button>
                                        </div>
                                    ))}
                                </div>
                                <button
                                    onClick={() => onResolve(insight.topic)} // Fallback if they want to fix the topic
                                    className="w-full py-2 text-xs font-medium bg-blue-500/10 text-blue-400 hover:bg-blue-500/20 border border-blue-500/20 rounded flex items-center justify-center gap-2 transition-colors active:scale-[0.99]"
                                >
                                    <Plus className="w-3 h-3" /> Add General Knowledge to Fix
                                </button>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
}
