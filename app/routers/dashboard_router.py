from fastapi import APIRouter
from app.services import dashboard_services

router = APIRouter(prefix="/dashboard", tags=["统计"])



@router.get("/stats")
async def get_stats():
    return await dashboard_services.get_stats()