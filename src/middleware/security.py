from fastapi import Request


async def security_headers_middleware(request: Request, call_next):
    """Add basic security headers to responses."""
    response = await call_next(request)

    # Basic security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"

    return response
