"use client";

import { useEffect, useState } from "react";
import { getComprehensiveAnalytics, refreshAIInsights, resolveGap } from "@/lib/api";
import { ComprehensiveAnalytics } from "@/lib/types/analytics";
import {
    HealthScoreWidget,
    KnowledgeGapStats,
    AIInsightsList,
    RecentGapsList,
    TopFailedQueriesChart
} from "@/components/analytics";
import { Skeleton } from "@/components/ui/Skeleton";
import { toast } from "sonner";
import { AlertCircle, RefreshCw, X, Check, Loader2 } from "lucide-react";
import { useAuth } from "@clerk/nextjs";

interface AnalyticsViewProps {
    botId: string;
}

export default function AnalyticsView({ botId }: AnalyticsViewProps) {
    const { getToken } = useAuth();
    const [analytics, setAnalytics] = useState<ComprehensiveAnalytics | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [refreshing, setRefreshing] = useState(false);

    // Resolution State
    const [resolvingQuery, setResolvingQuery] = useState<string | null>(null);
    const [resolutionAnswer, setResolutionAnswer] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);

    const fetchAnalytics = async () => {
        setLoading(true);
        setError(null);
        console.log("📊 Fetching analytics for bot:", botId);
        try {
            const token = await getToken();
            const data = await getComprehensiveAnalytics(botId, token);
            console.log("✅ Analytics loaded:", data);
            setAnalytics(data);
        } catch (err) {
            console.error("❌ Failed to fetch analytics:", err);
            setError("Failed to load analytics data. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    const handleRefreshInsights = async () => {
        setRefreshing(true);
        console.log("🔄 Refreshing AI insights...");
        try {
            const token = await getToken();
            const data = await refreshAIInsights(botId, token);
            console.log("✨ Insights refreshed:", data);
            setAnalytics(data);
            toast.success("AI Insights refreshed!");
        } catch (err) {
            console.error("❌ Failed to refresh insights:", err);
            toast.error("Failed to refresh insights");
        } finally {
            setRefreshing(false);
        }
    };

    const handleOpenResolution = (query: string) => {
        setResolvingQuery(query);
        setResolutionAnswer("");
    };

    const handleSubmitResolution = async () => {
        if (!resolvingQuery || !resolutionAnswer.trim()) return;

        setIsSubmitting(true);
        try {
            const token = await getToken();
            const result = await resolveGap(botId, resolvingQuery, resolutionAnswer, undefined, token);
            toast.success("Knowledge added & gap resolved!");

            // Close modal
            setResolvingQuery(null);
            setResolutionAnswer("");

            // Optimistically update or re-fetch
            // Re-fetching is safer to get the new Health Score correctly
            fetchAnalytics();

        } catch (err) {
            console.error("Failed to resolve gap:", err);
            toast.error("Failed to resolve gap. Please try again.");
        } finally {
            setIsSubmitting(false);
        }
    };

    useEffect(() => {
        if (botId) {
            fetchAnalytics();
        }
    }, [botId]);

    if (loading) {
        return (
            <div className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <Skeleton className="h-[280px] w-full rounded-xl bg-zinc-800/50" />
                    <Skeleton className="h-[280px] w-full rounded-xl md:col-span-2 bg-zinc-800/50" />
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <Skeleton className="h-[400px] w-full rounded-xl bg-zinc-800/50" />
                    <Skeleton className="h-[400px] w-full rounded-xl bg-zinc-800/50" />
                </div>
                <Skeleton className="h-[300px] w-full rounded-xl bg-zinc-800/50" />
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex flex-col items-center justify-center p-12 bg-zinc-900 border border-white/5 rounded-xl">
                <AlertCircle className="w-12 h-12 text-red-500 mb-4" />
                <h3 className="text-xl font-bold text-white mb-2">Error Loading Analytics</h3>
                <p className="text-zinc-400 mb-6">{error}</p>
                <button
                    onClick={fetchAnalytics}
                    className="flex items-center gap-2 bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-500 transition-colors"
                >
                    <RefreshCw className="w-4 h-4" /> Try Again
                </button>
            </div>
        );
    }

    if (!analytics) return null;

    return (
        <div className="space-y-6 animate-in fade-in duration-500 relative">
            {/* Top Row: Health & Key Stats */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-1">
                    <HealthScoreWidget score={analytics.health_score} />
                </div>
                <div className="lg:col-span-2">
                    <KnowledgeGapStats stats={analytics.stats} />
                </div>
            </div>

            {/* Middle Row: Charts & Lists */}
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                <TopFailedQueriesChart data={analytics.top_failed_queries} />
                <RecentGapsList gaps={analytics.recent_gaps} onResolve={handleOpenResolution} />
            </div>

            {/* Bottom Row: AI Insights */}
            <div className="grid grid-cols-1">
                <AIInsightsList
                    insights={analytics.ai_insights}
                    onRefresh={handleRefreshInsights}
                    refreshing={refreshing}
                    onResolve={handleOpenResolution}
                />
            </div>

            <div className="text-center text-xs text-zinc-600 mt-8 font-mono">
                Last generated: {new Date(analytics.generated_at).toLocaleString()}
            </div>

            {/* Resolution Modal Overlay */}
            {resolvingQuery && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 animate-in fade-in duration-200">
                    <div className="w-full max-w-lg bg-zinc-900 border border-white/10 rounded-xl shadow-2xl overflow-hidden scale-100 animate-in zoom-in-95 duration-200">
                        <div className="p-6">
                            <div className="flex items-center justify-between mb-6">
                                <h3 className="text-lg font-bold text-white">Resolve Knowledge Gap</h3>
                                <button
                                    onClick={() => setResolvingQuery(null)}
                                    className="text-zinc-400 hover:text-white transition-colors"
                                >
                                    <X className="w-5 h-5" />
                                </button>
                            </div>

                            <div className="space-y-4">
                                <div className="space-y-2">
                                    <label className="text-xs font-medium text-zinc-400 uppercase">Context / User Asked:</label>
                                    <input
                                        type="text"
                                        value={resolvingQuery}
                                        onChange={(e) => setResolvingQuery(e.target.value)}
                                        className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white font-mono text-sm focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50"
                                    />
                                </div>

                                <div className="space-y-2">
                                    <label className="text-xs font-medium text-zinc-400 uppercase">Teach the Bot (Ideal Answer):</label>
                                    <textarea
                                        value={resolutionAnswer}
                                        onChange={(e) => setResolutionAnswer(e.target.value)}
                                        placeholder="Type the correct answer here..."
                                        className="w-full h-32 px-4 py-3 bg-black/40 border border-white/10 rounded-lg text-white placeholder:text-zinc-600 focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50 resize-none text-sm"
                                        autoFocus
                                    />
                                </div>
                            </div>
                        </div>

                        <div className="bg-white/5 p-4 flex justify-between items-center">
                            <button
                                onClick={() => setResolvingQuery(null)}
                                className="px-4 py-2 text-sm font-medium text-zinc-400 hover:text-white transition-colors"
                            >
                                Cancel
                            </button>
                            <button
                                onClick={handleSubmitResolution}
                                disabled={!resolutionAnswer.trim() || isSubmitting}
                                className="px-6 py-2 bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium rounded-lg transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {isSubmitting ? (
                                    <>
                                        <Loader2 className="w-4 h-4 animate-spin" /> Resolving...
                                    </>
                                ) : (
                                    <>
                                        <Check className="w-4 h-4" /> Resolve & Fix
                                    </>
                                )}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
