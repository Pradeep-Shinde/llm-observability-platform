from .investigation import investigate_question
from .rca import generate_rca
from .anomaly_detector import detect_anomalies
from .llm import ask_llm
from .prompts import build_incident_report_prompt


def generate_incident_report(incident):
    investigation = investigate_question(incident)
    rca = generate_rca(incident)
    anomalies = detect_anomalies()
    anomalies = "No anomalies detected" if not anomalies else anomalies
    prompt = build_incident_report_prompt(incident, investigation, rca, anomalies)
    return ask_llm(prompt)