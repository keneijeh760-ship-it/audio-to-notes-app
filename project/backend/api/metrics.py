from fastapi import APIRouter
from project.backend.services.metrics_service import get_metrics

router = APIRouter()

@router.get("/metrics")
def metrics():
    return {
        "success": True,
        "data": get_metrics()
    }