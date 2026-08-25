"use client";

import { Download, CheckCircle2, Clock, Layers, FileSpreadsheet, Terminal } from "lucide-react";

export default function DiffViewer({ result, downloadUrl }) {
    if (!result) return null;

    const { job_id, status, execution_time_ms, diff_summary, error_log } = result;

    return (
        <div className="glass-panel rounded-2xl p-6 border border-emerald-500/30 bg-emerald-950/10 flex flex-col gap-6">
            {/* Header */}
            <div className="flex items-center justify-between border-b border-emerald-500/20 pb-4">
                <div className="flex items-center gap-2">
                    <CheckCircle2 className="h-6 w-6 text-emerald-400" />
                    <div>
                        <h2 className="text-lg font-bold text-slate-100">Sandbox Execution Complete</h2>
                        <p className="text-xs text-emerald-400/80 font-medium">Status: SUCCESS</p>
                    </div>
                </div>

                <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-xs font-semibold text-emerald-300">
                    <Clock className="h-3.5 w-3.5" />
                    <span>Latency: {execution_time_ms} ms</span>
                </div>
            </div>

            {/* Differential Summary Cards */}
            {diff_summary && (
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800">
                        <span className="text-xs text-slate-400">Total Output Rows</span>
                        <div className="text-xl font-extrabold text-slate-100 mt-1">
                            {diff_summary.modified_total_rows?.toLocaleString() || diff_summary.original_total_rows || 0}
                        </div>
                    </div>

                    <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800">
                        <span className="text-xs text-slate-400">Row Delta</span>
                        <div className={`text-xl font-extrabold mt-1 ${(diff_summary.rows_delta || 0) < 0 ? "text-amber-400" : "text-emerald-400"
                            }`}>
                            {diff_summary.rows_delta > 0 ? `+${diff_summary.rows_delta}` : diff_summary.rows_delta || 0}
                        </div>
                    </div>

                    <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800">
                        <span className="text-xs text-slate-400">Modified Sheets</span>
                        <div className="text-sm font-bold text-cyan-300 mt-1">
                            {diff_summary.common_sheets_modified?.join(", ") || "Sheet1"}
                        </div>
                    </div>
                </div>
            )}

            {/* Raw Output Log */}
            {error_log && (
                <div className="flex flex-col gap-2">
                    <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                        <Terminal className="h-3.5 w-3.5 text-slate-400" />
                        Execution Stdout Log
                    </span>
                    <pre className="p-3 rounded-lg bg-slate-950 border border-slate-800 text-[11px] font-mono text-slate-300 overflow-x-auto">
                        <code>{error_log}</code>
                    </pre>
                </div>
            )}

            {/* Download Transformed Workbook Button */}
            <a
                href={downloadUrl || `http://localhost:8000/api/v1/jobs/results/${job_id}/download`}
                download
                className="w-full py-4 px-6 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-extrabold text-sm shadow-lg shadow-emerald-500/20 flex items-center justify-center gap-2 transition-all"
            >
                <Download className="h-5 w-5" />
                <span>📥 Download Transformed Workbook (.xlsx)</span>
            </a>
        </div>
    );
}
