from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_config_check_never_returns_secret_values():
    response = client.get("/config-check")
    assert response.status_code == 200
    assert set(response.json()) == {
        "ai_configured",
        "search_configured",
        "database_configured",
    }
