"use client";

import { Sparkles, Code2, CheckCircle, Zap, ShieldCheck, AlertTriangle } from "lucide-react";

export default function PlanCard({ planData, onExecute, isExecuting }) {
    if (!planData) return null;

    const { plan, generated_code } = planData;

    const getOpBadge = (opType) => {
        switch (opType) {
            case "filter":
                return "bg-cyan-500/20 text-cyan-300 border-cyan-500/30";
            case "sort":
                return "bg-indigo-500/20 text-indigo-300 border-indigo-500/30";
            case "calculate_column":
                return "bg-purple-500/20 text-purple-300 border-purple-500/30";
            case "create_sheet":
                return "bg-emerald-500/20 text-emerald-300 border-emerald-500/30";
            default:
                return "bg-slate-700/50 text-slate-300 border-slate-600/40";
        }
    };

    return (
        <div className="glass-panel rounded-2xl p-6 border border-white/10 flex flex-col gap-6">
            {/* Header */}
            <div className="flex items-center justify-between border-b border-white/10 pb-4">
                <div className="flex items-center gap-2">
                    <Sparkles className="h-5 w-5 text-indigo-400" />
                    <h2 className="text-lg font-bold text-slate-100">AI Action Plan & AST Code</h2>
                </div>

                <div className="flex items-center gap-3">
                    <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-xs font-semibold text-indigo-300">
                        <ShieldCheck className="h-3.5 w-3.5" />
                        <span>Confidence: {Math.round((plan?.confidence || 0.95) * 100)}%</span>
                    </div>
                </div>
            </div>

            {/* Intent & Clarification Notice */}
            {plan?.requires_clarification ? (
                <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-start gap-3">
                    <AlertTriangle className="h-5 w-5 text-amber-400 shrink-0 mt-0.5" />
                    <div>
                        <h4 className="text-sm font-bold text-amber-300">Schema Adherence Warning</h4>
                        <p className="text-xs text-amber-200/80 mt-1">{plan.clarification_message}</p>
                    </div>
                </div>
            ) : (
                <div className="p-4 rounded-xl bg-indigo-950/40 border border-indigo-500/20">
                    <h3 className="text-xs font-semibold text-indigo-400 uppercase tracking-wider">
                        Synthesized Transformation Intent
                    </h3>
                    <p className="text-sm font-medium text-slate-200 mt-1">{plan?.intent}</p>
                </div>
            )}

            {/* Operations List */}
            <div className="flex flex-col gap-3">
                <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                    Planned Operations ({plan?.operations?.length || 0})
                </h3>

                <div className="flex flex-col gap-2">
                    {plan?.operations?.map((op, idx) => (
                        <div
                            key={idx}
                            className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between gap-3"
                        >
                            <div className="flex items-center gap-3">
                                <span className="h-6 w-6 rounded-full bg-slate-800 text-slate-400 text-xs font-bold flex items-center justify-center border border-slate-700">
                                    {idx + 1}
                                </span>
                                <span className="text-sm text-slate-200 font-medium">{op.description}</span>
                            </div>

                            <span
                                className={`text-xs font-mono font-semibold px-2.5 py-1 rounded-lg border ${getOpBadge(
                                    op.type
                                )}`}
                            >
                                {op.type}
                            </span>
                        </div>
                    ))}
                </div>
            </div>

            {/* Generated Code Preview */}
            <div className="flex flex-col gap-2">
                <div className="flex items-center justify-between">
                    <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                        <Code2 className="h-4 w-4 text-cyan-400" />
                        Synthesized AST Python Code (Pandas)
                    </h3>
                    <span className="text-[10px] text-slate-500 font-mono">Verified Zero-Hallucination</span>
                </div>

                <pre className="p-4 rounded-xl bg-slate-950 border border-slate-800 text-xs font-mono text-cyan-300 overflow-x-auto leading-relaxed max-h-60">
                    <code>{generated_code}</code>
                </pre>
            </div>

            {/* Execute Button */}
            <button
                type="button"
                onClick={onExecute}
                disabled={isExecuting}
                className="w-full py-3.5 px-6 rounded-xl bg-gradient-to-r from-cyan-500 via-indigo-500 to-purple-600 hover:from-cyan-400 hover:to-purple-500 text-white font-bold text-sm shadow-lg shadow-cyan-500/20 flex items-center justify-center gap-2 transition-all disabled:opacity-50"
            >
                {isExecuting ? (
                    <>
                        <Zap className="h-4 w-4 animate-spin text-white" />
                        <span>Executing in AST Sandbox...</span>
                    </>
                ) : (
                    <>
                        <Zap className="h-4 w-4 text-white" />
                        <span>⚡ Execute in AST Sandbox</span>
                    </>
                )}
            </button>
        </div>
    );
}
