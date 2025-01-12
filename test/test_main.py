import pytest
from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)

def test_search_and_summarize_baidu():
    response = client.post("/search_and_summarize/", json={"engine": "baidu", "keyword": "测试", "max_results": 5})
    assert response.status_code == 200
    assert "summary" in response.json()

def test_search_and_summarize_bing():
    response = client.post("/search_and_summarize/", json={"engine": "bing", "keyword": "测试", "max_results": 5})
    assert response.status_code == 200
    assert "summary" in response.json()

def test_search_and_summarize_sogou():
    response = client.post("/search_and_summarize/", json={"engine": "sogou", "keyword": "测试", "max_results": 5})
    assert response.status_code == 200
    assert "summary" in response.json()

def test_search_and_summarize_wechat():
    response = client.post("/search_and_summarize/", json={"engine": "wechat", "keyword": "测试", "max_results": 5})
    assert response.status_code == 200
    assert "summary" in response.json()
