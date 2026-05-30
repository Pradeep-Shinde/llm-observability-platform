import os
import requests

PROM_URL = os.getenv("PROMETHEUS_URL", "http://localhost:19090")

def query(promql: str):

    response = requests.get(
        f"{PROM_URL}/api/v1/query",
        params={"query": promql},
        timeout=5,
    )

    response.raise_for_status()

    return response.json()