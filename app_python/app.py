"""
DevOps Info Service
Main application module
"""

import os
import socket
import platform
import logging
import time
from datetime import datetime, timezone

from flask import Flask, jsonify, request, g

from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST
)

from threading import Lock

DATA_DIR = "/data"
VISITS_FILE = os.path.join(DATA_DIR, "visits")

lock = Lock()

app = Flask(__name__)

# Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 6000))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Application start time
START_TIME = datetime.now(timezone.utc)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Prometheus Metrics
http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration seconds",
    ["method", "endpoint"]
)

http_requests_in_progress = Gauge(
    "http_requests_in_progress",
    "HTTP requests currently being processed"
)

endpoint_calls = Counter(
    "devops_info_endpoint_calls",
    "Endpoint calls",
    ["endpoint"]
)

system_info_duration = Histogram(
    "devops_info_system_collection_seconds",
    "System info collection time"
)


# Request instrumentation
@app.before_request
def before_request():
    g.start_time = time.time()
    http_requests_in_progress.inc()


@app.after_request
def after_request(response):
    duration = time.time() - g.start_time

    endpoint = request.path

    http_requests_total.labels(
        method=request.method,
        endpoint=endpoint,
        status=response.status_code
    ).inc()

    http_request_duration_seconds.labels(
        method=request.method,
        endpoint=endpoint
    ).observe(duration)

    http_requests_in_progress.dec()

    return response


# Helper functions
def get_system_info():
    """Collect system information."""

    start = time.time()

    info = {
        "hostname": socket.gethostname(),
        "platform": platform.system(),
        "platform_version": platform.platform(),
        "architecture": platform.machine(),
        "cpu_count": os.cpu_count(),
        "python_version": platform.python_version(),
    }

    system_info_duration.observe(time.time() - start)

    return info


def get_uptime():
    """Calculate application uptime."""
    uptime = (datetime.now(timezone.utc) - START_TIME).total_seconds()
    hours = int(uptime // 3600)
    minutes = int((uptime % 3600) // 60)

    return {
        "seconds": int(uptime),
        "human": f"{hours} hour, {minutes} minutes"
    }


def get_request_info():
    """Collect request information."""

    return {
        "client_ip": request.remote_addr,
        "user_agent": request.headers.get("User-Agent", "Unknown"),
        "method": request.method,
        "path": request.path,
    }


def read_visits():
    try:
        with open(VISITS_FILE, "r") as f:
            return int(f.read())
    except Exception:
        return 0


def write_visits(count):
    with open(VISITS_FILE, "w") as f:
        f.write(str(count))


def increment_visits():
    with lock:
        count = read_visits()
        count += 1
        write_visits(count)
        return count


# Routes
@app.route("/")
def index():
    endpoint_calls.labels(endpoint="/").inc()

    uptime = get_uptime()

    visits = increment_visits()

    response = {
        "service": {
            "name": "devops-info-service",
            "version": "1.0.0",
            "description": "DevOps course info service",
            "framework": "Flask",
        },
        "system": get_system_info(),
        "runtime": {
            "uptime_seconds": uptime["seconds"],
            "uptime_human": uptime["human"],
            "current_time": datetime.now(
                timezone.utc).isoformat().replace("+00:00", "")
            + "Z",
            "timezone": "UTC",
        },
        "request": get_request_info(),
        "endpoints": [
            {"path": "/", "method": "GET",
             "description": "Service information"},
            {"path": "/health", "method": "GET",
             "description": "Health check"},
            {"path": "/metrics", "method": "GET",
             "description": "Prometheus metrics"},
        ],
        "visits": visits,
    }

    logger.info(f"Request: {request.method} {request.path}")

    return jsonify(response), 200


@app.route("/health")
def health():
    endpoint_calls.labels(endpoint="/health").inc()

    uptime = get_uptime()

    response = {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00",
                                                                    "") + "Z",
        "uptime_seconds": uptime["seconds"],
    }

    logger.debug(f'Health check: {response["status"]}')

    return jsonify(response), 200


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


@app.route("/visits")
def visits():
    count = read_visits()
    return jsonify({"visits": count}), 200

# Errors


@app.errorhandler(404)
def not_found(error):

    logger.warning(f"Not found: {request.method} {request.path}")

    return (
        jsonify(
            {
                "error": "Not Found",
                "message": "The requested endpoint does not exist",
                "available_endpoints": ["/", "/health", "/metrics"],
            }
        ),
        404,
    )


@app.errorhandler(500)
def internal_error(error):

    logger.error(f"Internal server error: {str(error)}")

    return (
        jsonify(
            {
                "error": "Internal Server Error",
                "message": "An unexpected error occurred",
            }
        ),
        500,
    )


if __name__ == "__main__":
    logger.info("Starting DevOps Info Service v1.0.0")
    logger.info(f"Server running at http://{HOST}:{PORT}")

    app.run(host=HOST, port=PORT, debug=DEBUG)
