import Link from "next/link";
import { Mic, ShieldCheck, Table, Sparkles, ArrowRight, Zap, Download, Layers, CheckCircle2 } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="flex flex-col gap-24 py-12 max-w-7xl mx-auto px-4">
      {/* Hero Section */}
      <section className="text-center flex flex-col items-center gap-6 pt-8">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-xs font-bold text-cyan-300 tracking-wide uppercase shadow-sm">
          <Sparkles className="h-4 w-4 text-cyan-400 animate-pulse" />
          <span>Next-Gen Enterprise AI Spreadsheet Engine</span>
        </div>

        <h1 className="text-5xl sm:text-6xl md:text-7xl font-extrabold tracking-tight gradient-text max-w-4xl leading-tight">
          Automate Spreadsheets with Voice Commands & AST Security
        </h1>

        <p className="text-base sm:text-lg text-slate-300 max-w-2xl leading-relaxed">
          Transform complex Excel (.xlsx) and CSV files in seconds using natural voice instructions. Driven by zero-hallucination AST code verification and isolated Python sandboxes.
        </p>

        <div className="flex flex-col sm:flex-row items-center gap-4 mt-4">
          <Link
            href="/workspace"
            className="w-full sm:w-auto px-8 py-4 rounded-xl bg-gradient-to-r from-cyan-500 via-indigo-500 to-purple-600 hover:from-cyan-400 hover:to-purple-500 text-white font-extrabold text-base shadow-xl shadow-cyan-500/25 flex items-center justify-center gap-3 transition-all hover:scale-105"
          >
            <span>🚀 Try SheetPilot Studio</span>
            <ArrowRight className="h-5 w-5" />
          </Link>

          <a
            href="http://localhost:8501"
            target="_blank"
            rel="noreferrer"
            className="w-full sm:w-auto px-7 py-4 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 font-bold text-sm flex items-center justify-center gap-2 transition"
          >
            <span>📊 View Control Room Dashboard</span>
          </a>
        </div>

        {/* Live Feature Preview Mockup */}
        <div className="w-full max-w-4xl mt-8 glass-panel rounded-3xl p-6 sm:p-8 border border-white/10 shadow-2xl text-left flex flex-col gap-6 relative overflow-hidden glow-on-hover">
          <div className="flex items-center justify-between border-b border-white/10 pb-4">
            <div className="flex items-center gap-3">
              <div className="h-3 w-3 rounded-full bg-red-500/80"></div>
              <div className="h-3 w-3 rounded-full bg-amber-500/80"></div>
              <div className="h-3 w-3 rounded-full bg-emerald-500/80"></div>
              <span className="text-xs text-slate-400 font-mono ml-2">sheetpilot_studio_preview.xlsx</span>
            </div>
            <span className="text-xs px-2.5 py-1 rounded-md bg-cyan-500/20 text-cyan-300 font-semibold border border-cyan-500/30">
              Live Demo Preview
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="flex flex-col gap-3 p-4 rounded-2xl bg-slate-900/80 border border-slate-800">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-2">
                <Mic className="h-4 w-4 text-cyan-400" />
                Voice Command Input
              </span>
              <p className="text-sm font-medium text-slate-200 bg-slate-950 p-3 rounded-xl border border-slate-800 font-mono">
                "Filter students with Marks greater than 80, sort by name, and create summary sheet."
              </p>
            </div>

            <div className="flex flex-col gap-3 p-4 rounded-2xl bg-slate-900/80 border border-slate-800">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-2">
                <ShieldCheck className="h-4 w-4 text-emerald-400" />
                AST Verified Pandas Code
              </span>
              <pre className="text-[11px] font-mono text-cyan-300 bg-slate-950 p-3 rounded-xl border border-slate-800 overflow-x-auto leading-relaxed">
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
          <div className="glass-panel p-8 rounded-2xl border border-white/10 text-left flex flex-col gap-4 glow-on-hover">
            <div className="h-12 w-12 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
              <Mic className="h-6 w-6" />
            </div>
            <h3 className="text-xl font-bold text-slate-100">Voice-First Experience</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              Speak instructions directly using browser-native Web Speech API. Supports real-time transcript streaming and Brave Privacy safeguards.
            </p>
          </div>

          <div className="glass-panel p-8 rounded-2xl border border-white/10 text-left flex flex-col gap-4 glow-on-hover">
            <div className="h-12 w-12 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
              <ShieldCheck className="h-6 w-6" />
            </div>
            <h3 className="text-xl font-bold text-slate-100">AST Security Sandbox</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              Static AST inspection blocks dangerous imports (`os`, `sys`, `eval`) before executing code inside isolated 10-second child subprocess sandboxes.
            </p>
          </div>

          <div className="glass-panel p-8 rounded-2xl border border-white/10 text-left flex flex-col gap-4 glow-on-hover">
            <div className="h-12 w-12 rounded-xl bg-purple-500/10 border border-purple-500/30 flex items-center justify-center text-purple-400">
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
      <section className="glass-panel p-10 rounded-3xl border border-white/10 flex flex-col gap-10">
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
            <div key={s.step} className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 flex flex-col gap-3">
              <span className="text-3xl font-extrabold gradient-text">{s.step}</span>
              <h4 className="text-base font-bold text-slate-200">{s.title}</h4>
              <p className="text-xs text-slate-400 leading-relaxed">{s.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Final CTA Banner */}
      <section className="text-center p-12 rounded-3xl bg-gradient-to-r from-cyan-950/60 via-indigo-950/60 to-purple-950/60 border border-cyan-500/30 flex flex-col items-center gap-6 shadow-2xl">
        <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-100 max-w-2xl">
          Ready to Automate Your Excel Worksheets Effortlessly?
        </h2>
        <p className="text-sm text-slate-300 max-w-xl">
          Start using SheetPilot Studio now to transform files using natural language voice commands.
        </p>

        <Link
          href="/workspace"
          className="px-8 py-4 rounded-xl bg-gradient-to-r from-cyan-500 to-purple-600 hover:from-cyan-400 hover:to-purple-500 text-white font-extrabold text-base shadow-xl shadow-cyan-500/25 flex items-center gap-2 transition hover:scale-105"
        >
          <span>🚀 Launch Workspace Studio Now</span>
          <ArrowRight className="h-5 w-5" />
        </Link>
      </section>
    </div>
  );
}
