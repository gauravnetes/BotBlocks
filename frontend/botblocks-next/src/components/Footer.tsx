export function Footer() {
    return (
        <footer className="border-t border-white/5 py-16 bg-zinc-950">
            <div className="container mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-8 text-sm text-zinc-500">
                <div>© 2024 BotBlocks Inc.</div>
                <div className="flex gap-8">
                    <a href="#" className="hover:text-white transition-colors">Privacy</a>
                    <a href="#" className="hover:text-white transition-colors">Terms</a>
                    <a href="#" className="hover:text-white transition-colors">Twitter</a>
                    <a href="#" className="hover:text-white transition-colors">GitHub</a>
                </div>
            </div>
        </footer>
    );
}