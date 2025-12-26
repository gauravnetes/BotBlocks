export interface AnalyticsStats {
    total_queries: number;
    failed_queries: number;
    low_confidence_queries: number;
    success_rate: number;
    avg_confidence: number;
    period_days: number;
}

export interface AIInsight {
    topic: string;
    count: number;
    sample_queries: string[];
    advice: string;
    priority: 'high' | 'medium' | 'low';
}

export interface KnowledgeGap {
    query: string;
    response: string;
    confidence: number;
    timestamp: string;
}

export interface FailedQuery {
    query: string;
    frequency: number;
}

export interface ComprehensiveAnalytics {
    health_score: number;
    stats: AnalyticsStats;
    ai_insights: AIInsight[];
    recent_gaps: KnowledgeGap[];
    top_failed_queries: FailedQuery[];
    generated_at: string;
}
