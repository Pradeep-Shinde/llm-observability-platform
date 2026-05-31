from .metrics_collector import collect_observability_data
from .prompts import build_rca_prompt
from .llm import ask_llm


def generate_rca(incident):
    data = collect_observability_data()
    prompt = build_rca_prompt(incident, data)
    return ask_llm(prompt)