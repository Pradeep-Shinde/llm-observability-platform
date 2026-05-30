from fastapi import APIRouter

from open_webui.observability_ai.summary import generate_summary

router = APIRouter()


@router.get("/summary")
def summary():

    return generate_summary()

@router.get("/health")
def health():
    return {"status": "ok"}