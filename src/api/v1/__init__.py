from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from .vendor import router as vendor_router

api_router = APIRouter()
api_router.include_router(vendor_router, tags=["Vendors"])


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
