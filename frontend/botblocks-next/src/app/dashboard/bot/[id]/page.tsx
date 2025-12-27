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