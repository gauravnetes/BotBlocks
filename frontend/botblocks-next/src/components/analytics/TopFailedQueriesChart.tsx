"use client";

import React from "react";
import { FailedQuery } from "@/lib/types/analytics";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";

interface TopFailedQueriesChartProps {
    data: FailedQuery[];
}

export function TopFailedQueriesChart({ data }: TopFailedQueriesChartProps) {
    if (!data.length) {
        return (
            <div className="bg-zinc-900/50 border border-white/5 rounded-xl p-6 h-96 flex items-center justify-center animate-in fade-in duration-500">
                <p className="text-zinc-500">No failed queries recorded yet.</p>
            </div>
        );
    }

    // Sort and limit
    const chartData = [...data]
        .sort((a, b) => b.frequency - a.frequency)
        .slice(0, 5)
        .map(d => ({
            ...d,
            shortQuery: d.query.length > 25 ? d.query.substring(0, 25) + "..." : d.query
        }));

    return (
        <div className="bg-zinc-900/50 border border-white/5 rounded-xl p-6 hover:border-white/10 transition-colors">
            <h3 className="text-lg font-bold text-white mb-6">Top Failed Queries</h3>

            {/* Chart */}
            <div className="h-64 mb-6">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData} layout="vertical" margin={{ left: 0, right: 20 }}>
                        <XAxis type="number" hide />
                        <YAxis
                            type="category"
                            dataKey="shortQuery"
                            width={140}
                            tick={{ fill: '#a1a1aa', fontSize: 12, fontWeight: 500 }}
                            axisLine={false}
                            tickLine={false}
                        />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#18181b', border: '1px solid #27272a', borderRadius: '8px', color: '#fff', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}
                            cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                        />
                        <Bar dataKey="frequency" radius={[0, 4, 4, 0]} barSize={24} animationDuration={1000}>
                            {chartData.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={index === 0 ? '#ef4444' : '#3b82f6'} />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </div>

            {/* Table */}
            <div className="overflow-x-auto">
                <table className="w-full text-sm text-left">
                    <thead className="text-xs text-zinc-500 uppercase bg-white/5">
                        <tr>
                            <th className="px-4 py-2 rounded-l-lg font-semibold tracking-wider">Query</th>
                            <th className="px-4 py-2 text-right rounded-r-lg font-semibold tracking-wider">Count</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-white/5">
                        {chartData.map((row, i) => (
                            <tr key={i} className="hover:bg-white/5 transition-colors group">
                                <td className="px-4 py-3 text-zinc-400 group-hover:text-zinc-200 transition-colors w-full">{row.query}</td>
                                <td className="px-4 py-3 text-right font-mono text-white font-medium">{row.frequency}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
