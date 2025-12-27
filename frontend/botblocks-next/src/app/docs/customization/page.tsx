
export default function CustomizationPage() {
    return (
        <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="border-b border-white/5 pb-8">
                <span className="text-indigo-400 font-bold tracking-wider text-xs uppercase mb-2 block">Guides</span>
                <h1 className="text-3xl md:text-4xl font-black mb-4 tracking-tight">Widget Customization</h1>
                <p className="text-lg text-zinc-400 leading-relaxed">
                    Make the chat widget feel like a native part of your website.
                </p>
            </div>

            <div className="prose prose-invert prose-zinc max-w-none">

                <h3>Visual settings</h3>
                <p>
                    In the <strong>"Settings"</strong> tab of your bot, you can control the look and feel.
                </p>
                <ul className="space-y-4">
                    <li>
                        <strong>Theme:</strong> Choose between available presets like <em>Modern Light</em>, <em>Dark Mode</em>, or <em>Classic</em>.
                    </li>
                    <li>
                        <strong>Brand Color:</strong> Set the primary accent color. This affects the chat bubble, buttons, and links.
                        <div className="flex gap-2 mt-2 not-prose">
                            <div className="w-6 h-6 rounded-full bg-blue-500"></div>
                            <div className="w-6 h-6 rounded-full bg-purple-500"></div>
                            <div className="w-6 h-6 rounded-full bg-emerald-500"></div>
                            <div className="w-6 h-6 rounded-full bg-red-500"></div>
                        </div>
                    </li>
                    <li>
                        <strong>Position:</strong> Toggle between <code>Bottom Right</code> (standard) or <code>Bottom Left</code>.
                    </li>
                </ul>

                <h3>Bot Persona</h3>
                <p>
                    You can also customize how the bot introduces itself.
                </p>
                <div className="bg-zinc-900 border border-white/10 p-6 rounded-xl">
                    <div className="space-y-4">
                        <div>
                            <label className="text-xs uppercase font-bold text-zinc-500 block mb-1">Welcome Message</label>
                            <div className="p-3 bg-black/30 rounded border border-white/5 text-zinc-300 text-sm">
                                "Hi there! 👋 How can I help you with BotBlocks today?"
                            </div>
                        </div>
                        <div>
                            <label className="text-xs uppercase font-bold text-zinc-500 block mb-1">Suggested Questions</label>
                            <div className="flex gap-2">
                                <span className="px-3 py-1 bg-white/5 rounded-full text-xs text-zinc-400 border border-white/5">Pricing?</span>
                                <span className="px-3 py-1 bg-white/5 rounded-full text-xs text-zinc-400 border border-white/5">API Docs?</span>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    );
}
