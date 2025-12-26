import { getBot } from "@/lib/api";
import Link from "next/link";
import { BarChart3, ArrowRight } from "lucide-react";

interface PageProps {
  params: Promise<{ id: string }>;
}

export default async function BotOverviewPage({ params }: PageProps) {
  const resolvedParams = await params;
  const bot = await getBot(resolvedParams.id);

  if (!bot) return <div className="p-8 text-red-400">Bot not found</div>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {/* Analytics Card */}
      <div className="md:col-span-2 lg:col-span-2 bg-gradient-to-br from-zinc-900 to-zinc-900/50 border border-white/5 rounded-xl p-6 relative overflow-hidden group hover:border-white/10 transition-colors">
        <div className="absolute top-0 right-0 p-3 opacity-10 group-hover:opacity-20 transition-opacity">
          <BarChart3 className="w-32 h-32 text-blue-500" />
        </div>
        <div className="relative z-10">
          <h3 className="text-white font-bold text-lg mb-2 flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-blue-500" />
            Performance Analytics
          </h3>
          <p className="text-zinc-400 text-sm mb-6 max-w-sm">
            View detailed insights about your bot&apos;s performance, knowledge gaps, and health score.
          </p>

          <div className="flex items-center gap-4">
            <div className="flex flex-col">
              <span className="text-xs text-zinc-500 uppercase tracking-wider font-bold">Health Score</span>
              <span className="text-2xl font-bold text-white">
                {bot.health_score ? `${Math.round(bot.health_score)}%` : "N/A"}
              </span>
            </div>
            <div className="h-8 w-[1px] bg-white/10"></div>
            <div className="flex flex-col">
              <span className="text-xs text-zinc-500 uppercase tracking-wider font-bold">Last Check</span>
              <span className="text-sm text-zinc-300">
                {bot.last_health_check_at ? new Date(bot.last_health_check_at).toLocaleDateString() : "Never"}
              </span>
            </div>
          </div>

          <Link
            href={`/dashboard/bot/${bot.public_id}/analytics`}
            className="absolute bottom-6 right-6 flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-500 transition-colors shadow-lg shadow-blue-900/20"
          >
            View Analytics <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>

      <div className="bg-zinc-900 border border-white/5 rounded-xl p-6">
        <h3 className="text-zinc-400 text-sm font-bold uppercase mb-4">Status</h3>
        <span className="bg-green-500/10 text-green-500 px-3 py-1 rounded-full text-sm font-bold border border-green-500/20">
          ACTIVE
        </span>
      </div>

      <div className="bg-zinc-900 border border-white/5 rounded-xl p-6">
        <h3 className="text-zinc-400 text-sm font-bold uppercase mb-4">Platform</h3>
        <span className="text-white text-lg font-medium bg-white/5 px-3 py-1 rounded inline-block">
          {bot.platform?.toUpperCase() || "WEB"}
        </span>
      </div>

      <div className="col-span-full bg-zinc-900 border border-white/5 rounded-xl p-6">
        <h3 className="text-zinc-400 text-sm font-bold uppercase mb-4">System Prompt</h3>
        <div className="relative">
          <p className="text-zinc-300 font-mono text-sm bg-black/20 p-4 rounded-lg max-h-40 overflow-y-auto border border-white/5">
            {bot.system_prompt || "No prompt configured."}
          </p>
        </div>
      </div>
    </div>
  );
}