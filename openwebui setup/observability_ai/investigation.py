from .investigation_prompt import build_investigation_prompt
from .metrics_collector import collect_observability_data
from .llm import ask_llm

def investigate_question(question):
    investigation_data = collect_observability_data()
    prompt = build_investigation_prompt(question, investigation_data)
    answer = ask_llm(prompt)
    return answer