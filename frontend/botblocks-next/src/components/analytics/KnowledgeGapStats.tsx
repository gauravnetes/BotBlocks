"use client";

import React from "react";
import { AnalyticsStats } from "@/lib/types/analytics";
import { Activity, Target, AlertTriangle, TrendingUp } from "lucide-react";

interface KnowledgeGapStatsProps {
    stats: AnalyticsStats;
}

export function KnowledgeGapStats({ stats }: KnowledgeGapStatsProps) {
    const cards = [
        {
            label: "Total Queries",
            value: stats.total_queries,
            icon: Activity,
            color: "text-blue-400",
            bg: "bg-blue-500/10 border-blue-500/20",
        },
        {
            label: "Success Rate",
            value: `${stats.success_rate.toFixed(1)}%`,
            icon: Target,
            color: "text-green-400",
            bg: "bg-green-500/10 border-green-500/20",
        },
        {
            label: "Failed Queries",
            value: stats.failed_queries,
            icon: AlertTriangle,
            color: "text-red-400",
            bg: "bg-red-500/10 border-red-500/20",
        },
        {
            label: "Avg Confidence",
            value: `${(stats.avg_confidence * 100).toFixed(1)}%`,
            icon: TrendingUp,
            color: "text-purple-400",
            bg: "bg-purple-500/10 border-purple-500/20",
        },
    ];

    return (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 h-full">
            {cards.map((card, i) => (
                <div
                    key={i}
                    className="bg-zinc-900/50 border border-white/5 rounded-xl p-5 flex items-center justify-between hover:border-white/10 transition-all duration-300 group"
                >
                    <div>
                        <p className="text-zinc-400 text-sm mb-1 font-medium">{card.label}</p>
                        <p className="text-2xl font-bold text-white group-hover:scale-105 transition-transform origin-left">{card.value}</p>
                    </div>
                    <div className={`p-3 rounded-lg border ${card.bg} group-hover:bg-opacity-80 transition-colors`}>
                        <card.icon className={`w-5 h-5 ${card.color}`} />
                    </div>
                </div>
            ))}
        </div>
    );
}
