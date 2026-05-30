from .metrics_collector import collect_metrics
from .prompts import build_summary_prompt
from datetime import datetime
from .llm import ask_llm
import logging


def generate_summary():

    metrics = collect_metrics()

    prompt = build_summary_prompt(metrics)

    try:
        analysis = ask_llm(prompt)
    except Exception as e:
        analysis = f"AI analysis failed: {str(e)}"

    logger = logging.getLogger(__name__)
    logger.info(
        "Generated AI summary with metrics=%s",
        metrics
    )

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "metrics": metrics,
        "analysis": analysis,
    }