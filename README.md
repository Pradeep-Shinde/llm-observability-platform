# LLM Observability Platform

A production-inspired observability platform for LLM applications built using OpenWebUI, LiteLLM, Ollama, Langfuse, Prometheus, and Grafana.

The platform provides end-to-end monitoring, tracing, performance analysis, and infrastructure visibility for self-hosted LLM workloads. 
It extends OpenWebUI with custom Prometheus instrumentation and Grafana dashboards to improve operational visibility, debugging, and performance analysis.

<img src="Screenshots/grafana-dashboard-1.png" width="2560" alt="Grafana Dashboard">

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
                                 ▼
                     ┌──────────────────────────┐
                     │         LiteLLM          │
                     │        Port 4000         │
                     └───────────┬──────────────┘
                                 │
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
                                 ▼
                     ┌──────────────────────────┐
                     │         Grafana          │
                     │        Port 3001         │
                     └──────────────────────────┘
```

---

# Technology Stack

## LLM Layer

* OpenWebUI
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

# Screenshots

## Grafana Dashboard

<img src="Screenshots/grafana-dashboard-1.png" width="2560" alt="">

<img src="Screenshots/grafana-dashboard-2.png" width="2558" alt="">

<img src="Screenshots/grafana-dashboard-3.png" width="2560" alt="">

<img src="Screenshots/grafana-dashboard-4.png" width="2555" alt="">

---

## Langfuse Traces

<img src="Screenshots/langfuse-traces.png" width="2559" alt="">

---

## OpenWebUI

<img src="Screenshots/openwebui-chat.png" width="2556" alt="">

---

## Prometheus

<img src="Screenshots/prometheus.png" width="2560" alt="">

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

---

# Challenges Solved

* Endpoint metric cardinality explosion
* End-to-end LLM observability integration
* Real-time infrastructure monitoring
* Per-endpoint latency analysis
* Multi-component monitoring across OpenWebUI, Redis, PostgreSQL, and Langfuse

---

# Future Enhancements

* AI-powered observability assistant
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

## v1.0

* Custom Prometheus instrumentation
* Grafana dashboards
* Redis monitoring
* PostgreSQL monitoring
* Endpoint-level visibility
* P99 latency tracking

## v1.1 (Planned)

* AI-powered observability assistant
* LLM-based metric analysis
* Operational insight generation

## v1.2 (Future)

* Root cause analysis
* Incident summarization
* Anomaly detection
* Alert intelligence

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
