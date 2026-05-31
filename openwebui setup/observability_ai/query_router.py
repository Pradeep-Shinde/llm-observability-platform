def route_question(question):
    q = question.lower()

    if any(word in q for word in ["slow", "slowest", "latency", "performance"]):
        return "latency"

    if any(word in q for word in ["traffic", "requests", "rps"]):
        return "traffic"

    if "redis" in q:
        return "redis"

    if "postgres" in q:
        return "postgres"

    if any(word in q for word in ["cpu", "processor"]):
        return "cpu"

    if "memory" in q:
        return "memory"

    if "health" in q:
        return "health"

    if any(word in q for word in ["postgres", "postgresql", "database", "db"]):
        return "postgres"

    return "summary"