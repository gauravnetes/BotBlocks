
export default function QuickStartPage() {
    return (
        <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="border-b border-white/5 pb-8">
                <span className="text-indigo-400 font-bold tracking-wider text-xs uppercase mb-2 block">Getting Started</span>
                <h1 className="text-3xl md:text-4xl font-black mb-4 tracking-tight">Quick Start Guide</h1>
                <p className="text-lg text-zinc-400 leading-relaxed">
                    Get your first intelligent chatbot up and running on BotBlocks in less than 5 minutes.
                </p>
            </div>

            <div className="prose prose-invert prose-zinc max-w-none">

                <ol className="relative border-l border-zinc-800 ml-3 space-y-12">
                    <li className="pl-8 relative">
                        <span className="absolute -left-[17px] top-0 flex items-center justify-center w-9 h-9 bg-zinc-900 rounded-full border-2 border-indigo-500 text-indigo-400 font-bold text-sm">1</span>
                        <h3 className="text-xl font-bold text-white mt-0 mb-2">Create Your Account</h3>
                        <p className="text-zinc-400 mb-4">
                            Sign up for a free account at the <a href="/dashboard" className="text-indigo-400 no-underline hover:underline">BotBlocks Dashboard</a>. No credit card required for the Starter plan.
                        </p>
                    </li>

                    <li className="pl-8 relative">
                        <span className="absolute -left-[17px] top-0 flex items-center justify-center w-9 h-9 bg-zinc-900 rounded-full border-2 border-zinc-700 text-zinc-400 font-bold text-sm">2</span>
                        <h3 className="text-xl font-bold text-white mt-0 mb-2">Create a New Bot</h3>
                        <p className="text-zinc-400 mb-4">
                            Click the <strong>"Create Bot"</strong> button in the top right corner. Give your bot a name (e.g., "My Support Bot") and choose an initial primary color.
                        </p>
                        <div className="bg-black/50 p-4 rounded-lg border border-white/10 font-mono text-sm text-zinc-300">
                            Dashboard &gt; Bots &gt; New Bot
                        </div>
                    </li>

                    <li className="pl-8 relative">
                        <span className="absolute -left-[17px] top-0 flex items-center justify-center w-9 h-9 bg-zinc-900 rounded-full border-2 border-zinc-700 text-zinc-400 font-bold text-sm">3</span>
                        <h3 className="text-xl font-bold text-white mt-0 mb-2">Add Knowledge</h3>
                        <p className="text-zinc-400 mb-4">
                            Your bot starts empty. To make it smart, go to the <strong>"Knowledge"</strong> tab.
                        </p>
                        <ul className="list-disc pl-5 text-zinc-400 space-y-2">
                            <li><strong>Option A (Files):</strong> Drag and drop a PDF manual or text file.</li>
                            <li><strong>Option B (Web):</strong> Enter your website URL to have us crawl it.</li>
                            <li><strong>Option C (Q&A):</strong> Manually add specific Question/Answer pairs.</li>
                        </ul>
                    </li>

                    <li className="pl-8 relative">
                        <span className="absolute -left-[17px] top-0 flex items-center justify-center w-9 h-9 bg-zinc-900 rounded-full border-2 border-zinc-700 text-zinc-400 font-bold text-sm">4</span>
                        <h3 className="text-xl font-bold text-white mt-0 mb-2">Test & Deploy</h3>
                        <p className="text-zinc-400 mb-4">
                            Use the <strong>"Chat"</strong> preview on the right side of the dashboard to test your bot. Ask it questions based on the data you uploaded.
                        </p>
                        <p className="text-zinc-400">
                            Once satisfied, go to the <strong>"Embed"</strong> tab to get the code snippet for your website.
                        </p>
                    </li>
                </ol>

                <div className="bg-indigo-900/20 border-l-4 border-indigo-500 p-4 my-8 rounded-r-lg">
                    <p className="text-indigo-200 m-0 text-sm">
                        <strong>Pro Tip:</strong> It may take a minute or two for large documents to be processed and indexed.
                    </p>
                </div>

            </div>
        </div>
    );
}
