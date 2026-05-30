# LLM Observability Platform

A production-inspired observability platform for LLM applications built using OpenWebUI, LiteLLM, Ollama, Langfuse, Prometheus, and Grafana.

The platform provides end-to-end monitoring, tracing, performance analysis, and infrastructure visibility for self-hosted LLM workloads. 
It extends OpenWebUI with custom Prometheus instrumentation and Grafana dashboards to improve operational visibility, debugging, and performance analysis.

<img src="Screenshots/grafana-dashboard-1.png" width="2560" alt="Grafana Dashboard Overview">

---

# Features

* ✅ Local LLM inference using Ollama (Llama 3)
* ✅ LiteLLM proxy integration
* ✅ Langfuse tracing and monitoring
* ✅ Custom Prometheus instrumentation
* ✅ HTTP request metrics and latency tracking
* ✅ PostgreSQL monitoring
* ✅ Redis monitoring
* ✅ Grafana dashboards
* ✅ Per-endpoint observability
* ✅ HTTP status code monitoring (2xx/4xx/5xx)
* ✅ P99 latency tracking
* ✅ Endpoint normalization to prevent metric cardinality explosion
* ✅ AI-powered observability assistant (/api/ai/summary)
* ✅ LLM-based metric analysis
* ✅ Automated operational insight generation

---

# Overview

Modern LLM applications require visibility across application requests, infrastructure components, and model interactions. This project was built to provide a unified observability layer for an OpenWebUI-based LLM stack.

The platform collects and visualizes:

* LLM request traffic
* Endpoint-level request rates
* HTTP latency and P99 response times
* HTTP status code distribution
* Redis health metrics
* PostgreSQL connection metrics
* Process resource consumption
* System-level CPU and memory utilization
* Langfuse traces for LLM interactions

The platform also includes an AI-powered observability assistant that analyzes Prometheus metrics using LiteLLM and Llama 3 to generate operational summaries and health assessments.
The goal is to provide production-style monitoring and telemetry for local and self-hosted LLM environments.

---

# Architecture

```text
                        ┌─────────────────┐
                        │      User       │
                        └────────┬────────┘
                                 │
                                 ▼
                     ┌──────────────────────────┐
                     │       OpenWebUI          │
                     │        Port 3000         │
                     └───────────┬──────────────┘
                                 │
                                 │ Chat Requests
                                 ▼
                     ┌──────────────────────────┐
                     │         LiteLLM          │
                     │        Port 4000         │
                     └───────────┬──────────────┘
                                 │
                                 │ Inference
                                 ▼
                     ┌──────────────────────────┐
                     │         Ollama           │
                     │        Llama 3           │
                     │       Port 11434         │
                     └──────────────────────────┘


     ┌─────────────────────────────────────────────────────────┐
     │                    LLM Observability                    │
     └─────────────────────────────────────────────────────────┘

                     ┌──────────────────────────┐
                     │        LiteLLM           │
                     │  OTEL / Langfuse Trace   │
                     └───────────┬──────────────┘
                                 │
                                 ▼
                     ┌──────────────────────────┐
                     │         Langfuse         │
                     │        Port 3100         │
                     └──────┬──────┬──────┬─────┘
                            │      │      │
                            │      │      │
                            ▼      ▼      ▼
                    ┌─────────┐ ┌──────┐ ┌────────────┐
                    │Postgres │ │Redis │ │ ClickHouse │
                    └─────────┘ └──────┘ └────────────┘
                                           │
                                           ▼
                                      ┌────────┐
                                      │ MinIO  │
                                      └────────┘


     ┌─────────────────────────────────────────────────────────┐
     │                    Metrics Pipeline                     │
     └─────────────────────────────────────────────────────────┘

                     ┌──────────────────────────┐
                     │       OpenWebUI          │
                     │ Custom Middleware &      │
                     │ Prometheus Metrics       │
                     └───────────┬──────────────┘
                                 │
                                 │ /metrics
                                 ▼
                     ┌──────────────────────────┐
                     │       Prometheus         │
                     │        Port 19090        │
                     └───────────┬──────────────┘
                                 │
                                 │ Queries
                                 ▼
                     ┌──────────────────────────┐
                     │         Grafana          │
                     │        Port 3001         │
                     └──────────────────────────┘


     ┌─────────────────────────────────────────────────────────┐
     │               AI Observability Assistant                │
     └─────────────────────────────────────────────────────────┘

                    ┌──────────────────────────┐
                    │       Prometheus         │
                    └───────────┬──────────────┘
                                │
                                ▼
                    ┌──────────────────────────┐
                    │ AI Observability         │
                    │ Assistant                │
                    └───────────┬──────────────┘
                                │
                                ▼
                    ┌──────────────────────────┐
                    │         LiteLLM          │
                    └───────────┬──────────────┘
                                │
                                ▼
                    ┌──────────────────────────┐
                    │        Llama 3           │
                    └──────────────────────────┘
```

