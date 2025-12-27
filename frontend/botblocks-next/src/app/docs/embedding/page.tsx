
export default function EmbeddingPage() {
    return (
        <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="border-b border-white/5 pb-8">
                <span className="text-indigo-400 font-bold tracking-wider text-xs uppercase mb-2 block">Integration</span>
                <h1 className="text-3xl md:text-4xl font-black mb-4 tracking-tight">Website Embedding</h1>
                <p className="text-lg text-zinc-400 leading-relaxed">
                    How to install the BotBlocks widget on your site.
                </p>
            </div>

            <div className="prose prose-invert prose-zinc max-w-none">

                <h3>Universal Embed Code</h3>
                <p>
                    This method works for 99% of websites, including plain HTML, WordPress, Webflow, Shopify, and more.
                </p>
                <div className="bg-[#0d1117] border border-white/10 rounded-xl overflow-hidden mb-6 not-prose">
                    <div className="flex items-center gap-2 px-4 py-2 bg-white/5 border-b border-white/5">
                        <span className="text-xs text-zinc-500 font-mono">HTML / Script</span>
                    </div>
                    <div className="p-4 overflow-x-auto">
                        <pre className="text-sm font-mono text-zinc-300">
                            {`<iframe 
  src="https://botblocks.ai/widget/YOUR_BOT_ID"
  style="position: fixed; bottom: 20px; right: 20px; width: 400px; height: 600px; border: none; z-index: 9999;"
></iframe>`}
                        </pre>
                    </div>
                </div>

                <h3>React / Next.js Integration</h3>
                <p>
                    If you are building a React application, you can simply use an iframe as well, or create a wrapper component.
                </p>
                <div className="bg-[#0d1117] border border-white/10 rounded-xl overflow-hidden mb-6 not-prose">
                    <div className="flex items-center gap-2 px-4 py-2 bg-white/5 border-b border-white/5">
                        <span className="text-xs text-zinc-500 font-mono">ChatWidget.tsx</span>
                    </div>
                    <div className="p-4 overflow-x-auto">
                        <pre className="text-sm font-mono text-zinc-300">
                            {`export function ChatWidget({ botId }) {
  return (
    <iframe
      src={"https://botblocks.ai/widget/" + botId}
      style={{
        position: 'fixed',
        bottom: '20px',
        right: '20px',
        width: '400px',
        height: '600px',
        border: 'none',
        zIndex: 9999
      }}
    />
  );
}`}
                        </pre>
                    </div>
                </div>

            </div>
        </div>
    );
}
