
import { Skeleton } from "@/components/ui/Skeleton"

export default function DashboardLoading() {
    return (
        <div>
            <div className="flex justify-between items-center mb-8">
                <div>
                    <Skeleton className="h-10 w-48 mb-2 bg-zinc-800" />
                    <Skeleton className="h-4 w-64 bg-zinc-800/50" />
                </div>
                <Skeleton className="h-10 w-32 rounded-lg bg-zinc-800" />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {[1, 2, 3].map((i) => (
                    <div key={i} className="bg-zinc-900/50 border border-white/5 rounded-xl p-6 h-[200px] flex flex-col justify-between">
                        <div className="flex justify-between items-start">
                            <div className="space-y-2">
                                <Skeleton className="h-6 w-32 bg-zinc-800" />
                                <Skeleton className="h-4 w-16 bg-zinc-800/50" />
                            </div>
                            <div className="flex gap-2">
                                <Skeleton className="h-6 w-16 rounded bg-zinc-800" />
                                <Skeleton className="h-6 w-12 rounded bg-zinc-800" />
                            </div>
                        </div>

                        <div className="space-y-2">
                            <Skeleton className="h-4 w-full bg-zinc-800/50" />
                            <Skeleton className="h-4 w-2/3 bg-zinc-800/50" />
                        </div>

                        <div className="grid grid-cols-4 gap-2 mt-4">
                            <Skeleton className="h-9 rounded-lg bg-zinc-800" />
                            <Skeleton className="h-9 rounded-lg bg-zinc-800" />
                            <Skeleton className="h-9 rounded-lg bg-zinc-800" />
                            <Skeleton className="h-9 rounded-lg bg-zinc-800" />
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}
