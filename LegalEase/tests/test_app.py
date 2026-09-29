from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_empty_input_rejected():
    response = client.post("/qa", json={"text": ""})
    assert response.status_code == 422


def test_unknown_route():
    response = client.get("/does-not-exist")
    assert response.status_code == 404
