
export default function ApiReferencePage() {
    return (
        <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="border-b border-white/5 pb-8">
                <span className="text-indigo-400 font-bold tracking-wider text-xs uppercase mb-2 block">Developers</span>
                <h1 className="text-3xl md:text-4xl font-black mb-4 tracking-tight">API Reference</h1>
                <p className="text-lg text-zinc-400 leading-relaxed">
                    Interact with your bots programmatically using our REST API.
                </p>
            </div>

            <div className="prose prose-invert prose-zinc max-w-none">

                <div className="bg-yellow-500/10 border border-yellow-500/20 rounded-lg p-4 mb-8">
                    <p className="text-yellow-200 text-sm m-0">
                        <strong>Note:</strong> API access is currently in Beta. Please contact support to generate an API Key.
                    </p>
                </div>

                <h3>Authentication</h3>
                <p>
                    All API requests must include your API key in the header.
                </p>
                <div className="bg-[#0d1117] border border-white/10 rounded-lg p-4 font-mono text-sm text-zinc-300 not-prose mb-8">
                    Authorization: Bearer YOUR_API_KEY
                </div>

                <hr className="border-white/5" />

                <h3>Endpoints</h3>

                <div className="space-y-12">

                    {/* Endpoint 1 */}
                    <div>
                        <div className="flex items-center gap-3 mb-4">
                            <span className="px-2 py-1 bg-green-500/20 text-green-400 font-bold text-xs rounded border border-green-500/30">POST</span>
                            <code className="text-zinc-200 font-mono">/v1/chat/completions</code>
                        </div>
                        <p className="text-zinc-400 mb-4">
                            Send a message to a bot and get a response.
                        </p>

                        <div className="bg-[#0d1117] border border-white/10 rounded-xl overflow-hidden not-prose">
                            <div className="flex items-center gap-2 px-4 py-2 bg-white/5 border-b border-white/5">
                                <span className="text-xs text-zinc-500 font-mono">Request Body</span>
                            </div>
                            <div className="p-4 overflow-x-auto">
                                <pre className="text-sm font-mono text-zinc-300">
                                    {`{
  "bot_id": "7334ea7a...",
  "messages": [
    { "role": "user", "content": "How do I reset my password?" }
  ]
}`}
                                </pre>
                            </div>
                        </div>
                    </div>

                    {/* Endpoint 2 */}
                    <div>
                        <div className="flex items-center gap-3 mb-4">
                            <span className="px-2 py-1 bg-blue-500/20 text-blue-400 font-bold text-xs rounded border border-blue-500/30">GET</span>
                            <code className="text-zinc-200 font-mono">/v1/bots</code>
                        </div>
                        <p className="text-zinc-400 mb-4">
                            List all bots associated with your account.
                        </p>
                    </div>

                </div>

            </div>
        </div>
    );
}
