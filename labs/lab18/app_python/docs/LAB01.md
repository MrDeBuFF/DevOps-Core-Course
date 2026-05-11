# Lab 1: DevOps Info Service - Report

## Framework Selection

Choice – Flask

### Framework Comparison:

| Criterion | Flask | FastAPI | Django |
|-----------|-------|---------|--------|
| **Learning Curve** | Low | Medium | High |
| **Performance** | High | Very High | Medium |
| **Built-in Features** | Minimal | Modern API features | Full-stack |
| **Auto-documentation** | Manual | OpenAPI/Swagger | Manual |
| **Async Support** | Limited | Native | Limited |
| **Project Size** | ~150KB | ~1.2MB | ~8MB+ |
| **Use Case** | Microservices, APIs | Modern APIs, Microservices | Monoliths, CMS |

**Decision Justification:** For Lab 1's requirements (simple info service with 2 endpoints), Flask provides the perfect balance of simplicity, control, and maintainability. It allows us to focus on the DevOps aspects rather than framework intricacies.

## Implemented Best Practices

### 1. Clean Code Organization

**Code Example:**
```python
def get_system_info():
    """Collect system information."""
    return {
        "hostname": socket.gethostname(),
        "platform": platform.system(),
        # ... other fields
    }

@app.route("/")
def index():
    """Main endpoint - service and system information."""
    # Clear request handling logic
```

Benefits:
- Clear separation of concerns with dedicated functions for better understanding
- Logical grouping of imports
- Comprehensive docstrings for all functions and endpoints
- Consistent naming conventions (PEP 8 compliant)



### 2. Comprehensive Error Handling

Implemented error handlers for common HTTP status codes:

```python
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    logger.warning(f"Not found: {request.method} {request.path}")
    return (
        jsonify({
            "error": "Not Found",
            "message": "The requested endpoint does not exist",
            "available_endpoints": ["/", "/health"],
        }),
        404,
    )

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return (
        jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
        }),
        500,
    )
```

Benefits:

- Consistent error responses
- Helpful error messages for API consumers
- Proper logging of all errors

### 3. Structured Logging

Configured logging with appropriate levels and format:

```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
```

Benefits:

- Timestamps help debug timing issues
- Different levels for filtering
- Production monitoring systems read these logs


### 4. Environment-Based Configuration

All configuration externalized to environment variables:

```python
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5000))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
```

Benefits:

- No hardcoded values in source code
- Easy configuration for different environments
- Secure handling of sensitive data (for future features)
- Twelve-factor app compliance

### 5. Type Consistency and ISO 8601 Formatting

```python
# Consistent time formatting in UTC
datetime.now(timezone.utc).isoformat().replace("+00:00", "") + "Z"

# Human-readable uptime formatting
f"{hours} hour, {minutes} minutes"
```

Benefits:

- Consistent time formatting
- Human-readable uptime formatting

## API Documentation

### Endpoint 1: GET /

Purpose: Retrieve comprehensive service and system information.

Response Structure:

```json
{
  "service": {
    "name": "devops-info-service",
    "version": "1.0.0",
    "description": "DevOps course info service",
    "framework": "Flask"
  },
  "system": {
    "hostname": "ubuntu-server",
    "platform": "Linux",
    "platform_version": "Linux-6.8.0-31-generic-x86_64-with-glibc2.39",
    "architecture": "x86_64",
    "cpu_count": 8,
    "python_version": "3.12.3"
  },
  "runtime": {
    "uptime_seconds": 120,
    "uptime_human": "0 hour, 2 minutes",
    "current_time": "2024-10-15T10:30:45.123456Z",
    "timezone": "UTC"
  },
  "request": {
    "client_ip": "127.0.0.1",
    "user_agent": "curl/7.81.0",
    "method": "GET",
    "path": "/"
  },
  "endpoints": [
    {"path": "/", "method": "GET", "description": "Service information"},
    {"path": "/health", "method": "GET", "description": "Health check"}
  ]
}
```

### Endpoint 2: GET /health

Purpose: Health check for monitoring and Kubernetes probes.

Response Structure:

```json
{
  "status": "healthy",
  "timestamp": "2024-10-15T10:30:45.123456Z",
  "uptime_seconds": 120
}
```

### Testing Commands:

```bash
# Get service information
curl http://localhost:6000/

# Health check
curl http://localhost:6000/health

# Formatted JSON output
curl http://localhost:6000/ | python3 -m json.tool
```

## Testing Evidence


See the screenshots directory `app_python/docs/screenshots/` for visual proof:

- 01-main-endpoint.png - Complete JSON response from GET /
- 02-health-check.png - Health check endpoint response
- 03-formatted-output.png - Pretty-printed JSON output
Terminal Output Examples:

```bash
$ curl http://localhost:6000/ | python3 -m json.tool

{
    "endpoints": [
        {
            "description": "Service information",
            "method": "GET",
            "path": "/"
        },
        {
            "description": "Health check",
            "method": "GET",
            "path": "/health"
        }
    ],
    "request": {
        "client_ip": "127.0.0.1",
        "method": "GET",
        "path": "/",
        "user_agent": "curl/8.7.1"
    },
    "runtime": {
        "current_time": "2026-01-27T16:58:50.775183Z",
        "timezone": "UTC",
        "uptime_human": "0 hour, 0 minutes",
        "uptime_seconds": 4
    },
    "service": {
        "description": "DevOps course info service",
        "framework": "Flask",
        "name": "devops-info-service",
        "version": "1.0.0"
    },
    "system": {
        "architecture": "arm64",
        "cpu_count": 8,
        "hostname": "MacBook-Air-Mr-DeBuFF.local",
        "platform": "Darwin",
        "platform_version": "macOS-26.2-arm64-arm-64bit-Mach-O",
        "python_version": "3.13.2"
    }
}
```

## Challenges and Solutions

### Challenge 1: Accurate Uptime Calculation

Problem: Needed to calculate application uptime in both seconds and human-readable format.

Solution: Created a dedicated function that calculates the difference between current time and application start time:

```python
def get_uptime():
    """Calculate application uptime."""
    uptime = (datetime.now(timezone.utc) - START_TIME).total_seconds()
    hours = int(uptime // 3600)
    minutes = int((uptime % 3600) // 60)
    return {"seconds": int(uptime), "human": f"{hours} hour, {minutes} minutes"}
```

## GitHub Community

1. **The Value of Starring Repositories in Open Source:**

They act as quality signals that help developers discover reliable and well-maintained projects. When you star a repository, you're not just bookmarking it for personal reference—you're contributing to its visibility and credibility. 

2. **The Importance of Following Developers in Team Projects:**

By following professors and TAs, you gain insights into professional development practices and stay updated on industry trends. Following classmates fosters collaboration and peer learning, allowing you to see different approaches to problem-solving and stay connected on course projects.
