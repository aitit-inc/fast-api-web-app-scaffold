"""Hello controller."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def hello() -> dict[str, str]:
    """Hello world."""
    return {"message": "Hello world!"}
