import { getBots } from "@/lib/api";
import { BotCard } from "@/components/BotCard";
import { Plus } from "lucide-react";
import Link from "next/link";
import { auth } from "@clerk/nextjs/server";

export default async function DashboardPage() {
  const { getToken } = await auth();
  const token = await getToken();
  const bots = await getBots(token);
  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-white">Dashboard</h1>
          <p className="text-zinc-400">Manage all your chatbots from one place</p>
        </div>
        <Link
          href="/dashboard/create"
          className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg font-medium transition-colors"
        >
          <Plus className="w-5 h-5" />
          Create New Bot
        </Link>
      </div>
      {bots.length === 0 ? (
        <div className="text-center py-20 border border-dashed border-white/10 rounded-2xl">
          <div className="text-4xl mb-4">🤖</div>
          <h2 className="text-xl font-semibold text-white mb-2">No Bots Yet</h2>
          <p className="text-zinc-400 mb-6">Create your first chatbot to get started!</p>
          <Link
            href="/dashboard/create"
            className="inline-flex items-center gap-2 bg-white text-black px-6 py-2 rounded-lg font-semibold hover:bg-zinc-200 transition-colors"
          >
            Create Bot
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {bots.map((bot) => (
            <BotCard key={bot.public_id} bot={bot} />
          ))}
        </div>
      )}
    </div>
  );
}