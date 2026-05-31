from .query_router import route_question
from .prometheus_tools import *
from .llm import ask_llm
from .context_builder import build_context


def answer_question(question):
    intent = route_question(question)

    if intent == "latency":
        data = get_slowest_endpoints()

    elif intent == "traffic":
        data = get_top_endpoints()

    elif intent == "cpu":
        data = get_cpu_usage()

    elif intent == "memory":
        data = get_memory_health()

    elif intent == "health":
        data = "\n".join([
            get_cpu_usage(),
            get_memory_usage(),
            get_memory_total(),
            get_rps(),
            get_error_rate()
        ])

    elif intent == "redis":
        data = get_redis_health()

    elif intent == "postgres":
        data = get_postgres_health()

    else:
        data = {}

    prompt = build_context(question, intent, data)
    answer = ask_llm(prompt)
    return intent, answer