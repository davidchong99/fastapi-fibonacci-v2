from fastapi import APIRouter, Request
from fastapi_pagination import Page, paginate

router = APIRouter(tags=["fibonacci"])


@router.get("/all")
async def get_all(request: Request) -> Page[int]:
    return paginate(request.app.state.fibonacci)
