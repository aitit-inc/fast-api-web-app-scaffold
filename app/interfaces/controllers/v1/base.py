from fastapi import APIRouter

from app.interfaces.controllers.v1 import sample_item

v1_router = APIRouter()

v1_router.include_router(sample_item.router)