---

# Technology Stack

## LLM Layer

* OpenWebUI
* LiteLLM
* Ollama
* Llama 3

### AI Stack

* Prometheus
* LiteLLM
* Ollama
* Llama 3

## Observability

* Prometheus
* Grafana
* Langfuse

## Infrastructure

* PostgreSQL
* Redis
* ClickHouse
* MinIO
* Docker

## Backend

* Python
* FastAPI
* Starlette Middleware
* Prometheus Client

---

# Custom Engineering Work

## HTTP Observability

Implemented custom Starlette middleware for collecting:

* Request rate (RPS)
* Active requests
* HTTP status codes
* Endpoint-level metrics
* Request latency
* P99 latency

### Metrics

* `custom_openwebui_http_requests_total`
* `custom_openwebui_http_requests_global_total`
* `custom_openwebui_http_request_latency_seconds`
* `custom_openwebui_http_requests_in_progress`

---

## Redis Monitoring

Added custom Redis metrics:

* Connected clients
* Used memory
* Blocked clients

---

## PostgreSQL Monitoring

Added custom PostgreSQL metrics:

* Active connections
* Idle connections
* Total connections

---

## Process & System Metrics

Implemented monitoring for:

### System

* CPU utilization
* Memory utilization

### Process

* Process uptime
* Process start time
* RSS memory usage

---

## Cardinality Optimization

Implemented dynamic endpoint normalization to prevent Prometheus metric cardinality explosion.

### Before

```text
/api/v1/chats/969c6688-e661-49bd-9550-40e0ba00ffa2
/api/v1/chats/12345678-abcd-efgh-ijkl-987654321000
```

### After

```text
/api/v1/chats/{id}
```

This significantly improves:

* Prometheus performance
* Dashboard readability
* Query efficiency
* Metric scalability

---

# Grafana Dashboards

The dashboard provides visibility into:

## Traffic Monitoring

* Global Requests Per Second (RPS)
* Endpoint-level RPS
* Traffic distribution

## HTTP Monitoring

* 2xx Success Responses
* 4xx Client Errors
* 5xx Server Errors
* Status code trends

## Performance Monitoring

* Endpoint-level P99 latency
* Request latency distribution
* Active requests

## Infrastructure Monitoring

### Redis

* Connected clients
* Used memory
* Blocked clients

### PostgreSQL

* Active connections
* Idle connections
* Total connections

### System

* CPU utilization
* Memory utilization
* Process uptime
* RSS memory

---


# AI Observability Assistant

The platform includes an AI-powered observability assistant that analyzes Prometheus metrics and generates operational insights using LiteLLM and Llama 3.

### API

GET /api/ai/summary

### Example

curl http://localhost:3000/api/ai/summary

### Example Response

Example response generated from live Prometheus metrics using LiteLLM and Llama 3.

```json
{
  "timestamp": "2026-05-30T08:17:41.847241",
  "metrics": {
    "cpu": 62.4,
    "memory_mb": 8148.02,
    "rps": 0.21,
    "p99_latency": 13.0,
    "error_rate": 0.0
  },
  "analysis": "Health Status: The system is experiencing high CPU usage and elevated memory consumption..."
}
```

Returns:

- Health Status
- Observations
- Risks Visible From Metrics
- Additional Data Needed

