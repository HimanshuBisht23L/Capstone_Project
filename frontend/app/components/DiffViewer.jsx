"use client";

import { Download, CheckCircle2, Clock, Layers, FileSpreadsheet, Terminal } from "lucide-react";

export default function DiffViewer({ result, downloadUrl }) {
    if (!result) return null;

    const { job_id, status, execution_time_ms, diff_summary, error_log } = result;

    return (
        <div className="glass-panel rounded-2xl p-6 sm:p-8 border border-emerald-500/30 bg-emerald-950/10 flex flex-col gap-6 shadow-2xl">
            {/* Header */}
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between border-b border-emerald-500/20 pb-4 gap-3">
                <div className="flex items-center gap-3">
                    <div className="h-10 w-10 rounded-xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400">
                        <CheckCircle2 className="h-6 w-6" />
                    </div>
                    <div>
                        <h2 className="text-lg font-bold text-slate-100">Sandbox Execution Complete</h2>
                        <p className="text-xs text-emerald-400 font-medium flex items-center gap-1.5 mt-0.5">
                            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
                            <span>Status: SUCCESS</span>
                        </p>
                    </div>
                </div>

                <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-emerald-500/15 border border-emerald-500/30 text-xs font-semibold text-emerald-300">
                    <Clock className="h-3.5 w-3.5" />
                    <span>Latency: {execution_time_ms} ms</span>
                </div>
            </div>

            {/* Differential Summary Cards */}
            {diff_summary && (
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3.5">
                    <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 flex flex-col justify-between">
                        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Total Output Rows</span>
                        <div className="text-2xl font-extrabold text-slate-100 mt-2">
                            {diff_summary.modified_total_rows?.toLocaleString() || diff_summary.original_total_rows || 0}
                        </div>
                    </div>

                    <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 flex flex-col justify-between">
                        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Row Delta</span>
                        <div className={`text-2xl font-extrabold mt-2 ${(diff_summary.rows_delta || 0) < 0 ? "text-amber-400" : "text-emerald-400"
                            }`}>
                            {diff_summary.rows_delta > 0 ? `+${diff_summary.rows_delta}` : diff_summary.rows_delta || 0}
                        </div>
                    </div>

                    <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 flex flex-col justify-between">
                        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Modified Sheets</span>
                        <div className="text-sm font-bold text-cyan-300 mt-2 font-mono truncate">
                            {diff_summary.common_sheets_modified?.join(", ") || "Sheet1"}
                        </div>
                    </div>
                </div>
            )}

            {/* Raw Output Log */}
            {error_log && (
                <div className="flex flex-col gap-2">
                    <span className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                        <Terminal className="h-3.5 w-3.5 text-cyan-400" />
                        Execution Stdout Log
                    </span>
                    <pre className="p-4 rounded-xl bg-[#07090e] border border-slate-800 text-[11px] font-mono text-slate-300 overflow-x-auto leading-relaxed shadow-inner">
                        <code>{error_log}</code>
                    </pre>
                </div>
            )}

            {/* Download Transformed Workbook Button */}
            <a
                href={downloadUrl || `http://localhost:8000/api/v1/jobs/results/${job_id}/download`}
                download
                className="w-full py-4 px-6 rounded-xl bg-gradient-to-r from-emerald-500 via-emerald-400 to-teal-400 hover:from-emerald-400 hover:to-teal-300 text-slate-950 font-extrabold text-sm shadow-xl shadow-emerald-500/25 flex items-center justify-center gap-2.5 transition-all hover:scale-[1.01] active:scale-[0.99]"
            >
                <Download className="h-5 w-5" />
                <span>📥 Download Transformed Workbook (.xlsx)</span>
            </a>
        </div>
    );
}

