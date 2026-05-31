from open_webui.observability_ai.incident_report import generate_incident_report
from open_webui.observability_ai.investigation import investigate_question
from open_webui.observability_ai.anomaly_detector import detect_anomalies
from open_webui.observability_ai.alert_intelligence import analyze_alert
from open_webui.observability_ai.summary import generate_summary
from open_webui.observability_ai.ask import answer_question
from open_webui.observability_ai.rca import generate_rca
from open_webui.observability_ai.agent import run_agent
from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

class RCARequest(BaseModel):
    incident: str

class AlertRequest(BaseModel):
    alert: str

class AlertManagerRequest(BaseModel):
    alerts: list

class IncidentRequest(BaseModel):
    incident: str


@router.get("/summary")
def summary():
    return generate_summary()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/ask")
def ask(req: QuestionRequest):
    intent, answer = answer_question(req.question)
    return {
        "question": req.question,
        "intent": intent,
        "answer": answer
    }

@router.post("/investigate")
def investigate(req: QuestionRequest):
    return {
        "question": req.question,
        "investigation": investigate_question(req.question)
    }

@router.post("/rca")
def rca(req: RCARequest):
    return {
        "incident": req.incident,
        "analysis": generate_rca(req.incident)
    }

@router.get("/anomalies")
def anomalies():
    anomalies_detected = detect_anomalies()
    return {
        "count": len(anomalies_detected),
        "anomalies": anomalies_detected
    }

@router.post("/alert-analysis")
def alert_analysis(req: AlertRequest):
    return {
        "alert": req.alert,
        "analysis": analyze_alert(req.alert)
    }

@router.post("/alerts/webhook")
def alertmanager_webhook(req: AlertManagerRequest):
    analyses = []
    for alert in req.alerts:
        alert_name = alert.get("labels", {}).get("alertname", "Unknown Alert")
        analysis = analyze_alert(alert_name)
        analyses.append({"alert": alert_name, "analysis": analysis})
    return {
        "alerts_processed": len(analyses),
        "results": analyses
    }

@router.post("/report")
def incident_report(req: IncidentRequest):
    return {
        "incident": req.incident,
        "report": generate_incident_report(req.incident)
    }

@router.post("/agent")
def agent(req: QuestionRequest):

    return {
        "question": req.question,
        "response": run_agent(req.question)
    }