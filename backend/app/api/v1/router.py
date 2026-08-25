from fastapi import APIRouter
from app.api.v1.endpoints import files, agent, jobs

api_router = APIRouter()

api_router.include_router(files.router, prefix="/files", tags=["Files & Schema Engine"])
api_router.include_router(agent.router, prefix="/agent", tags=["AI Action Planning"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["Sandbox Job Execution"])
