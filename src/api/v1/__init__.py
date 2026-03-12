from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from .auth import router as auth_router
from .user import router as user_router
from .vendor import router as vendor_router

api_router = APIRouter()
api_router.include_router(vendor_router, tags=["Vendors"])
api_router.include_router(user_router, tags=["Users"])
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])


# Add redirects for API documentation
@api_router.get("/docs", include_in_schema=False)
async def redirect_docs():
    return RedirectResponse(url="/docs")


@api_router.get("/redoc", include_in_schema=False)
async def redirect_redoc():
    return RedirectResponse(url="/redoc")


@api_router.get("/openapi.json", include_in_schema=False)
async def redirect_openapi():
    return RedirectResponse(url="/openapi.json")
