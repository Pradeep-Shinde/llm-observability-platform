def build_context(question, intent, data):

    return f"""
User Question:
{question}

Question Type:
{intent}

Observability Data:
{data}

Rules:

- Use only supplied observability data.
- Be concise.
- If answering about a metric, include the metric value.
- If answering about endpoints, mention the endpoint names.
- Do not invent information.
- If insufficient data exists, say so.
"""