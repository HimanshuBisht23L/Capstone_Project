import { NextResponse } from "next/server";

export async function GET(request, { params }) {
    try {
        const { id } = await params;
        const backendUrl = process.env.BACKEND_URL || "http://localhost:8000";

        const res = await fetch(`${backendUrl}/api/v1/jobs/results/${id}/download`, {
            cache: "no-store",
        });

        if (!res.ok) {
            return NextResponse.json({ detail: "File download unavailable." }, { status: res.status });
        }

        const fileBuffer = await res.arrayBuffer();
        const contentType = res.headers.get("content-type") || "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";

        return new Response(fileBuffer, {
            status: 200,
            headers: {
                "Content-Type": contentType,
                "Content-Disposition": `attachment; filename="processed_workbook_${id}.xlsx"`,
            },
        });
    } catch (error) {
        console.error("Next.js API Proxy Download Error:", error);
        return NextResponse.json(
            { detail: "Failed to download transformed workbook file." },
            { status: 500 }
        );
    }
}
