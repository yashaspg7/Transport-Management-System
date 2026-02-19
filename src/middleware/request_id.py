import uuid

from fastapi import Request


async def request_id_middleware(request: Request, call_next):
    """Add request ID for tracing."""
    request_id = str(uuid.uuid4())

    # Add to request state
    request.state.request_id = request_id

    response = await call_next(request)

    # Add to response headers
    response.headers["X-Request-ID"] = request_id

    return response
