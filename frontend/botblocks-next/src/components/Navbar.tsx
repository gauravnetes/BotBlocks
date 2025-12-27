import Link from "next/link";
import { SignInButton, SignUpButton, SignedIn, SignedOut, UserButton } from "@clerk/nextjs";
import { Zap } from "lucide-react";

export function Navbar() {
    return (
        <nav className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-14 py-6 backdrop-blur-sm">
            <div className="flex items-center gap-2 text-xl font-bold text-white">
                <img src="/logo.png" alt="logo png" className="h-8 w-8" />
                BotBlocks
            </div>
            <div className="flex gap-8 text-sm font-medium text-zinc-400 items-center">
                <Link href="#" className="hover:text-white transition-colors">Product</Link>
                <Link href="#" className="hover:text-white transition-colors">Solutions</Link>
                <Link href="#" className="hover:text-white transition-colors">Pricing</Link>
                <Link href="#" className="hover:text-white transition-colors">Docs</Link>

                <SignedOut>
                    <SignInButton mode="modal">
                        <button className="text-zinc-400 hover:text-white transition-colors">Sign In</button>
                    </SignInButton>
                    <SignUpButton mode="modal">
                        <button className="bg-white text-black px-4 py-2 rounded-lg font-semibold hover:bg-zinc-200 transition-colors">
                            Sign Up
                        </button>
                    </SignUpButton>
                </SignedOut>
                <SignedIn>
                    <UserButton />
                </SignedIn>
            </div>
        </nav>
    );
}