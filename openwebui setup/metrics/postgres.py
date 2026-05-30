import os
import psycopg2
from prometheus_client import Gauge

POSTGRES_ACTIVE_CONNECTIONS = Gauge("openwebui_postgres_active_connections", "Active Postgres connections")

POSTGRES_IDLE_CONNECTIONS = Gauge("openwebui_postgres_idle_connections", "Idle Postgres connections")

POSTGRES_TOTAL_CONNECTIONS = Gauge("openwebui_postgres_total_connections", "Total Postgres connections")


def collect_postgres_metrics():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        return
    try:
        conn = psycopg2.connect(db_url, connect_timeout=2)
        cur = conn.cursor()

        cur.execute("""SELECT state, COUNT(*) FROM pg_stat_activity GROUP BY state;""")
        rows = cur.fetchall()

        active = 0
        idle = 0
        total = 0

        for state, count in rows:
            total += count
            if state == "active":
                active = count
            elif state == "idle":
                idle = count

        POSTGRES_ACTIVE_CONNECTIONS.set(active)
        POSTGRES_IDLE_CONNECTIONS.set(idle)
        POSTGRES_TOTAL_CONNECTIONS.set(total)

        cur.close()
        conn.close()

    except Exception:
        pass
