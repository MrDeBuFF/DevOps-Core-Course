# DevOps Info Service

A lightweight web service built with Flask that provides detailed system information and health status monitoring.

## 📋 Overview

DevOps Info Service is a Python-based web application that exposes two main endpoints:
- **GET /** - Comprehensive service and system information
- **GET /health** - Health check endpoint for monitoring and probes

The service is designed to be configurable, production-ready, and follows Python best practices.

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone ...
cd app_python
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:
- Linux/Mac:

```bash
source venv/bin/activate
```
- Windows:

```bash
venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

- **Default Configuration:**


```bash
python app.py
```
The service will start at: http://0.0.0.0:6000

- **Custom Configuration:**


```bash
# Change port
PORT=8080 python app.py

# Change host and port
HOST=127.0.0.1 PORT=3000 python app.py

# Enable debug mode
DEBUG=true python app.py
```

## 🌐 API Endpoints

### GET /

Returns comprehensive service and system information.

**Request:**


```bash
curl http://localhost:6000/
```

### GET /health

Health check endpoint for monitoring systems and Kubernetes probes.

**Request:**

```bash
curl http://localhost:6000/health
```

**Status Codes:**

- 200 OK: Service is healthy
- 5xx: Service is unhealthy (implemented in future labs)

### ⚙️ Configuration

The application is configured through environment variables:

|Variable | Default | Description |
|----------|-------|---------|
|HOST | 0.0.0.0 | Host interface to bind the server|
|PORT | 6000 | Port number to listen on|
|DEBUG | false | Debug mode (true/false)|