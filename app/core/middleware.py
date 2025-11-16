import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()

        response = await call_next(request)
        process_time = time.time() - start

        logging.info(
            f"{request.method} {request.url.path} - {response.status_code} "
            f"({process_time:.3f}s)"
        )

        return response


def register_middleware(app):
    app.add_middleware(RequestLoggingMiddleware)