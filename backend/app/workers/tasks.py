import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.file import File
from app.models.agent_request import DBActionPlan, AgentRequest
from app.models.execution_job import ExecutionJob
from app.sandbox.runner import SandboxRunner
from app.services.storage_service import StorageService

def run_execution_job_async(job_id: str):
    """
    Background worker task executed asynchronously by Redis RQ worker.
    """
    asyncio.run(_execute_job_async_internal(job_id))

async def _execute_job_async_internal(job_id: str):
    async with AsyncSessionLocal() as session:
        # 1. Fetch ExecutionJob ORM Record
        res_job = await session.execute(select(ExecutionJob).where(ExecutionJob.id == job_id))
        job = res_job.scalar_one_or_none()

        if not job:
            print(f"❌ Worker Error: ExecutionJob {job_id} not found.")
            return

        # Update status to PROCESSING
        job.status = "PROCESSING"
        await session.commit()

        try:
            # 2. Fetch ActionPlan
            res_plan = await session.execute(select(DBActionPlan).where(DBActionPlan.id == job.plan_id))
            plan = res_plan.scalar_one_or_none()

            if not plan:
                job.status = "FAILED"
                job.error_log = "Associated DBActionPlan record not found."
                await session.commit()
                return

            # 3. Fetch AgentRequest to get file_id
            res_req = await session.execute(select(AgentRequest).where(AgentRequest.id == plan.request_id))
            req = res_req.scalar_one_or_none()

            if not req:
                job.status = "FAILED"
                job.error_log = "Associated AgentRequest record not found."
                await session.commit()
                return

            # 4. Fetch File record
            res_file = await session.execute(select(File).where(File.id == req.file_id))
            file_rec = res_file.scalar_one_or_none()

            if not file_rec:
                job.status = "FAILED"
                job.error_log = "Associated File record not found."
                await session.commit()
                return

            input_path = StorageService.get_file_path(file_rec.storage_key)

            # 5. Execute in Sandbox (Offloaded to threadpool to avoid event loop blocking)
            success, output_key, diff_summary, execution_time_ms, stdout_log = await asyncio.to_thread(
                SandboxRunner.execute_in_sandbox,
                python_code=plan.generated_code,
                input_file_path=input_path,
                output_file_name=f"output_{job_id}.xlsx"
            )

            # 6. Update ExecutionJob Status
            if success:
                job.status = "SUCCESS"
                job.output_file_key = output_key
                job.diff_summary = diff_summary
                job.execution_time_ms = execution_time_ms
                job.error_log = stdout_log
            else:
                job.status = "FAILED"
                job.execution_time_ms = execution_time_ms
                job.error_log = stdout_log

            await session.commit()
            print(f"✅ Worker Job {job_id} completed with status: {job.status}")

        except Exception as e:
            job.status = "FAILED"
            job.error_log = f"Worker Exception: {str(e)}"
            await session.commit()
            print(f"❌ Worker Exception on Job {job_id}: {e}")
