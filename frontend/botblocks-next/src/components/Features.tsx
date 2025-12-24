import { Database, Settings, Rocket } from "lucide-react";

const features = [
    {
        icon: Database,
        title: "Connect Data",
        desc: "Upload PDFs, connect Notion, or crawl your website. We ingest and index everything automatically.",
    },
    {
        icon: Settings,
        title: "Customize",
        desc: "Define the personality, tone, and strictness. Make the bot sound exactly like your brand.",
    },
    {
        icon: Rocket,
        title: "Deploy",
        desc: "Get an embed code for your site or connect directly to Slack, Discord, and Telegram.",
    },
];

export function Features() {
    return (
        <section className="py-32 container mx-auto px-6">
            <div className="text-center mb-16">
                <h2 className="text-4xl font-bold text-white mb-4">How BotBlocks Works</h2>
                <p className="text-zinc-400 max-w-2xl mx-auto">
                    From raw data to intelligent conversation in three simple steps.
                </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {features.map((f, i) => (
                    <div key={i} className="bg-white/5 border border-white/5 p-8 rounded-2xl hover:bg-white/10 transition-colors">
                        <div className="w-12 h-12 bg-zinc-800 rounded-xl flex items-center justify-center mb-6 text-white border border-white/5">
                            <f.icon className="w-6 h-6" />
                        </div>
                        <h3 className="text-xl font-semibold text-white mb-3">{f.title}</h3>
                        <p className="text-zinc-400 leading-relaxed">{f.desc}</p>
                    </div>
                ))}
            </div>
        </section>
    );
}