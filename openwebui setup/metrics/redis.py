import redis
from prometheus_client import Gauge

REDIS_UP = Gauge("openwebui_redis_up", "Redis availability (1 = up, 0 = down)")

REDIS_CONNECTED_CLIENTS = Gauge("openwebui_redis_connected_clients", "Connected Redis clients")

REDIS_USED_MEMORY = Gauge("openwebui_redis_used_memory_bytes", "Redis memory usage")

REDIS_BLOCKED_CLIENTS = Gauge("openwebui_redis_blocked_clients", "Redis blocked clients")

def collect_redis_metrics(redis_url: str | None):
    # 🔒 Guard: Redis not configured
    if not redis_url:
        REDIS_UP.set(0)
        return

    try:
        r = redis.from_url(redis_url, socket_connect_timeout=1)
        info = r.info()

        REDIS_UP.set(1)
        REDIS_CONNECTED_CLIENTS.set(info.get("connected_clients", 0))
        REDIS_USED_MEMORY.set(info.get("used_memory", 0))
        REDIS_BLOCKED_CLIENTS.set(info.get("blocked_clients", 0))
    except Exception:
        # 🔒 Redis down → fail safely
        REDIS_UP.set(0)
