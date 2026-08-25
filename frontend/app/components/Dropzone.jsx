"use client";

import { useState } from "react";
import { UploadCloud, FileSpreadsheet, CheckCircle2, Loader2 } from "lucide-react";

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
            className={`glass-panel rounded-2xl p-8 text-center border-2 border-dashed transition-all relative glow-on-hover ${dragActive
                    ? "border-cyan-400 bg-cyan-950/20"
                    : uploadedFileName
                        ? "border-emerald-500/50 bg-emerald-950/10"
                        : "border-slate-700/60 bg-slate-900/40"
                }`}
        >
            <input
                type="file"
                accept=".xlsx, .xls, .csv"
                onChange={handleChange}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                disabled={isUploading}
            />

            <div className="flex flex-col items-center justify-center gap-3">
                {isUploading ? (
                    <div className="flex flex-col items-center gap-2">
                        <Loader2 className="h-10 w-10 text-cyan-400 animate-spin" />
                        <p className="text-sm font-semibold text-slate-300">
                            Parsing workbook & extracting schema...
                        </p>
                    </div>
                ) : uploadedFileName ? (
                    <div className="flex flex-col items-center gap-2">
                        <div className="h-12 w-12 rounded-full bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400">
                            <CheckCircle2 className="h-6 w-6" />
                        </div>
                        <p className="text-base font-bold text-emerald-300">{uploadedFileName}</p>
                        <p className="text-xs text-slate-400">
                            Click or drag another workbook (.xlsx, .csv) to replace
                        </p>
                    </div>
                ) : (
                    <div className="flex flex-col items-center gap-2">
                        <div className="h-12 w-12 rounded-full bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 mb-1">
                            <UploadCloud className="h-6 w-6" />
                        </div>
                        <p className="text-sm font-bold text-slate-200">
                            Drag & Drop your Excel workbook here, or <span className="text-cyan-400 underline">Browse</span>
                        </p>
                        <p className="text-xs text-slate-400">
                            Supports Microsoft Excel (.xlsx, .xls) and CSV (.csv) up to 50MB
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
}
