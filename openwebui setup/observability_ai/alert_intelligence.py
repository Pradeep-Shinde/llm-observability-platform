from .metrics_collector import collect_observability_data
from .anomaly_detector import detect_anomalies
from .llm import ask_llm
from .prompts import build_alert_prompt

def analyze_alert(alert):
    metrics = collect_observability_data()
    anomalies = detect_anomalies()
    anomalies = "No anomalies detected" if not anomalies else anomalies
    prompt = build_alert_prompt(alert, metrics, anomalies)
    return ask_llm(prompt)