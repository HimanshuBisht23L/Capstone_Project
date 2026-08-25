import "./globals.css";
import Link from "next/link";

export const metadata = {
  title: "SheetPilot AI — Voice-Powered Spreadsheet Automation Platform",
  description: "Natural Language AI Spreadsheet Automation Engine powered by Python Pandas & AST Sandboxing",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#090d16] text-slate-100 antialiased selection:bg-cyan-500 selection:text-white flex flex-col min-h-screen">
        {/* Top Header Navigation */}
        <header className="sticky top-0 z-50 glass-panel border-b border-white/10 px-6 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-3 group">
            <div className="h-9 w-9 rounded-xl bg-gradient-to-tr from-cyan-500 via-indigo-500 to-purple-500 flex items-center justify-center font-bold text-white shadow-lg shadow-cyan-500/20 group-hover:scale-105 transition">
              📊
            </div>
            <div>
              <h1 className="text-xl font-extrabold tracking-tight gradient-text">
                SheetPilot AI
              </h1>
              <p className="text-[11px] text-slate-400 font-medium">
                Voice & Spreadsheet Automation
              </p>
            </div>
          </Link>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center gap-6 text-sm font-medium text-slate-300">
            <Link href="/" className="hover:text-cyan-400 transition">
              Home
            </Link>
            <Link href="/workspace" className="hover:text-cyan-400 transition">
              Workspace Studio
            </Link>
            <a
              href="http://localhost:8501"
              target="_blank"
              rel="noreferrer"
              className="hover:text-cyan-400 transition flex items-center gap-1"
            >
              Control Room ↗
            </a>
          </nav>

          <div className="flex items-center gap-4">
            <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-xs font-semibold text-emerald-400">
              <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
              AST Security Active
            </div>
            <Link
              href="/workspace"
              className="px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white font-bold text-xs shadow-md shadow-cyan-500/20 transition"
            >
              🚀 Launch Studio
            </Link>
          </div>
        </header>

        {/* Main View Area */}
        <main className="flex-1">
          {children}
        </main>

        {/* Footer */}
        <footer className="border-t border-slate-800/80 py-8 px-6 text-center text-xs text-slate-500 bg-slate-950/60">
          <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <p>© 2026 SheetPilot AI. Powered by Python Pandas, FastAPI & AST Sandboxing.</p>
            <div className="flex items-center gap-4">
              <Link href="/" className="hover:text-slate-400">Home</Link>
              <Link href="/workspace" className="hover:text-slate-400">Workspace</Link>
              <a href="http://localhost:8501" target="_blank" rel="noreferrer" className="hover:text-slate-400">Control Room</a>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
