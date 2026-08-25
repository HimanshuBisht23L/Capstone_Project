"use client";

import { useState, useRef } from "react";
import { Mic, MicOff, AlertCircle } from "lucide-react";

export default function VoiceMic({ onTranscriptChange }) {
    const [isRecording, setIsRecording] = useState(false);
    const [errorMsg, setErrorMsg] = useState("");
    const recognitionRef = useRef(null);

    const toggleRecording = () => {
        if (isRecording) {
            if (recognitionRef.current) recognitionRef.current.stop();
            setIsRecording(false);
            return;
        }

        const SpeechRecognition =
            window.SpeechRecognition || window.webkitSpeechRecognition;

        if (!SpeechRecognition) {
            setErrorMsg("Web Speech API is not supported in this browser. Please use Google Chrome or Brave.");
            return;
        }

        try {
            const recognition = new SpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.lang = "en-US";

            recognition.onstart = () => {
                setIsRecording(true);
                setErrorMsg("");
            };

            recognition.onresult = (event) => {
                let transcript = "";
                for (let i = 0; i < event.results.length; i++) {
                    transcript += event.results[i][0].transcript;
                }
                onTranscriptChange(transcript);
            };

            recognition.onerror = (event) => {
                console.error("Speech Recognition Error:", event.error);
                console.error("Speech Recognition Message:", event.message);

                setIsRecording(false);

                if (
                    event.error === "not-allowed" ||
                    event.error === "service-not-allowed"
                ) {
                    setErrorMsg(
                        "Microphone access blocked. Please allow microphone access."
                    );

                } else if (event.error === "network") {
                    setErrorMsg(
                        "Speech recognition service could not be reached. Check your internet connection or try another browser."
                    );

                } else if (event.error === "no-speech") {
                    setErrorMsg("No speech detected. Please try again.");

                } else {
                    setErrorMsg(`Speech recognition error: ${event.error}`);
                }
            };

            recognition.onend = () => {
                setIsRecording(false);
            };

            recognitionRef.current = recognition;
            recognition.start();
        } catch (err) {
            console.error("Mic start failure:", err);
            setIsRecording(false);
        }
    };

    return (
        <div className="flex flex-col gap-2">
            <button
                type="button"
                onClick={toggleRecording}
                className={`flex items-center gap-2.5 px-4 py-2.5 rounded-xl text-xs font-bold transition-all shadow-md ${isRecording
                    ? "bg-red-500/20 hover:bg-red-500/30 text-red-300 border border-red-500/40 recording-pulse shadow-red-500/20"
                    : "bg-gradient-to-r from-indigo-600/30 to-purple-600/30 hover:from-indigo-600/40 hover:to-purple-600/40 text-indigo-200 border border-indigo-500/40 hover:border-indigo-400/60 shadow-indigo-500/10"
                    }`}
            >
                {isRecording ? (
                    <>
                        <MicOff className="h-4 w-4 animate-pulse text-red-400" />
                        <span>Listening... (Click to Stop)</span>
                    </>
                ) : (
                    <>
                        <Mic className="h-4 w-4 text-indigo-400" />
                        <span>🎤 Voice Command</span>
                    </>
                )}
            </button>

            {errorMsg && (
                <div className="flex items-start gap-2.5 p-3 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs mt-1">
                    <AlertCircle className="h-4 w-4 shrink-0 mt-0.5" />
                    <span>{errorMsg}</span>
                </div>
            )}
        </div>
    );
}

