import os
import time
import psutil
from prometheus_client import Gauge

PROCESS_START_TIME = Gauge("openwebui_process_start_time", "Process start time (unix)")

PROCESS_UPTIME = Gauge("openwebui_process_uptime_seconds", "Process uptime in seconds")

PROCESS_RSS = Gauge("openwebui_process_rss_bytes", "Resident memory used by OpenWebUI process")

_process_start_unix = time.time()
_process_start_monotonic = time.monotonic()

PROCESS_START_TIME.set(_process_start_unix)

def collect_process_metrics():
    PROCESS_UPTIME.set(time.monotonic() - _process_start_monotonic)
    PROCESS_RSS.set(psutil.Process().memory_info().rss)
