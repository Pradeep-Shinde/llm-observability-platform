import math
from .prometheus_client import query


def _get_single_metric(query_result, label, unit=""):
    if not query_result["data"]["result"]:
        return f"{label}: unavailable"

    value = query_result["data"]["result"][0]["value"][1]

    return f"{label}: {value}{unit}"


def _get_endpoint_metric(query_result, unit=""):
    if not query_result["data"]["result"]:
        return "No endpoint data available"

    endpoints = []
    for item in query_result["data"]["result"]:
        path = item["metric"].get("path", "unknown")
        value = float(item["value"][1])
        if math.isnan(value):
            continue
        endpoints.append(f"{path}: {value:.2f}{unit}")
    return "\n".join(endpoints) if endpoints else "No endpoint data available"


def get_cpu_usage():
    result = query("openwebui_cpu_usage_percent")
    return _get_single_metric(result, "CPU Usage", "%")


def get_memory_usage():
    result = query("openwebui_memory_usage_bytes")

    if not result["data"]["result"]:
        return "Memory Usage: unavailable"

    value_bytes = float(result["data"]["result"][0]["value"][1])
    value_mb = round(value_bytes / (1024 * 1024), 2)
    return f"Memory Usage: {value_mb} MB"


def get_memory_total():
    result = query("openwebui_memory_total_bytes")

    if not result["data"]["result"]:
        return "Total Memory: unavailable"

    value_bytes = float(result["data"]["result"][0]["value"][1])

    value_gb = round(value_bytes / (1024 ** 3), 2)
    return f"Total Memory: {value_gb} GB"


def get_memory_health():
    return "\n".join([get_memory_usage(), get_memory_total()])


def get_rps():
    result = query("rate(custom_openwebui_http_requests_global_total[5m])")
    return _get_single_metric(result, "Request Rate", " req/sec")


def get_error_rate():
    result = query(
        """
        sum(rate(custom_openwebui_http_requests_total{
            status_code=~"5.."
        }[5m]))
        """
    )
    return _get_single_metric(result, "5xx Error Rate", " errors/sec")


def get_slowest_endpoints():
    result = query(
        """
        topk(
            5,
            histogram_quantile(
                0.99,
                sum by(path, le)(
                    rate(
                        custom_openwebui_http_request_latency_seconds_bucket[5m]
                    )
                )
            )
        )
        """
    )
    return _get_endpoint_metric(result, " sec")


def get_top_endpoints():
    result = query(
        """
        topk(
            5,
            sum by(path)(
                rate(
                    custom_openwebui_http_requests_total[5m]
                )
            )
        )
        """
    )
    return _get_endpoint_metric(result, " req/sec")


def get_redis_status():
    result = query("openwebui_redis_up")
    return _get_single_metric(result, "Redis Status")


def get_redis_clients():
    result = query("openwebui_redis_connected_clients")
    return _get_single_metric(result, "Connected Redis Clients")


def get_redis_blocked_clients():
    result = query("openwebui_redis_blocked_clients")
    return _get_single_metric(result, "Blocked Redis Clients")


def get_redis_memory():
    result = query("openwebui_redis_used_memory_bytes")

    if not result["data"]["result"]:
        return "Redis Memory Usage: unavailable"

    value_bytes = float(result["data"]["result"][0]["value"][1])
    value_mb = round(value_bytes / (1024 * 1024),2)
    return f"Redis Memory Usage: {value_mb} MB"


def get_redis_health():
    return "\n".join([get_redis_status(), get_redis_clients(), get_redis_blocked_clients(), get_redis_memory()])


def get_postgres_active_connections():
    result = query("openwebui_postgres_active_connections")
    return _get_single_metric(result, "Active Postgres Connections")


def get_postgres_idle_connections():
    result = query("openwebui_postgres_idle_connections")
    return _get_single_metric(result, "Idle Postgres Connections")


def get_postgres_total_connections():
    result = query("openwebui_postgres_total_connections")
    return _get_single_metric(result, "Total Postgres Connections")


def get_postgres_health():
    return "\n".join([get_postgres_active_connections(), get_postgres_idle_connections(), get_postgres_total_connections()])
