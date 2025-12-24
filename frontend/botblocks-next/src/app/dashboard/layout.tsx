import { Sidebar } from "@/components/Sidebar";
import { UserButton } from "@clerk/nextjs";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 flex">
      <Sidebar />
      <main className="flex-1 ml-64">
        {/* Top Header */}
        <header className="flex justify-end items-center p-6 border-b border-white/5">
          <UserButton showName />
        </header>
        {/* Main Content */}
        <div className="p-8">
          {children}
        </div>
      </main>
    </div>
  );
}