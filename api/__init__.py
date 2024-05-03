from .kai.routers import router as kai_router
# from .pocket_kai.routers import router as pocket_kai_router

from fastapi import APIRouter

router = APIRouter()

router.include_router(kai_router, prefix='/kai')
# router.include_router(pocket_kai_router, prefix='/pocket_kai')
