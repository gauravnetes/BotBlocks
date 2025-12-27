'use client'
import { Database, Settings, Rocket } from "lucide-react";
import FlowingMenu from "./ui/FlowingMenu";
import MagicBento from "./ui/MagicBento";

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

const demoItems = [
    { link: '/dashboard', text: 'Dashboard', image: 'https://picsum.photos/600/400?random=1' },
    { link: '/pricing', text: 'Pricing', image: 'https://picsum.photos/600/400?random=2' },
    { link: '/docs', text: 'Documentation', image: 'https://picsum.photos/600/400?random=3' },
    { link: '/blog', text: 'Blog', image: 'https://picsum.photos/600/400?random=4' }
];

export function Features() {
    return (
        <div id="features" className="relative z-10">

            {/* 1. Bento Grid with Side Text - BENTO LEFT, TEXT RIGHT */}
            <section className="py-24">
                <div className="container mx-auto px-6 max-w-full">
                    <div className="grid grid-cols-1 xl:grid-cols-12 gap-8 items-center">

                        {/* Left Side - Bento Grid */}
                        <div className="xl:col-span-7 flex justify-center">
                            <MagicBento
                                textAutoHide={true}
                                enableStars={true}
                                enableSpotlight={true}
                                enableBorderGlow={true}
                                enableTilt={true}
                                enableMagnetism={true}
                                clickEffect={true}
                                spotlightRadius={300}
                                particleCount={12}
                                glowColor="99, 102, 241"
                            />
                        </div>

                        {/* Right Side - Text Content */}
                        <div className="xl:col-span-5">
                            <span className="text-indigo-400 font-semibold tracking-wider text-sm uppercase mb-4 block">
                                Platform Capabilities
                            </span>
                            <h2 className="text-4xl lg:text-5xl font-bold text-white mb-6 leading-tight">
                                Everything You Need to Build Your AI Agents
                            </h2>
                            <p className="text-zinc-400 text-lg leading-relaxed mb-6">
                                BotBlocks gives you the complete toolkit to create, train, and deploy intelligent chatbots that truly understand your business.
                            </p>
                            <p className="text-zinc-500 text-base leading-relaxed mb-8">
                                From analytics to automation, our platform covers every aspect of building conversational AI.
                                Connect your data sources, customize behavior, integrate with your favorite tools, and maintain enterprise-grade security — all in one place.
                            </p>
                            <div className="flex flex-wrap gap-3">
                                <span className="px-4 py-2 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-sm font-medium">
                                     Instant Domain Scraping
                                </span>
                                <span className="px-4 py-2 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-sm font-medium">
                                     Zero-Code Deployment
                                </span>
                                <span className="px-4 py-2 rounded-full bg-orange-500/10 border border-orange-500/20 text-orange-300 text-sm font-medium">
                                    Private Data Silos
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </section>


            {/* 2. Core Features - "How it Works" Grid */}
            <section className="py-24 border-t border-white/5">
                <div className="container mx-auto px-6 max-w-6xl">
                    <div className="text-center mb-16 max-w-3xl mx-auto">
                        <span className="text-emerald-400 font-semibold tracking-wider text-sm uppercase mb-4 block">
                            Simple Workflow
                        </span>
                        <h2 className="text-4xl lg:text-5xl font-bold text-white mb-6">
                            From Data to Intelligence
                        </h2>
                        <p className="text-zinc-400 text-lg leading-relaxed">
                            Import your data, configure your agent, and deploy anywhere in three simple steps.
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        {features.map((f, i) => (
                            <div key={i} className="group bg-zinc-900/50 border border-white/5 p-8 rounded-3xl hover:bg-zinc-800/50 hover:border-indigo-500/30 transition-all duration-300">
                                <div className="w-16 h-16 bg-zinc-800 rounded-2xl flex items-center justify-center mb-6 text-white border border-white/5 group-hover:scale-110 group-hover:bg-indigo-500 transition-all mx-auto">
                                    <f.icon className="w-8 h-8" />
                                </div>
                                <div className="text-center mb-4">
                                    <div className="text-sm text-indigo-400 font-bold mb-2">Step {i + 1}</div>
                                    <h3 className="text-xl font-bold text-white mb-3">{f.title}</h3>
                                </div>
                                <p className="text-zinc-400 leading-relaxed text-sm text-center">{f.desc}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* 3. Visual Showcase - Flowing Menu */}
            <section className="py-10 border-t border-white/5">
                <div className="container mx-auto px-6 max-w-full">
                    <div className="text-center mb-12">
                        <span className="text-orange-400 font-semibold tracking-wider text-sm uppercase mb-3 block">
                            Quick Links
                        </span>
                        <h2 className="text-3xl font-bold text-white mb-3">Explore More</h2>
                        <p className="text-zinc-400 text-base max-w-xl mx-auto">
                            Navigate through different sections of the platform
                        </p>
                    </div>
                    <div style={{ height: '400px', position: 'relative' }} className="w-full">
                        <FlowingMenu items={demoItems} />
                    </div>
                </div>
            </section>

        </div>
    );
}