# 🚀 SheetPilot AI: System Architecture, Data Flow & Production Scaling (100k+ Users)

This document explains the end-to-end operational flow of **SheetPilot AI**, detailing how user requests move from the Next.js frontend and Streamlit control room through the FastAPI backend, how files are managed in Local MVP vs Production Cloud S3, what data enters PostgreSQL, and how natural language commands execute safely in an AST-secured sandbox.

---

## 📌 Executive Summary & Architecture Overview

SheetPilot AI is an asynchronous, secure AI-driven spreadsheet automation platform. It allows users to manipulate Excel (`.xlsx`, `.xls`) and CSV (`.csv`) workbooks using natural language or voice commands.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                   FRONTEND (Next.js 14)                                 │
│  - File Upload Dropzone    - Voice Web Speech API    - Interactive Workspace Studio     │
└───────────────────────────┬─────────────────────────────────────────────----------------┘
                                            │ HTTP REST (JSON / Multipart Forms)
                                            ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                  BACKEND API (FastAPI)                                  │
│  - /api/v1/files/upload     - /api/v1/plan/generate     - /api/v1/jobs/execute          │
└───────┬───────────────────┬───────────────────────────────┬─────────────---------------─┘
        │                                   │                               │
        ▼                                   ▼                               ▼
┌──────────────┐                  ┌──────────────────┐           ┌──────────────────────┐
│ Storage      │                  │ AI & Security    │           │ AST Sandbox          │
│ Service      │                  │ Engine           │           │ Subprocess Runner    │
└───────┬──────┘                  └─────────┬────────┘           └──────────┬───────────┘
        │                                   │                               │
        ▼                                   ▼                               ▼
┌──────────────┐                  ┌──────────────────┐           ┌──────────────────────┐
│ Local Disk   │                  │ PostgreSQL DB    │           │ OS Temp Directory    │
│ Storage      │                  │ (SQLAlchemy)     │           │ (Isolated Execution) │
│ (storage/)   │                  └──────────────────┘           └──────────────────────┘
└──────────────┘
```

---

## 🌲 End-to-End System Tree-Structure Data Flow

```mermaid
graph TD
    Root["🚀 SheetPilot AI System Architecture"]

    %% Node 1: User Interface Layer
    Root --> UI["1. User & Client Interface Layer"]
    UI --> UI_FE["Next.js 14 Interactive Studio (http://localhost:3000)"]
    UI --> UI_ST["Streamlit Operations Control Room (http://localhost:8501)"]
    
    UI_FE --> FE_A["File Upload Dropzone (.xlsx, .xls, .csv up to 50MB)"]
    UI_FE --> FE_B["Browser Web Speech API Voice Controller"]
    UI_FE --> FE_C["Interactive Prompt & Quick Suggestion Pills"]

    UI_ST --> ST_A["10-Benchmark Dataset Suite Selector (docs/test_datasets/)"]
    UI_ST --> ST_B["Ground-Truth Tabular Inspector (st.data_editor)"]
    UI_ST --> ST_C["AST Security Audit & Failure Tracing Sandbox"]

    %% Node 2: FastAPI Gateway Layer
    Root --> API["2. FastAPI Web Gateway & Router (http://localhost:8000)"]
    API --> API_UP["POST /api/v1/files/upload"]
    API --> API_PL["POST /api/v1/agent/plan"]
    API --> API_EX["POST /api/v1/jobs/execute & GET /api/v1/jobs/{job_id}"]
    API --> API_DL["GET /api/v1/jobs/results/{job_id}/download"]

    %% Node 3: Phase 1 Upload & Schema Extraction
    API_UP --> P1["Phase 1: Workbook Ingestion & Schema Extraction"]
    P1 --> P1_A["SpreadsheetService.extract_workbook_schema()"]
    P1_A --> P1_A1["Header Auto-Detection (_detect_header_row)"]
    P1_A --> P1_A2["Data Type Standardizer (string, float64, int64, boolean)"]
    P1_A --> P1_A3["Non-Null Sample Values Extraction"]
    P1 --> P1_B["File Persistence & DB Metadata"]
    P1_B --> P1_B1["Save Raw File to backend/storage/{file_uuid}.xlsx"]
    P1_B --> P1_B2["Persist File Metadata Record in PostgreSQL / SQLite"]

    %% Node 4: Phase 2 AI Planning & Code Generation
    API_PL --> P2["Phase 2: Natural Language AI Planning & Code Synthesis"]
    P2 --> P2_AI["AIService Engine"]
    P2_AI --> P2_AI1["Google Gemini API Call (gemini-2.5-flash / 1.5-flash)"]
    P2_AI --> P2_AI2["Rule-Based Deterministic NLP Fallback Parser"]
    P2_AI --> P2_AI3["Zero-Hallucination Column Constraint Verifier"]
    P2 --> P2_CG["CodeGenService Engine"]
    P2_CG --> P2_CG1["Pydantic ActionPlanPayload Synthesis"]
    P2_CG --> P2_CG2["Synthesizes Executable Pandas & OpenPyXL Python Code"]

    %% Node 5: Phase 3 AST Audit & Sandbox Execution
    API_EX --> P3["Phase 3: AST Security Audit & Subprocess Sandbox Execution"]
    P3 --> P3_AST["Static AST Security Auditor"]
    P3_AST --> P3_AST1["SecurityASTVisitor Scan"]
    P3_AST1 --> AST_Pass["✅ Passed: Safe Python Abstract Syntax Tree"]
    P3_AST1 --> AST_Fail["❌ Blocked: Security Error (Forbidden os, sys, eval)"]
    P3 --> P3_SB["SandboxRunner Execution Engine"]
    P3_SB --> P3_SB1["Isolated Child Subprocess (10-Second Timeout Limit)"]
    P3_SB --> P3_SB2["Multi-Sheet Execution (sheets_dict Container)"]
    P3_SB --> P3_SB3["Differential Metrics Calculation (_calculate_diff)"]
    P3_SB --> P3_SB4["Save Transformed Output to storage/transformed_{id}.xlsx"]

    %% Node 6: Phase 4 Result Inspection & Download
    API_DL --> P4["Phase 4: Inspection Telemetry & File Download"]
    P4 --> P4_A["Cell Differential Metrics Display (Rows Delta, Modified Sheets)"]
    P4 --> P4_B["Execution Latency Telemetry (Subprocess Runtime in ms)"]
    P4 --> P4_C["Binary Stream Workbook Download (HTTP 200 File Attachment)"]

