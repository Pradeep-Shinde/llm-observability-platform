from .prometheus_client import query

def get_metric_value(result):

    results = result.get("data", {}).get("result", [])

    if not results:
        return 0.0

    return float(results[0]["value"][1])


def collect_metrics():

    cpu = get_metric_value(query("openwebui_cpu_usage_percent"))

    memory = get_metric_value(query("openwebui_memory_usage_bytes"))

    rps = get_metric_value(
        query(
            "rate(custom_openwebui_http_requests_global_total[5m])"
        )
    )

    p99 = get_metric_value(
        query(
            """
            histogram_quantile(
              0.99,
              sum(
                rate(
                  custom_openwebui_http_request_latency_seconds_bucket[5m]
                )
              ) by (le)
            )
            """
        )
    )

    errors = get_metric_value(
        query(
            """
            sum(
              rate(
                custom_openwebui_http_requests_total{
                  status_code=~"5.."
                }[5m]
              )
            )
            """
        )
    )

    return {
        "cpu": round(cpu, 2),
        "memory_mb": round(memory / 1024 / 1024, 2),
        "rps": round(rps, 2),
        "p99_latency": round(p99, 2),
        "error_rate": round(errors, 2),
    }