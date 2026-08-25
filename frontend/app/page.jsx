import Link from "next/link";
import { Mic, ShieldCheck, Table, Sparkles, ArrowRight, Zap, Download, Layers, CheckCircle2, Terminal, Cpu } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="flex flex-col gap-24 py-12 max-w-7xl mx-auto px-4 relative">
      {/* Background Ambient Glow */}
      <div className="absolute top-12 left-1/2 -translate-x-1/2 w-full max-w-4xl h-96 bg-cyan-500/10 blur-[120px] rounded-full pointer-events-none -z-10"></div>

      {/* Hero Section */}
      <section className="text-center flex flex-col items-center gap-6 pt-6 sm:pt-10">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-xs font-semibold text-cyan-300 tracking-wide shadow-inner">
          <Sparkles className="h-3.5 w-3.5 text-cyan-400 animate-pulse" />
          <span>Next-Gen Enterprise AI Spreadsheet Engine</span>
        </div>

        <h1 className="text-4xl sm:text-6xl md:text-7xl font-extrabold tracking-tight gradient-text max-w-5xl leading-[1.1] sm:leading-[1.15]">
          Automate Spreadsheets with Voice Commands & AST Security
        </h1>

        <p className="text-base sm:text-lg text-slate-300 max-w-2xl leading-relaxed font-normal">
          Transform complex Excel (.xlsx) and CSV files in seconds using natural voice instructions. Driven by zero-hallucination AST code verification and isolated Python sandboxes.
        </p>

        <div className="flex flex-col sm:flex-row items-center gap-4 mt-3 w-full sm:w-auto">
          <Link
            href="/workspace"
            className="w-full sm:w-auto px-8 py-4 rounded-xl bg-gradient-to-r from-cyan-500 via-indigo-500 to-purple-600 hover:from-cyan-400 hover:to-purple-500 text-white font-extrabold text-base shadow-xl shadow-cyan-500/25 flex items-center justify-center gap-3 transition-all hover:scale-[1.03] active:scale-[0.98]"
          >
            <span>🚀 Try SheetPilot Studio</span>
            <ArrowRight className="h-5 w-5" />
          </Link>

          <a
            href="https://sheetpilotai.streamlit.app/"
            target="_blank"
            rel="noreferrer"
            className="w-full sm:w-auto px-7 py-4 rounded-xl bg-slate-900/90 hover:bg-slate-800 text-slate-200 border border-slate-700/80 font-bold text-sm flex items-center justify-center gap-2.5 transition-all hover:border-cyan-500/40"
          >
            <Terminal className="h-4 w-4 text-cyan-400" />
            <span>View Control Room Dashboard</span>
          </a>
        </div>

        {/* System Architecture Stats Bar */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 w-full max-w-4xl mt-6 p-4 rounded-2xl bg-slate-900/40 border border-white/5 backdrop-blur-md">
          <div className="flex flex-col items-center justify-center p-2">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Security</span>
            <span className="text-sm font-bold text-emerald-400 flex items-center gap-1 mt-0.5">
              <ShieldCheck className="h-4 w-4" /> 100% AST Audited
            </span>
          </div>
          <div className="flex flex-col items-center justify-center p-2">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Sandbox Timeout</span>
            <span className="text-sm font-bold text-cyan-300 flex items-center gap-1 mt-0.5">
              <Cpu className="h-4 w-4" /> 10s Subprocess Limit
            </span>
          </div>
          <div className="flex flex-col items-center justify-center p-2">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">NLP Engine</span>
            <span className="text-sm font-bold text-indigo-300 flex items-center gap-1 mt-0.5">
              <Sparkles className="h-4 w-4" /> Zero-Hallucination
            </span>
          </div>
          <div className="flex flex-col items-center justify-center p-2">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Benchmark Suite</span>
            <span className="text-sm font-bold text-purple-300 flex items-center gap-1 mt-0.5">
              <CheckCircle2 className="h-4 w-4" /> 10 Domain Suite
            </span>
          </div>
        </div>

        {/* Live Feature Preview Mockup */}
        <div className="w-full max-w-4xl mt-6 glass-panel rounded-3xl p-6 sm:p-8 border border-white/10 shadow-2xl text-left flex flex-col gap-6 relative overflow-hidden glow-on-hover">
          <div className="flex items-center justify-between border-b border-white/10 pb-4">
            <div className="flex items-center gap-3">
              <div className="h-3 w-3 rounded-full bg-red-500/80"></div>
              <div className="h-3 w-3 rounded-full bg-amber-500/80"></div>
              <div className="h-3 w-3 rounded-full bg-emerald-500/80"></div>
              <span className="text-xs text-slate-400 font-mono ml-2">sheetpilot_studio_preview.xlsx</span>
            </div>
            <span className="text-xs px-3 py-1 rounded-full bg-cyan-500/20 text-cyan-300 font-semibold border border-cyan-500/30 flex items-center gap-1.5">
              <span className="h-1.5 w-1.5 rounded-full bg-cyan-400 animate-ping"></span>
              Live Demo Preview
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="flex flex-col gap-3 p-4 rounded-2xl bg-slate-900/90 border border-slate-800/90">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-2">
                <Mic className="h-4 w-4 text-cyan-400" />
                Voice Command Input
              </span>
              <p className="text-sm font-medium text-slate-200 bg-[#07090e] p-3.5 rounded-xl border border-slate-800 font-mono leading-relaxed">
                "Filter students with Marks greater than 80, sort by name, and create summary sheet."
              </p>
            </div>

            <div className="flex flex-col gap-3 p-4 rounded-2xl bg-slate-900/90 border border-slate-800/90">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-2">
                <ShieldCheck className="h-4 w-4 text-emerald-400" />
                AST Verified Pandas Code
              </span>
              <pre className="text-[11px] font-mono text-cyan-300 bg-[#07090e] p-3.5 rounded-xl border border-slate-800 overflow-x-auto leading-relaxed">
                <code>{`df = sheets_dict['Sheet1']\ndf = df[df['Marks'] > 80]\ndf = df.sort_values(by='Student_Name')`}</code>
              </pre>
            </div>
          </div>
        </div>
      </section>

      {/* Core Features Grid */}
      <section className="flex flex-col gap-12 text-center">
        <div>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-100">
            Why Choose SheetPilot AI?
          </h2>
          <p className="text-sm sm:text-base text-slate-400 mt-2 max-w-xl mx-auto">
            Built for enterprise security, lightning speed, and effortless natural language spreadsheet control.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="glass-panel p-8 rounded-2xl border border-white/10 text-left flex flex-col gap-4 glow-on-hover relative group">
            <div className="h-12 w-12 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 group-hover:scale-110 transition-transform">
              <Mic className="h-6 w-6" />
            </div>
            <h3 className="text-xl font-bold text-slate-100">Voice-First Experience</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              Speak instructions directly using browser-native Web Speech API. Supports real-time transcript streaming and Brave Privacy safeguards.
            </p>
          </div>

          <div className="glass-panel p-8 rounded-2xl border border-white/10 text-left flex flex-col gap-4 glow-on-hover relative group">
            <div className="h-12 w-12 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 group-hover:scale-110 transition-transform">
              <ShieldCheck className="h-6 w-6" />
            </div>
            <h3 className="text-xl font-bold text-slate-100">AST Security Sandbox</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              Static AST inspection blocks dangerous imports (`os`, `sys`, `eval`) before executing code inside isolated 10-second child subprocess sandboxes.
            </p>
          </div>

          <div className="glass-panel p-8 rounded-2xl border border-white/10 text-left flex flex-col gap-4 glow-on-hover relative group">
            <div className="h-12 w-12 rounded-xl bg-purple-500/10 border border-purple-500/30 flex items-center justify-center text-purple-400 group-hover:scale-110 transition-transform">
              <Table className="h-6 w-6" />
            </div>
            <h3 className="text-xl font-bold text-slate-100">Pandas Schema Engine</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              Automatic column data type mapping (`string`, `float64`, `int64`) and sample value inspection ensuring zero AI schema hallucination.
            </p>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="glass-panel p-8 sm:p-12 rounded-3xl border border-white/10 flex flex-col gap-10">
        <div className="text-center">
          <h2 className="text-3xl font-extrabold text-slate-100">How It Works in 4 Easy Steps</h2>
          <p className="text-sm text-slate-400 mt-1">From raw Excel workbook to transformed output in under 2 seconds</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {[
            { step: "01", title: "Upload Workbook", desc: "Drag & drop your .xlsx or .csv spreadsheet file up to 50MB." },
            { step: "02", title: "Speak or Type", desc: "Use voice commands or type natural instructions for transformation." },
            { step: "03", title: "Verify AST Code", desc: "Inspect zero-hallucination Python Pandas script synthesized by AI." },
            { step: "04", title: "Execute & Export", desc: "Run in sandbox, review row deltas, and download clean transformed .xlsx." },
          ].map((s) => (
            <div key={s.step} className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800/80 flex flex-col gap-3 hover:border-cyan-500/30 transition-all">
              <span className="text-3xl font-extrabold gradient-text">{s.step}</span>
              <h4 className="text-base font-bold text-slate-200">{s.title}</h4>
              <p className="text-xs text-slate-400 leading-relaxed">{s.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Final CTA Banner */}
      <section className="text-center p-10 sm:p-14 rounded-3xl bg-gradient-to-br from-cyan-950/40 via-indigo-950/40 to-purple-950/40 border border-cyan-500/30 flex flex-col items-center gap-6 shadow-2xl relative overflow-hidden">
        <div className="absolute inset-0 bg-grid-pattern opacity-30 pointer-events-none"></div>

        <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-100 max-w-2xl leading-tight relative z-10">
          Ready to Automate Your Excel Worksheets Effortlessly?
        </h2>
        <p className="text-sm sm:text-base text-slate-300 max-w-xl relative z-10">
          Start using SheetPilot Studio now to transform files using natural language voice commands.
        </p>

        <Link
          href="/workspace"
          className="px-8 py-4 rounded-xl bg-gradient-to-r from-cyan-500 via-indigo-500 to-purple-600 hover:from-cyan-400 hover:to-purple-500 text-white font-extrabold text-base shadow-xl shadow-cyan-500/25 flex items-center gap-2 transition hover:scale-[1.03] active:scale-[0.98] relative z-10"
        >
          <span>🚀 Launch Workspace Studio Now</span>
          <ArrowRight className="h-5 w-5" />
        </Link>
      </section>
    </div>
  );
}

