from prometheus_client import Histogram, Gauge, Counter

CUSTOM_HTTP_REQUEST_LATENCY = Histogram(
    "custom_openwebui_http_request_latency_seconds",
    "HTTP request latency",
    ["method", "status_code", "path"],
    buckets=(0.1, 0.25, 0.5, 1, 2, 3, 5, 8, 13)
)

CUSTOM_HTTP_REQUESTS_IN_PROGRESS = Gauge(
    "custom_openwebui_http_requests_in_progress",
    "Active HTTP requests"
)

CUSTOM_HTTP_REQUESTS_TOTAL = Counter(
    "custom_openwebui_http_requests_total",
    "Total HTTP requests",
    ["method", "status_code", "path"]
)

CUSTOM_HTTP_REQUESTS_GLOBAL = Counter(
    "custom_openwebui_http_requests_global_total",
    "Total HTTP requests (global)"
)