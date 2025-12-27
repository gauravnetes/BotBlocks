import { Navbar } from "@/components/Navbar";
import { Hero } from "@/components/Hero";
import { Footer } from "@/components/Footer";
import { Features } from "@/components/Features";
import { LandingBot } from "@/components/LandingBot";

export default function Home() {
  return (
    <main className="min-h-screen overflow-hidden bg-zinc-950 bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:30px_30px]">
      <Navbar />
      <Hero />
      <LandingBot />
      <Features />
      <Footer />
    </main>
  );
}