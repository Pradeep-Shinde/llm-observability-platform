import psutil
from prometheus_client import Gauge

CPU_USAGE = Gauge("openwebui_cpu_usage_percent", "CPU usage percentage")

CPU_CORES = Gauge("openwebui_cpu_cores", "Number of CPU cores")

MEMORY_TOTAL = Gauge("openwebui_memory_total_bytes", "Total system memory in bytes")

MEMORY_USAGE = Gauge("openwebui_memory_usage_bytes", "Memory usage in bytes")

def collect_system_metrics():
    vm = psutil.virtual_memory()
    CPU_USAGE.set(psutil.cpu_percent(interval=None))
    CPU_CORES.set(psutil.cpu_count())
    MEMORY_USAGE.set(vm.used)
    MEMORY_TOTAL.set(vm.total)
