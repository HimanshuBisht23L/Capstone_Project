import { NextResponse } from "next/server";

export async function POST(request) {
    try {
        const formData = await request.formData();
        const backendUrl = process.env.BACKEND_URL || "http://localhost:8000";

        const res = await fetch(`${backendUrl}/api/v1/files/upload`, {
            method: "POST",
            body: formData,
        });

        const data = await res.json();
        return NextResponse.json(data, { status: res.status });
    } catch (error) {
        console.error("Next.js API Proxy Upload Error:", error);
        return NextResponse.json(
            { detail: "Could not connect to backend FastAPI service." },
            { status: 500 }
        );
    }
}
