"use client";
import Link from "next/link";
import { Bot, deleteBot } from "@/lib/api";
import { MessageSquare, Code, Trash2, Loader2 } from "lucide-react";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { useAuth } from "@clerk/nextjs";

export function BotCard({ bot }: { bot: Bot }) {
  const router = useRouter();
  const { getToken } = useAuth();
  const [isDeleting, setIsDeleting] = useState(false);

  const handleDelete = async () => {
    if (!confirm("Are you sure you want to delete this bot?")) return;
    setIsDeleting(true);
    const token = await getToken();
    const success = await deleteBot(bot.public_id, token);
    if (success) {
      router.refresh();
    } else {
      alert("Failed to delete bot");
      setIsDeleting(false);
    }
  };

  return (
    <div className="bg-zinc-900/50 border border-white/5 rounded-xl p-6 hover:border-white/10 transition-colors">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-semibold text-white">{bot.name}</h3>
          <span className="text-xs font-bold text-zinc-950 bg-blue-500 px-2 py-0.5 rounded-sm uppercase mt-1 inline-block">
            Active
          </span>
        </div>
        <div className="flex gap-2">
          {(() => {
            const type = bot.bot_type || "rag";

            return (
              <div className={`text-xs font-bold px-2 py-1 rounded border uppercase ${type === 'persona'
                ? "text-purple-400 border-purple-400/20 bg-purple-400/10"
                : "text-amber-400 border-amber-400/20 bg-amber-400/10"
                }`}>
                {type === 'persona' ? '🎭 Persona' : '📚 RAG'}
              </div>
            );
          })()}
          <div className="text-xs text-zinc-500 font-mono border border-white/5 px-2 py-1 rounded bg-zinc-950 uppercase">
            {bot.platform || "WEB"}
          </div>
        </div>
      </div>

      <p className="text-sm text-zinc-400 mb-6 h-10 line-clamp-2">
        {bot.description || bot.system_prompt || "No description provided."}
      </p>

      <div className="grid grid-cols-3 gap-2">

        <Link
          href={`/dashboard/bot/${bot.public_id}?tab=chat`}
          className="flex items-center justify-center gap-2 py-2 text-sm font-medium text-zinc-300 bg-white/5 rounded-lg hover:bg-white/10 hover:text-white transition-colors"
        >
          <MessageSquare className="w-4 h-4" /> Chat
        </Link>
        <Link
          href={`/dashboard/bot/${bot.public_id}?tab=embed`}
          className="flex items-center justify-center gap-2 py-2 text-sm font-medium text-zinc-300 bg-white/5 rounded-lg hover:bg-white/10 hover:text-white transition-colors"
        >
          <Code className="w-4 h-4" /> Embed
        </Link>
        <button
          onClick={handleDelete}
          disabled={isDeleting}
          className="flex items-center justify-center gap-2 py-2 text-sm font-medium text-zinc-300 bg-white/5 rounded-lg hover:bg-red-500/10 hover:text-red-500 transition-colors disabled:opacity-50"
        >
          {isDeleting ? <Loader2 className="w-4 h-4 animate-spin" /> : <Trash2 className="w-4 h-4" />}
          {isDeleting ? "Deleting..." : "Del"}
        </button>
      </div>
    </div>
  );
}