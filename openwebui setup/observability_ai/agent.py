from .investigation import investigate_question
from .rca import generate_rca
from .anomaly_detector import detect_anomalies
from .alert_intelligence import analyze_alert
from .llm import ask_llm
from .prompts import build_agent_prompt


def run_agent(question):
    investigation = investigate_question(question)
    rca = generate_rca(question)
    anomalies = detect_anomalies()
    if not anomalies:
        anomalies = "No anomalies detected."
    else:
        anomalies = "\n".join(f"- {a['metric']}: {a['message']}" for a in anomalies)
    alert_analysis = analyze_alert(question)
    prompt = build_agent_prompt(
        question=question,
        investigation=investigation,
        rca=rca,
        anomalies=anomalies,
        alert_analysis=alert_analysis
    )
    return ask_llm(prompt)