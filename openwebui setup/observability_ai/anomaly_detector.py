from .prometheus_tools import (
    get_cpu_usage,
    get_memory_usage,
    get_error_rate,
)


def detect_anomalies():
    anomalies_list = []
    try:
        cpu = float(
            get_cpu_usage()
            .split(":")[1]
            .replace("%", "")
            .strip()
        )

        if cpu > 90:
            anomalies_list.append(
                {
                    "severity": "critical",
                    "metric": "cpu",
                    "value": cpu,
                    "message": f"CPU usage is {cpu}%"
                }
            )
    except (ValueError, IndexError):
        pass

    try:
        memory = float(
            get_memory_usage()
            .split(":")[1]
            .replace("MB", "")
            .strip()
        )

        if memory > 12000:
            anomalies_list.append(
                {
                    "severity": "warning",
                    "metric": "memory",
                    "message": f"Memory usage is {memory} MB"
                }
            )
    except (ValueError, IndexError):
        pass

    try:
        errors = float(
            get_error_rate()
            .split(":")[1]
            .replace("errors/sec", "")
            .strip()
        )

        if errors > 1:
            anomalies_list.append(
                {
                    "severity": "critical",
                    "metric": "errors",
                    "message": f"5xx error rate is {errors}"
                }
            )
    except (ValueError, IndexError):
        pass

    return anomalies_list