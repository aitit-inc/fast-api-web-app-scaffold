"""Base router"""
from fastapi import APIRouter

from app.interfaces.controllers.v1.base import v1_router

router = APIRouter(prefix='/api')

router.include_router(v1_router, prefix='/v1')


@router.get('/health-check')
async def root() -> dict[str, str]:
    return {'status': 'Healthy.'}
