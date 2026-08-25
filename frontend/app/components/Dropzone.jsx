"use client";

import { useState } from "react";
import { UploadCloud, FileSpreadsheet, CheckCircle2, Loader2, RefreshCw } from "lucide-react";

export default function Dropzone({ onFileSelected, isUploading, uploadedFileName }) {
    const [dragActive, setDragActive] = useState(false);

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            onFileSelected(e.dataTransfer.files[0]);
        }
    };

    const handleChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            onFileSelected(e.target.files[0]);
        }
    };

    return (
        <div
            onDragEnter={handleDrag}
            onDragOver={handleDrag}
            onDragLeave={handleDrag}
            onDrop={handleDrop}
            className={`glass-panel rounded-2xl p-8 sm:p-10 text-center border-2 border-dashed transition-all duration-300 relative glow-on-hover overflow-hidden ${dragActive
                ? "border-cyan-400 bg-cyan-950/30 scale-[1.01] shadow-2xl shadow-cyan-500/20"
                : uploadedFileName
                    ? "border-emerald-500/50 bg-emerald-950/15"
                    : "border-slate-700/60 bg-slate-900/40 hover:border-slate-600"
                }`}
        >
            <input
                type="file"
                accept=".xlsx, .xls, .csv"
                onChange={handleChange}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                disabled={isUploading}
            />

            <div className="flex flex-col items-center justify-center gap-3 relative z-0">
                {isUploading ? (
                    <div className="flex flex-col items-center gap-3 py-2">
                        <div className="h-14 w-14 rounded-full bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
                            <Loader2 className="h-7 w-7 text-cyan-400 animate-spin" />
                        </div>
                        <div className="flex flex-col items-center gap-1">
                            <p className="text-sm font-bold text-slate-200">
                                Parsing workbook & extracting schema...
                            </p>
                            <p className="text-xs text-slate-400">
                                Pandas type inference & row metadata extraction in progress
                            </p>
                        </div>
                    </div>
                ) : uploadedFileName ? (
                    <div className="flex flex-col items-center gap-2.5 py-1">
                        <div className="h-12 w-12 rounded-full bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400 shadow-lg shadow-emerald-500/10">
                            <CheckCircle2 className="h-6 w-6" />
                        </div>
                        <div className="flex flex-col items-center gap-1">
                            <span className="text-xs font-semibold text-emerald-400 uppercase tracking-wider">Active Workbook</span>
                            <p className="text-base font-extrabold text-slate-100 flex items-center gap-2">
                                <FileSpreadsheet className="h-4 w-4 text-emerald-400" />
                                <span>{uploadedFileName}</span>
                            </p>
                        </div>
                        <p className="text-xs text-slate-400 font-medium flex items-center gap-1 mt-1">
                            <RefreshCw className="h-3 w-3 text-slate-400" />
                            <span>Click or drag another workbook (.xlsx, .csv) to replace</span>
                        </p>
                    </div>
                ) : (
                    <div className="flex flex-col items-center gap-3">
                        <div className="h-14 w-14 rounded-2xl bg-gradient-to-br from-cyan-500/10 to-indigo-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 mb-1 shadow-inner">
                            <UploadCloud className="h-7 w-7" />
                        </div>
                        <div className="flex flex-col items-center gap-1">
                            <p className="text-base font-bold text-slate-200">
                                Drag & Drop your Excel workbook here, or <span className="text-cyan-400 underline underline-offset-4 font-extrabold">Browse</span>
                            </p>
                            <p className="text-xs text-slate-400 max-w-sm leading-relaxed">
                                Supports Microsoft Excel (.xlsx, .xls) and CSV (.csv) up to 50MB
                            </p>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

