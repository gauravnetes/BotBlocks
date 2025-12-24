import Link from "next/link";
import { SignOutButton } from "@clerk/nextjs";
import { Zap, LayoutDashboard, PlusCircle, Settings, LogOut } from "lucide-react";

export function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 bottom-0 w-64 bg-zinc-900 border-r border-white/5 flex flex-col">
      <div className="p-6 flex items-center gap-2 text-xl font-bold text-white border-b border-white/5">
        <Zap className="h-6 w-6 text-blue-500" fill="currentColor" />
        BotBlocks
      </div>

      <nav className="flex-1 p-4 space-y-2">
        <Link href="/dashboard" className="flex items-center gap-3 px-4 py-3 text-zinc-100 bg-white/5 rounded-lg border border-white/5">
          <LayoutDashboard className="w-5 h-5" />
          Dashboard
        </Link>
        <Link href="/dashboard/create" className="flex items-center gap-3 px-4 py-3 text-zinc-400 hover:text-white hover:bg-white/5 rounded-lg transition-colors">
          <PlusCircle className="w-5 h-5" />
          Create Bot
        </Link>
        <Link href="/dashboard/settings" className="flex items-center gap-3 px-4 py-3 text-zinc-400 hover:text-white hover:bg-white/5 rounded-lg transition-colors">
          <Settings className="w-5 h-5" />
          Settings
        </Link>
      </nav>

      <div className="p-4 border-t border-white/5">
        <SignOutButton>
          <button className="flex items-center gap-3 px-4 py-3 text-zinc-400 hover:text-red-400 w-full transition-colors">
            <LogOut className="w-5 h-5" />
            Sign Out
          </button>
        </SignOutButton>
      </div>
    </aside>
  );
}