import "./globals.css";
import Link from "next/link";
import { Sparkles, ExternalLink, ShieldCheck, Terminal } from "lucide-react";

export const metadata = {
  title: "SheetPilot AI — Voice-Powered Spreadsheet Automation Platform",
  description: "Natural Language AI Spreadsheet Automation Engine powered by Python Pandas & AST Sandboxing",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#07090e] text-slate-100 antialiased selection:bg-cyan-500 selection:text-white flex flex-col min-h-screen">
        {/* Top Header Navigation */}
        <header className="sticky top-0 z-50 bg-[#07090e]/80 backdrop-blur-xl border-b border-white/10 px-4 sm:px-8 py-3.5 flex items-center justify-between transition-all">
          <Link href="/" className="flex items-center gap-3 group">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-cyan-500 via-indigo-500 to-purple-600 p-[1px] shadow-lg shadow-cyan-500/20 group-hover:scale-105 transition duration-300">
              <div className="h-full w-full bg-[#0d121e] rounded-[11px] flex items-center justify-center font-bold text-cyan-400 text-lg">
                📊
              </div>
            </div>
            <div className="flex flex-col">
              <div className="flex items-center gap-2">
                <span className="text-xl font-extrabold tracking-tight gradient-text">
                  SheetPilot AI
                </span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-300 border border-cyan-500/30">
                  v1.0
                </span>
              </div>
              <p className="text-[11px] text-slate-400 font-medium">
                Voice & Spreadsheet Intelligence
              </p>
            </div>
          </Link>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-300">
            <Link href="/" className="hover:text-cyan-400 transition-colors flex items-center gap-1.5">
              <span>Home</span>
            </Link>
            <Link href="/workspace" className="hover:text-cyan-400 transition-colors flex items-center gap-1.5">
              <Sparkles className="h-3.5 w-3.5 text-indigo-400" />
              <span>Workspace Studio</span>
            </Link>
            <a
              href="https://sheetpilotai.streamlit.app/"
              target="_blank"
              rel="noreferrer"
              className="hover:text-cyan-400 transition-colors flex items-center gap-1 text-slate-300 group"
            >
              <span>Control Room</span>
              <ExternalLink className="h-3.5 w-3.5 text-slate-400 group-hover:text-cyan-400 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
            </a>
          </nav>

          <div className="flex items-center gap-3">
            <div className="hidden lg:flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-xs font-medium text-emerald-400">
              <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <ShieldCheck className="h-3.5 w-3.5" />
              <span>AST Security Active</span>
            </div>
            <Link
              href="/workspace"
              className="px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500 via-indigo-500 to-purple-600 hover:from-cyan-400 hover:to-purple-500 text-white font-bold text-xs shadow-lg shadow-cyan-500/20 hover:shadow-cyan-500/35 transition-all hover:scale-[1.02] flex items-center gap-1.5"
            >
              <Sparkles className="h-3.5 w-3.5 text-cyan-200" />
              <span>Launch Studio</span>
            </Link>
          </div>
        </header>

        {/* Main View Area */}
        <main className="flex-1">
          {children}
        </main>

        {/* Footer */}
        <footer className="border-t border-slate-800/80 py-10 px-6 text-xs text-slate-400 bg-[#07090e]/90 relative z-10">
          <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="flex items-center gap-3">
              <div className="h-7 w-7 rounded-lg bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 font-bold">
                ⚡
              </div>
              <p className="text-slate-400">
                © 2026 SheetPilot AI. Powered by Python Pandas, FastAPI & AST Security Sandboxing.
              </p>
            </div>

            <div className="flex items-center gap-6 text-sm font-medium">
              <Link href="/" className="hover:text-cyan-400 transition-colors">Home</Link>
              <Link href="/workspace" className="hover:text-cyan-400 transition-colors">Workspace</Link>
              <a href="https://sheetpilotai.streamlit.app/" target="_blank" rel="noreferrer" className="hover:text-cyan-400 transition-colors flex items-center gap-1">
                <span>Control Room</span>
                <ExternalLink className="h-3 w-3" />
              </a>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}

