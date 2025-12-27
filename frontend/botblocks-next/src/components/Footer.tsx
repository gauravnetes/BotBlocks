import Link from "next/link";
import { Twitter, Linkedin, ShieldCheck, Lock, Instagram, Youtube } from "lucide-react";

export function Footer() {
    return (
        <footer className="relative h-[60vh] border-t border-white/5 bg-black px-10 pt-20 pb-10 overflow-hidden">
            {/* Watermark */}
            <div className="absolute -bottom-10 left-1/2 -translate-x-1/2 w-full text-center pointer-events-none select-none overflow-hidden">
                <span className="text-[13rem] md:text-[15rem] text-white font-bold text-transparent leading-none [-webkit-text-stroke:1px_rgba(255,255,255,0.05)] opacity-100">
                    BotBlocks
                </span>
            </div>

            <div className="container relative z-10 mx-auto  md-10 px-6">
                <div className="flex flex-col lg:flex-row justify-between gap-16 lg:gap-24 mb-20">

                    {/* Brand Column */}
                    <div className="flex flex-col items-start space-y-8 max-w-sm">
                        <div className="space-y-4">
                            <div className="flex items-center gap-2 text-white font-bold text-2xl">
                                <div className="w-8 h-8 bg-white text-black rounded-lg flex items-center justify-center font-black">B</div>
                                BotBlocks
                            </div>
                            <p className="text-zinc-500 text-sm">© 2025 BotBlocks, Inc.</p>
                        </div>

                        {/* Contact & Socials */}
                        <div className="flex items-center gap-4">
                            <button className="bg-white text-black px-6 py-2.5 rounded-lg font-bold text-sm hover:bg-zinc-200 transition-colors">
                                Contact
                            </button>
                            <div className="flex gap-2">
                                <Link href="#" className="w-10 h-10 flex items-center justify-center border border-zinc-800 rounded-lg text-white hover:border-zinc-600 transition-all bg-zinc-950">
                                    <Linkedin className="w-4 h-4" />
                                </Link>
                                <Link href="#" className="w-10 h-10 flex items-center justify-center border border-zinc-800 rounded-lg text-white hover:border-zinc-600 transition-all bg-zinc-950">
                                    <Instagram className="w-4 h-4" />
                                </Link>
                                <Link href="#" className="w-10 h-10 flex items-center justify-center border border-zinc-800 rounded-lg text-white hover:border-zinc-600 transition-all bg-zinc-950">
                                    <Twitter className="w-4 h-4" />
                                </Link>
                                <Link href="#" className="w-10 h-10 flex items-center justify-center border border-zinc-800 rounded-lg text-white hover:border-zinc-600 transition-all bg-zinc-950">
                                    <Youtube className="w-4 h-4" />
                                </Link>
                            </div>
                        </div>

                       
                    </div>

                    {/* Links Columns */}
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-12 lg:gap-24">
                        <div>
                            <h3 className="font-bold text-white mb-6 uppercase tracking-wider text-xs">Product</h3>
                            <ul className="space-y-4 text-sm">
                                <li><Link href="#" className="text-zinc-500 hover:text-white transition-colors">Testimonials</Link></li>
                                <li><Link href="#" className="text-zinc-500 hover:text-white transition-colors">Pricing</Link></li>
                                <li><Link href="#" className="text-zinc-500 hover:text-white transition-colors">Security</Link></li>
                                <li><Link href="#" className="text-zinc-500 hover:text-white transition-colors">Changelog</Link></li>
                                <li><Link href="#" className="text-zinc-500 hover:text-white transition-colors">Affiliates</Link></li>
                            </ul>
                        </div>
                        <div>
                            <h3 className="font-bold text-white mb-6 uppercase tracking-wider text-xs">Resources</h3>
                            <ul className="space-y-4 text-sm">
                                <li><Link href="#" className="text-zinc-500 hover:text-white transition-colors">Contact us</Link></li>
                                <li><Link href="#" className="text-zinc-500 hover:text-white transition-colors">API</Link></li>
                                <li><Link href="#" className="text-zinc-500 hover:text-white transition-colors">Guide</Link></li>
                                <li><Link href="#" className="text-zinc-500 hover:text-white transition-colors">Blog</Link></li>
                            </ul>
                        </div>
                        <div>
                            <h3 className="font-bold text-white mb-6 uppercase tracking-wider text-xs">Company</h3>
                            <ul className="space-y-4 text-sm">
                                <li><Link href="#" className="text-zinc-500 hover:text-white transition-colors">Careers</Link></li>
                                <li><Link href="#" className="text-zinc-500 hover:text-white transition-colors">Privacy policy</Link></li>
                                <li><Link href="#" className="text-zinc-500 hover:text-white transition-colors">Terms of service</Link></li>
                                <li><Link href="#" className="text-zinc-500 hover:text-white transition-colors">DPA</Link></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </footer>
    );
}