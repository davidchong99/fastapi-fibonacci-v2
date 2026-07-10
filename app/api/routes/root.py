from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter(tags=["root"])


@router.get("/", response_class=PlainTextResponse)
async def get_root() -> str:
    return "Root ..."
