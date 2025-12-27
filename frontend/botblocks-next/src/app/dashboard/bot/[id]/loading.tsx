
import { Skeleton } from "@/components/ui/Skeleton"

export default function BotOverviewLoading() {
    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-in fade-in duration-500">

            {/* Status Card Skeleton */}
            <div className="bg-zinc-900 border border-white/5 rounded-xl p-6 h-32 flex flex-col justify-between">
                <Skeleton className="h-4 w-24 bg-zinc-800" />
                <Skeleton className="h-8 w-20 rounded-full bg-zinc-800" />
            </div>

            {/* Platform Card Skeleton */}
            <div className="bg-zinc-900 border border-white/5 rounded-xl p-6 h-32 flex flex-col justify-between">
                <Skeleton className="h-4 w-24 bg-zinc-800" />
                <Skeleton className="h-8 w-16 rounded bg-zinc-800" />
            </div>

            {/* Placeholder for potential 3rd column or spacing */}
            <div className="hidden lg:block bg-zinc-900/0 p-6 h-32"></div>

            {/* System Prompt Skeleton */}
            <div className="col-span-full bg-zinc-900 border border-white/5 rounded-xl p-6 h-64">
                <Skeleton className="h-4 w-32 mb-4 bg-zinc-800" />
                <div className="space-y-3">
                    <Skeleton className="h-4 w-full bg-zinc-800/50" />
                    <Skeleton className="h-4 w-full bg-zinc-800/50" />
                    <Skeleton className="h-4 w-3/4 bg-zinc-800/50" />
                </div>
            </div>
        </div>
    )
}
