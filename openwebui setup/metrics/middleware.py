import re
import time
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from open_webui.metrics.http import (CUSTOM_HTTP_REQUEST_LATENCY, CUSTOM_HTTP_REQUESTS_IN_PROGRESS, CUSTOM_HTTP_REQUESTS_TOTAL, CUSTOM_HTTP_REQUESTS_GLOBAL)

UUID_RE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.IGNORECASE)

def normalize_path(path: str) -> str:
    return UUID_RE.sub("{id}", path)

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.scope["type"] != "http":
            return await call_next(request)

        start = time.time()
        CUSTOM_HTTP_REQUESTS_IN_PROGRESS.inc()

        try:
            response = await call_next(request)

            CUSTOM_HTTP_REQUESTS_GLOBAL.inc()

            method = request.method
            status = str(response.status_code)
            raw_path = request.url.path
            path = normalize_path(raw_path)
            duration = time.time() - start

            CUSTOM_HTTP_REQUESTS_TOTAL.labels(method=method, status_code=status, path=path).inc()

            CUSTOM_HTTP_REQUEST_LATENCY.labels(method=method, status_code=status, path=path).observe(duration)

            return response

        finally:
            CUSTOM_HTTP_REQUESTS_IN_PROGRESS.dec()
