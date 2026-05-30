import os
from fastapi import APIRouter, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from open_webui.metrics.system import collect_system_metrics
from open_webui.metrics.process import collect_process_metrics
from open_webui.metrics.redis import collect_redis_metrics
from open_webui.metrics.postgres import collect_postgres_metrics

router = APIRouter(tags=["metrics"])

@router.get("/")
def metrics():
    collect_system_metrics()
    collect_process_metrics()
    collect_redis_metrics(os.getenv("REDIS_URL"))
    collect_postgres_metrics()
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
