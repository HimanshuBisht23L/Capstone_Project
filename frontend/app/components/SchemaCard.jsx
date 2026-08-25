"use client";

import { useState } from "react";
import { Table, Layers, Hash, Calendar, FileText } from "lucide-react";

export default function SchemaCard({ schema }) {
    const [activeTab, setActiveTab] = useState(0);

    if (!schema || !schema.sheets || schema.sheets.length === 0) return null;

    const currentSheet = schema.sheets[activeTab] || schema.sheets[0];

    const getDtypeBadge = (dtype) => {
        if (dtype.includes("int")) return "bg-blue-500/15 text-blue-300 border-blue-500/30";
        if (dtype.includes("float")) return "bg-purple-500/15 text-purple-300 border-purple-500/30";
        if (dtype.includes("datetime")) return "bg-amber-500/15 text-amber-300 border-amber-500/30";
        if (dtype.includes("bool")) return "bg-emerald-500/15 text-emerald-300 border-emerald-500/30";
        return "bg-slate-800 text-slate-300 border-slate-700/60";
    };

    return (
        <div className="glass-panel rounded-2xl p-6 border border-white/10 flex flex-col gap-6">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between border-b border-white/10 pb-4 gap-3">
                <div className="flex items-center gap-2.5">
                    <div className="h-9 w-9 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
                        <Table className="h-5 w-5" />
                    </div>
                    <div>
                        <h2 className="text-lg font-bold text-slate-100">Extracted Workbook Schema</h2>
                        <p className="text-xs text-slate-400">Pandas structure & metadata breakdown</p>
                    </div>
                </div>

                <div className="flex items-center gap-3 text-xs text-slate-400">
                    <span className="px-3 py-1.5 rounded-lg bg-slate-900/80 border border-slate-800 flex items-center gap-1.5">
                        <Layers className="h-3.5 w-3.5 text-cyan-400" />
                        <span>Sheets:</span>
                        <strong className="text-slate-200">{schema.total_sheets}</strong>
                    </span>
                    <span className="px-3 py-1.5 rounded-lg bg-slate-900/80 border border-slate-800 flex items-center gap-1.5">
                        <Hash className="h-3.5 w-3.5 text-indigo-400" />
                        <span>Total Rows:</span>
                        <strong className="text-slate-200">{schema.total_rows.toLocaleString()}</strong>
                    </span>
                </div>
            </div>

            {/* Sheet Tabs */}
            {schema.sheets.length > 1 && (
                <div className="flex items-center gap-2 overflow-x-auto pb-2 border-b border-slate-800/80">
                    {schema.sheets.map((s, idx) => (
                        <button
                            key={s.name}
                            onClick={() => setActiveTab(idx)}
                            className={`px-3.5 py-2 rounded-xl text-xs font-semibold transition-all flex items-center gap-2 shrink-0 ${activeTab === idx
                                ? "bg-gradient-to-r from-cyan-500/20 to-indigo-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm"
                                : "bg-slate-900/50 text-slate-400 hover:bg-slate-900 hover:text-slate-200"
                                }`}
                        >
                            <Layers className="h-3.5 w-3.5" />
                            <span>{s.name}</span>
                            <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-slate-800 text-slate-400 font-mono">
                                {s.row_count} rows
                            </span>
                        </button>
                    ))}
                </div>
            )}

            {/* Columns Grid */}
            <div className="flex flex-col gap-3">
                <div className="flex items-center justify-between">
                    <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                        Detected Columns & Dtypes ({currentSheet.columns.length})
                    </h3>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
                    {currentSheet.columns.map((col) => (
                        <div
                            key={col.name}
                            className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800/90 flex flex-col gap-2 hover:border-slate-700/80 transition-all glow-on-hover"
                        >
                            <div className="flex items-center justify-between gap-2">
                                <span className="text-sm font-bold text-slate-200 truncate">{col.name}</span>
                                <span
                                    className={`text-[10px] font-mono px-2 py-0.5 rounded-full border font-semibold ${getDtypeBadge(
                                        col.dtype
                                    )}`}
                                >
                                    {col.dtype}
                                </span>
                            </div>

                            {col.sample_values && col.sample_values.length > 0 && (
                                <div className="text-[11px] text-slate-400 truncate pt-1 border-t border-slate-800/50">
                                    <span className="text-slate-500 font-medium">Samples: </span>
                                    <span className="text-slate-300 font-mono">{col.sample_values.slice(0, 3).join(", ")}</span>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

