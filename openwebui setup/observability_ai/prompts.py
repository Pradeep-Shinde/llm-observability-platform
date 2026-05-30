def build_summary_prompt(metrics):

    return f"""
You are a senior Site Reliability Engineer.

Analyze the following OpenWebUI metrics.

CPU Usage:
{metrics["cpu"]} %

Memory Usage:
{metrics["memory_mb"]} MB

Requests Per Second:
{metrics["rps"]}

P99 Latency:
{metrics["p99_latency"]} seconds

5xx Error Rate:
{metrics["error_rate"]}

Rules:

- Only use supplied metrics.
- Do not invent root causes.
- Do not infer causes from correlation alone.
- Do not recommend infrastructure changes unless directly supported by metrics.
- If insufficient information exists, say:
  "Insufficient data to determine root cause."

Provide:

1. Health Status
2. Observations
3. Risks Visible From Metrics
4. Additional Data Needed

Keep the response under 150 words.
"""