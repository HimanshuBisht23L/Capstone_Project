import { NextResponse } from "next/server";

export async function POST(request) {
    try {
        const body = await request.json();
        const backendUrl = process.env.BACKEND_URL || "http://localhost:8000";

        const res = await fetch(`${backendUrl}/api/v1/jobs/execute`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
        });

        const data = await res.json();
        return NextResponse.json(data, { status: res.status });
    } catch (error) {
        console.error("Next.js API Proxy Execute Error:", error);
        return NextResponse.json(
            { detail: "Failed to connect to backend job execution engine." },
            { status: 500 }
        );
    }
}
