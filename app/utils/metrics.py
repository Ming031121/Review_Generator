metrics = {
    "request_count": 0,
    "success_count": 0,
    "failure_count": 0,
    "retrieval_failure_count": 0,
    "total_latency_ms": 0.0
}

def record_request():
    metrics["request_count"] += 1

def record_success(latency_ms):
    metrics["success_count"] += 1
    metrics["total_latency_ms"] += latency_ms

def record_failure():
    metrics["failure_count"] += 1

def record_retrieval_failure():
    metrics["retrieval_failure_count"] += 1

def get_success_count():
    return metrics["success_count"]

def get_failure_count():
    return metrics["failure_count"]

def get_retrieval_failure_count():
    return metrics["retrieval_failure_count"]

def get_total_latency_ms():
    return metrics["total_latency_ms"]

def get_avg_latency_ms():
    return metrics["total_latency_ms"] / metrics["success_count"]

def get_metrics():
    avg_latency = 0.0
    if metrics["success_count"] > 0:
        avg_latency = metrics["total_latency_ms"] / metrics["success_count"]

    return {
        "request_count": metrics["request_count"],
        "success_count": metrics["success_count"],
        "failure_count": metrics["failure_count"],
        "retrieval_failure_count": metrics["retrieval_failure_count"],
        "avg_latency_ms": round(avg_latency, 2)
    }