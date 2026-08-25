"use client";

import { useState } from "react";
import VoiceMic from "../components/VoiceMic";
import Dropzone from "../components/Dropzone";
import SchemaCard from "../components/SchemaCard";
import PlanCard from "../components/PlanCard";
import DiffViewer from "../components/DiffViewer";
import { Sparkles, RefreshCw, AlertCircle, ArrowLeft, Terminal, Cpu } from "lucide-react";
import Link from "next/link";

export default function WorkspaceStudioPage() {
    const [file, setFile] = useState(null);
    const [fileId, setFileId] = useState(null);
    const [schema, setSchema] = useState(null);
    const [uploading, setUploading] = useState(false);

    const [prompt, setPrompt] = useState("");
    const [planData, setPlanData] = useState(null);
    const [generatingPlan, setGeneratingPlan] = useState(false);

    const [executing, setExecuting] = useState(false);
    const [executionResult, setExecutionResult] = useState(null);

    const [errorMsg, setErrorMsg] = useState("");

    // 1. Upload File Handler (POST /api/files/upload)
    const handleFileUpload = async (uploadedFile) => {
        if (!uploadedFile) return;

        setFile(uploadedFile);
        setUploading(true);
        setErrorMsg("");
        setSchema(null);
        setPlanData(null);
        setExecutionResult(null);

        try {
            const formData = new FormData();
            formData.append("file", uploadedFile);

            const res = await fetch("/api/files/upload", {
                method: "POST",
                body: formData,
            });

            if (res.ok) {
                const data = await res.json();
                setFileId(data.file_id);
                setSchema(data.schema_info);
            } else {
                const errData = await res.json();
                setErrorMsg(`Upload error: ${errData.detail || "Failed to process workbook."}`);
            }
        } catch (err) {
            console.error("Upload network failure:", err);
            setErrorMsg("Could not connect to Next.js API Proxy.");
        } finally {
            setUploading(false);
        }
    };

    // 2. Generate Plan Handler (POST /api/agent/plan)
    const handleGeneratePlan = async () => {
        if (!prompt.trim()) {
            setErrorMsg("Please enter a natural language instruction or use voice input.");
            return;
        }
        if (!fileId) {
            setErrorMsg("Please upload a spreadsheet workbook first.");
            return;
        }

        setGeneratingPlan(true);
        setErrorMsg("");
        setPlanData(null);
        setExecutionResult(null);

        try {
            const res = await fetch("/api/agent/plan", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    file_id: fileId,
                    user_prompt: prompt,
                }),
            });

            if (res.ok) {
                const data = await res.json();
                setPlanData(data);
            } else {
                const errData = await res.json();
                setErrorMsg(`Plan generation failed: ${errData.detail || "AI synthesis error."}`);
            }
        } catch (err) {
            console.error("Plan generation network failure:", err);
            setErrorMsg("Could not connect to Next.js API Proxy.");
        } finally {
            setGeneratingPlan(false);
        }
    };

    // 3. Execute Sandbox Handler (POST /api/jobs/execute)
    const handleExecuteSandbox = async () => {
        if (!planData?.plan_id) return;

        setExecuting(true);
        setErrorMsg("");

        try {
            const res = await fetch("/api/jobs/execute", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ plan_id: planData.plan_id }),
            });

            if (res.ok) {
                const data = await res.json();
                pollJobStatus(data.job_id);
            } else {
                const errData = await res.json();
                setErrorMsg(`Execution trigger failed: ${errData.detail || "Sandbox error."}`);
                setExecuting(false);
            }
        } catch (err) {
            console.error("Execution network failure:", err);
            setErrorMsg("Failed to connect to Next.js API Proxy.");
            setExecuting(false);
        }
    };

    // 4. Poll Job Status (GET /api/jobs/{job_id})
    const pollJobStatus = (jobId) => {
        const interval = setInterval(async () => {
            try {
                const res = await fetch(`/api/jobs/${jobId}`);
                if (res.ok) {
                    const data = await res.json();
                    if (data.status === "SUCCESS" || data.status === "FAILED") {
                        clearInterval(interval);
                        setExecutionResult(data);
                        setExecuting(false);
                    }
                }
            } catch (err) {
                console.error("Polling error:", err);
                clearInterval(interval);
                setExecuting(false);
            }
        }, 1000);
    };

    return (
        <div className="flex flex-col gap-8 py-8 max-w-7xl mx-auto px-4 pb-20 relative">
            {/* Studio Navigation & Header */}
            <div className="flex items-center justify-between border-b border-white/10 pb-4">
                <Link
                    href="/"
                    className="inline-flex items-center gap-2 text-xs font-semibold text-slate-400 hover:text-cyan-400 transition"
                >
                    <ArrowLeft className="h-4 w-4" />
                    <span>Back to Home</span>
                </Link>

                <div className="flex items-center gap-2">
                    <span className="px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-xs font-bold text-cyan-300 flex items-center gap-1.5">
                        <Sparkles className="h-3.5 w-3.5 text-cyan-400" />
                        SheetPilot Interactive Studio
                    </span>
                </div>
            </div>

            {/* Global Error Banner */}
            {errorMsg && (
                <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-sm flex items-start gap-3 shadow-lg">
                    <AlertCircle className="h-5 w-5 shrink-0 mt-0.5" />
                    <span>{errorMsg}</span>
                </div>
            )}

            {/* Step 1: Upload Dropzone */}
            <div className="flex flex-col gap-3">
                <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-2">
                    <span className="h-6 w-6 rounded-full bg-cyan-500/20 text-cyan-400 text-xs flex items-center justify-center font-bold border border-cyan-500/30">1</span>
                    Select or Drop Spreadsheet Workbook
                </h2>
                <Dropzone
                    onFileSelected={handleFileUpload}
                    isUploading={uploading}
                    uploadedFileName={file?.name}
                />
            </div>

            {/* Extracted Schema Preview */}
            {schema && <SchemaCard schema={schema} />}

            {/* Step 2: Prompt Input & Voice Controls */}
            {schema && (
                <div className="glass-panel rounded-2xl p-6 sm:p-8 border border-white/10 flex flex-col gap-5 shadow-xl">
                    <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                        <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-2">
                            <span className="h-6 w-6 rounded-full bg-indigo-500/20 text-indigo-400 text-xs flex items-center justify-center font-bold border border-indigo-500/30">2</span>
                            Enter Natural Language Instruction
                        </h2>

                        <VoiceMic onTranscriptChange={(text) => setPrompt(text)} />
                    </div>

                    <div className="flex flex-col sm:flex-row gap-3">
                        <textarea
                            value={prompt}
                            onChange={(e) => setPrompt(e.target.value)}
                            placeholder="e.g. Filter rows where Marks > 80, sort by Student_Name ascending, and calculate summary."
                            rows={3}
                            className="w-full p-4 rounded-xl bg-[#07090e] border border-slate-800 text-sm text-slate-100 placeholder:text-slate-500 focus:outline-none focus:border-cyan-500/60 focus:ring-1 focus:ring-cyan-500/60 transition resize-none leading-relaxed font-sans"
                        />
                    </div>

                    {/* Quick Prompt Pills */}
                    <div className="flex flex-wrap items-center gap-2 pt-1">
                        <span className="text-xs text-slate-500 font-medium">Quick Prompts:</span>
                        {[
                            "Filter students with Marks > 80",
                            "Sort table by Student_Name ascending",
                            "Calculate average marks and summary",
                        ].map((qp) => (
                            <button
                                key={qp}
                                type="button"
                                onClick={() => setPrompt(qp)}
                                className="text-xs px-3 py-1.5 rounded-lg bg-slate-900/80 hover:bg-slate-800 text-slate-300 border border-slate-700/80 hover:border-cyan-500/40 transition"
                            >
                                {qp}
                            </button>
                        ))}
                    </div>

                    <button
                        type="button"
                        onClick={handleGeneratePlan}
                        disabled={generatingPlan}
                        className="w-full py-4 px-6 rounded-xl bg-gradient-to-r from-indigo-600 via-indigo-500 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-extrabold text-sm shadow-lg shadow-indigo-500/20 flex items-center justify-center gap-2.5 transition-all disabled:opacity-50 mt-2"
                    >
                        {generatingPlan ? (
                            <>
                                <RefreshCw className="h-4 w-4 animate-spin text-white" />
                                <span>Synthesizing AI Action Plan...</span>
                            </>
                        ) : (
                            <>
                                <Sparkles className="h-4 w-4 text-cyan-300" />
                                <span>🚀 Generate AI Action Plan</span>
                            </>
                        )}
                    </button>
                </div>
            )}

            {/* Step 3: AI Action Plan & AST Code Inspector */}
            {planData && (
                <PlanCard
                    planData={planData}
                    onExecute={handleExecuteSandbox}
                    isExecuting={executing}
                />
            )}

            {/* Step 4: Differential Metrics & Transformed File Download */}
            {executionResult && (
                <DiffViewer
                    result={executionResult}
                    downloadUrl={`/api/jobs/results/${executionResult.job_id}/download`}
                />
            )}
        </div>
    );
}

