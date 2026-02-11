import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_index_success(client):
    response = client.get("/")

    assert response.status_code == 200

    data = response.get_json()

    # Проверяем верхний уровень
    assert "service" in data
    assert "system" in data
    assert "runtime" in data
    assert "request" in data
    assert "endpoints" in data

    # Проверяем service
    assert data["service"]["name"] == "devops-info-service"
    assert data["service"]["framework"] == "Flask"

    # Проверяем system (НЕ значения, а наличие)
    assert "hostname" in data["system"]
    assert "cpu_count" in data["system"]

    # Проверяем runtime
    assert isinstance(data["runtime"]["uptime_seconds"], int)


def test_health_success(client):
    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert isinstance(data["uptime_seconds"], int)


def test_not_found(client):
    response = client.get("/does-not-exist")

    assert response.status_code == 404

    data = response.get_json()

    assert data["error"] == "Not Found"
    assert "/health" in data["available_endpoints"]