The assistant uses Prometheus metrics as context and generates structured operational summaries for troubleshooting and system monitoring.


---

# Screenshots

## AI Observability Assistant

<img src="Screenshots/ai_observability_summary.png" width="2920" alt="AI Observability Assistant Summary API">

## Grafana Dashboard

<img src="Screenshots/grafana-dashboard-1.png" width="2560" alt="Grafana Dashboard Overview">

<img src="Screenshots/grafana-dashboard-2.png" width="2558" alt="Grafana HTTP Metrics">

<img src="Screenshots/grafana-dashboard-3.png" width="2560" alt="Grafana Redis and PostgreSQL Metrics">

<img src="Screenshots/grafana-dashboard-4.png" width="2555" alt="Grafana System Metrics">

---

## Langfuse Traces

<img src="Screenshots/langfuse-traces.png" width="2559" alt="Langfuse Traces">

---

## OpenWebUI

<img src="Screenshots/openwebui-chat.png" width="2556" alt="OpenWebUI Chat Interface">

---

## Prometheus

<img src="Screenshots/prometheus.png" width="2560" alt="Prometheus Metrics">

---

# Key Metrics

## HTTP Metrics

* Request Rate (RPS)
* Request Latency
* P99 Latency
* Active Requests
* Status Code Distribution
* Endpoint-Level Visibility

## Redis Metrics

* Connected Clients
* Used Memory
* Blocked Clients

## PostgreSQL Metrics

* Active Connections
* Idle Connections
* Total Connections

## System Metrics

* CPU Usage
* Memory Usage
* Process Uptime
* RSS Memory

---

# Impact

* Built a production-inspired observability platform for LLM applications.
* Improved visibility into request behavior and endpoint performance.
* Enabled monitoring of Redis and PostgreSQL dependencies.
* Reduced observability blind spots through custom instrumentation.
* Simplified performance analysis and debugging through Grafana dashboards.
* Implemented scalable metric collection using path normalization.
* Built an AI-powered observability assistant using LiteLLM and Llama 3.
* Automated operational health analysis from Prometheus metrics.
* Generated structured observability summaries using LLMs.

---

# Challenges Solved

* Endpoint metric cardinality explosion
* End-to-end LLM observability integration
* Real-time infrastructure monitoring
* Per-endpoint latency analysis
* Multi-component monitoring across OpenWebUI, Redis, PostgreSQL, and Langfuse

---

# Future Enhancements

* Automated incident report generation
* Root cause analysis using LLMs
* Anomaly detection and alert summarization
* Prometheus Alertmanager integration
* ClickHouse observability metrics
* MinIO monitoring
* SLO and SLA dashboards
* Automated dashboard provisioning

---

# Roadmap

## v1.0 (Completed)

* Custom Prometheus instrumentation
* Grafana dashboards
* Redis monitoring
* PostgreSQL monitoring
* Endpoint-level visibility
* P99 latency tracking


## v1.1 (Completed)

* AI-powered observability assistant
* LLM-based metric analysis
* Operational insight generation
* Automated health summaries
* /api/ai/summary endpoint


## v1.2 (Planned)

* Natural language observability queries
* Interactive observability assistant (/api/ai/ask)
* Endpoint performance analysis
* Endpoint latency investigation
* Traffic pattern analysis
* Redis health analysis
* PostgreSQL health analysis
* Query routing for observability questions
* Prometheus-backed AI responses
* Langfuse tracing for AI assistant interactions


## v1.3 (Future)

* Root cause analysis workflows
* Incident report generation
* Multi-step AI investigation
* Anomaly detection and summarization
* Alert intelligence
* Prometheus Alertmanager integration
* AI observability agent

---

# Learning Outcomes

This project strengthened practical experience in:

* LLM Infrastructure
* LLM Observability
* Prometheus Instrumentation
* Grafana Dashboard Design
* Middleware Development
* Performance Monitoring
* Telemetry Engineering
* Distributed Systems Debugging
* Production-Grade Monitoring Systems
* LLM Application Development
* Prompt Engineering
* AI-assisted Observability
* Retrieval-Augmented Operational Analysis
