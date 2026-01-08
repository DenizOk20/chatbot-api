import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def chat_valid_message():
    response = client.post("/chat", json={"message": ""})
    assert response.status_code == 422  # validation error for empty message

def test_chat_too_long_message():
    long_message = "a" * 1001
    response = client.post(
        "/chat",
        json={"message": long_message}
    )
    assert response.status_code == 422  # validation error for too long message

def test_rate_limiting():
    from main import check_rate_limit
    
    test_ip = "127.0.0.1"
    
    from main import rate_limit_store
    rate_limit_store.clear()
    
    for i in range(10):
        assert check_rate_limit(test_ip) == True
    
    assert check_rate_limit(test_ip) == False
    responses = []
    for _ in range(11):
        response = client.post(
            "/chat",
            json={"message": "hello"}
        )
        responses.append(response.status_code)
    
    assert 429 in responses