---

## 🏭 Local MVP vs. Production System Design (100k Users)

| Dimension | 🛠️ Local MVP Architecture (Current) | ☁️ Enterprise Production Architecture (100k+ Users) |
| :--- | :--- | :--- |
| **Binary Storage** | Local Disk (`backend/storage/`) | **AWS S3 / MinIO Object Storage** (Direct Presigned URLs) |
| **Server State** | Stateful single server | **100% Stateless FastAPI Clusters** (Auto-scaling ECS/EKS) |
| **Temp Script Lifecycle** | OS Temp folder (`/tmp`), deleted immediately | **Ephemeral Worker Containers** (In-Memory execution, destroyed on completion) |
| **Job Execution** | FastAPI `BackgroundTasks` | **Redis Queue (RQ) / Celery Workers** across dedicated GPU/CPU nodes |
| **Storage Cleanup** | Manual file deletion | **S3 Lifecycle TTL Policies** (Auto-delete transformed files after 7 days) |

---

## 🌐 Enterprise Cloud Architecture: 100k - 1,000,000 Users Scale

### Question 1: If files upload directly to AWS S3, how does the backend server access them for further processing?

```
1. Upload Phase (Direct Browser to S3)
   Browser ──(Presigned S3 PUT URL)──► AWS S3 Bucket (uploads/{uuid}.xlsx)
                                             │
2. Schema & Sandbox Processing Phase        │
   FastAPI Worker ◄──(Stream io.BytesIO)────┘
   └─► Sandbox Mutates Cell Data in RAM Memory
   └─► Streams Transformed Workbook Back ──► AWS S3 Bucket (transformed/{uuid}.xlsx)
```

1. **Presigned Upload (Zero Disk Overhead on API Server)**:
   * Next.js requests a **Presigned PUT URL** from FastAPI (`GET /api/v1/files/presigned-url`).
   * Browser uploads `data.xlsx` directly to `https://s3.amazonaws.com/uploads/{uuid}.xlsx`.
   * The FastAPI server disk receives **0 MB** of binary data!

2. **In-Memory Streaming Processing (`io.BytesIO`)**:
   * When Sandbox execution begins, worker nodes do not download files to local disk.
   * `boto3` streams the binary file directly from S3 into an **In-Memory Buffer (`io.BytesIO`)**.
   * OpenPyXL / Pandas reads the stream, executes AST-verified mutations, and saves the modified buffer back to S3 (`s3.put_object(Key='transformed/...')`).
   * **Result:** No local hard drive space is consumed!

---

### Question 2: How do S3, Cloudflare R2, Redis, and Celery Workers handle 1,000,000 concurrent requests?

```
┌─────────────────┐
│ User Requests   │ (1,000,000 concurrent users)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ NGINX / Cloudflare│ (Global Edge CDN Load Balancing)
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│ FastAPI API Server Cluster (Auto-scales 1 -> 50 Pods)    │
└────────────────────────┬────────────────────────────────┘
                         │ Pushes Job Payload (JSON) in < 1ms
                         ▼
┌─────────────────────────────────────────────────────────┐
│ Redis Queue Broker (Handles 1,000,000 msgs/sec in RAM)  │
└────────────────────────┬────────────────────────────────┘
                         │ Distributes Jobs across Worker Pool
                         ▼
┌─────────────────────────────────────────────────────────┐
│ Celery / RQ Worker Pool (Auto-scales 10 -> 200 Workers) │
│ [Worker 1]  [Worker 2]  [Worker 3] ... [Worker 200]    │
└─────────────────────────────────────────────────────────┘
```

1. **AWS S3 / Cloudflare R2 High-Concurrency Capacity**:
   * AWS S3 automatically scales to support **3,500 WRITE requests/sec** and **5,500 READ requests/sec PER PREFIX**. With UUID prefixes, S3 handles **millions of concurrent file transfers** without slowdown!
   * Cloudflare R2 runs on 300+ global edge locations worldwide.

2. **Current Project Workers vs Production Workers**:
   * **Current Local Setup:** 1 FastAPI process running 1 async thread loop.
   * **Production Cloud Setup:** **Kubernetes HPA (Horizontal Pod Autoscaler)** running **200+ Celery Worker containers**.

3. **How Redis Flows under 1 Million Requests**:
   * **FastAPI (Producer):** Receives user request and pushes `job_id` JSON to Redis (`redis.rpush()`) in **0.5 milliseconds**.
   * **Redis (Broker):** Keeps queue pointers in high-speed RAM (capable of **1,000,000 operations per second**).
   * **Celery Workers (Consumers):** Worker pods continuously pop jobs from Redis (`redis.blpop()`), stream S3 data, execute AST sandbox scripts, and update status in PostgreSQL!
