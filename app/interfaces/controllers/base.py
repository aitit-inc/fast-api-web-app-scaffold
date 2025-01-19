"""Base router"""
from fastapi import APIRouter

from app.interfaces.controllers.path import API_BASE_PATH, V1_PREFIX, \
    HEALTH_CHECK_ENDPOINT
from app.interfaces.controllers.v1.base import v1_router

router = APIRouter(prefix=API_BASE_PATH)

router.include_router(v1_router, prefix=V1_PREFIX)


@router.get(HEALTH_CHECK_ENDPOINT)
async def root() -> dict[str, str]:
    """Health check."""
    return {'status': 'Healthy.'}
