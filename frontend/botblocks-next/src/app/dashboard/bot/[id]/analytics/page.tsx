import { Metadata } from "next";
import AnalyticsView from "./AnalyticsView";

export const metadata: Metadata = {
    title: "Bot Analytics | BotBlocks",
    description: "View comprehensive performance metrics and insights for your chatbot.",
};

interface PageProps {
    params: Promise<{ id: string }>;
}

export default async function AnalyticsPage({ params }: PageProps) {
    const resolvedParams = await params;
    return <AnalyticsView botId={resolvedParams.id} />;
}
