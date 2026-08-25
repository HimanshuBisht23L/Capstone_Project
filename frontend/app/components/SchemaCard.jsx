"use client";

import { useState } from "react";
import { Table, Layers, FileText, Hash, Calendar, ToggleLeft, Strut } from "lucide-react";

export default function SchemaCard({ schema }) {
    const [activeTab, setActiveTab] = useState(0);

    if (!schema || !schema.sheets || schema.sheets.length === 0) return null;

    const currentSheet = schema.sheets[activeTab] || schema.sheets[0];

    const getDtypeBadge = (dtype) => {
        if (dtype.includes("int")) return "bg-blue-500/20 text-blue-300 border-blue-500/30";
        if (dtype.includes("float")) return "bg-purple-500/20 text-purple-300 border-purple-500/30";
        if (dtype.includes("datetime")) return "bg-amber-500/20 text-amber-300 border-amber-500/30";
        if (dtype.includes("bool")) return "bg-emerald-500/20 text-emerald-300 border-emerald-500/30";
        return "bg-slate-700/50 text-slate-300 border-slate-600/40";
    };

    return (
        <div className="glass-panel rounded-2xl p-6 border border-white/10 flex flex-col gap-5">
            <div className="flex items-center justify-between border-b border-white/10 pb-4">
                <div className="flex items-center gap-2">
                    <Table className="h-5 w-5 text-cyan-400" />
                    <h2 className="text-lg font-bold text-slate-100">Extracted Workbook Schema</h2>
                </div>

                <div className="flex items-center gap-3 text-xs text-slate-400">
                    <span className="px-2.5 py-1 rounded-md bg-slate-800 border border-slate-700">
                        Sheets: <strong className="text-slate-200">{schema.total_sheets}</strong>
                    </span>
                    <span className="px-2.5 py-1 rounded-md bg-slate-800 border border-slate-700">
                        Total Rows: <strong className="text-slate-200">{schema.total_rows.toLocaleString()}</strong>
                    </span>
                </div>
            </div>

            {/* Sheet Tabs */}
            {schema.sheets.length > 1 && (
                <div className="flex items-center gap-2 overflow-x-auto pb-2 border-b border-slate-800">
                    {schema.sheets.map((s, idx) => (
                        <button
                            key={s.name}
                            onClick={() => setActiveTab(idx)}
                            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${activeTab === idx
                                    ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40"
                                    : "bg-slate-800/60 text-slate-400 hover:bg-slate-800"
                                }`}
                        >
                            <Layers className="h-3.5 w-3.5 inline mr-1" />
                            {s.name} ({s.row_count} rows)
                        </button>
                    ))}
                </div>
            )}

            {/* Columns Grid */}
            <div className="flex flex-col gap-3">
                <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                    Detected Columns & Dtypes ({currentSheet.columns.length})
                </h3>

                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
                    {currentSheet.columns.map((col) => (
                        <div
                            key={col.name}
                            className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 flex flex-col gap-2 hover:border-slate-700 transition"
                        >
                            <div className="flex items-center justify-between gap-2">
                                <span className="text-sm font-bold text-slate-200 truncate">{col.name}</span>
                                <span
                                    className={`text-[10px] font-mono px-2 py-0.5 rounded-full border ${getDtypeBadge(
                                        col.dtype
                                    )}`}
                                >
                                    {col.dtype}
                                </span>
                            </div>

                            {col.sample_values && col.sample_values.length > 0 && (
                                <div className="text-[11px] text-slate-400 truncate">
                                    Samples: <span className="text-slate-300">{col.sample_values.slice(0, 3).join(", ")}</span>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
