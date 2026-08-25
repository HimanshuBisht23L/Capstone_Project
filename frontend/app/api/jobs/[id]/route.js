import { NextResponse } from "next/server";

export async function GET(request, { params }) {
    try {
        const { id } = await params;
        const backendUrl = process.env.BACKEND_URL || "http://localhost:8000";

        const res = await fetch(`${backendUrl}/api/v1/jobs/${id}`, {
            cache: "no-store",
        });

        const data = await res.json();
        return NextResponse.json(data, { status: res.status });
    } catch (error) {
        console.error("Next.js API Proxy Job Status Error:", error);
        return NextResponse.json(
            { detail: "Failed to poll job status from backend." },
            { status: 500 }
        );
    }
}
