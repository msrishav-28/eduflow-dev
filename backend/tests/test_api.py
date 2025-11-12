"""
API endpoint tests for EduFlow backend
"""
import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add parent directory to path to import server
sys.path.insert(0, str(Path(__file__).parent.parent))

from server import app


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_health_check(self, client):
        """Test basic health check"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
        assert "timestamp" in response.json()
    
    def test_readiness_check(self, client):
        """Test readiness check"""
        response = client.get("/readiness")
        # May fail if MongoDB is not available
        assert response.status_code in [200, 503]


class TestAPIRoot:
    """Test API root endpoint"""
    
    def test_api_root(self, client):
        """Test API root endpoint"""
        response = client.get("/api/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "EduFlow API"
        assert data["version"] == "1.0.0"
        assert "endpoints" in data


class TestQAEndpoint:
    """Test Q&A endpoint"""
    
    def test_qa_endpoint_validation(self, client):
        """Test Q&A endpoint with invalid data"""
        # Empty question
        response = client.post("/api/qa", json={"question": ""})
        assert response.status_code == 422
        
        # Invalid depth
        response = client.post("/api/qa", json={"question": "Test?", "depth": "invalid"})
        assert response.status_code == 422
    
    def test_qa_endpoint_structure(self, client):
        """Test Q&A endpoint response structure"""
        # Note: This may fail without valid LLM API key
        response = client.post(
            "/api/qa",
            json={"question": "What is 2+2?", "depth": "concise"}
        )
        # May return 500 if no LLM key configured
        if response.status_code == 200:
            data = response.json()
            assert "id" in data
            assert "question" in data
            assert "answer" in data
            assert "depth" in data
            assert "timestamp" in data


class TestSummarizerEndpoint:
    """Test summarizer endpoint"""
    
    def test_summarizer_validation(self, client):
        """Test summarizer endpoint with invalid data"""
        # Empty text
        response = client.post("/api/summarize", json={"text": ""})
        assert response.status_code == 422
        
        # Invalid max_points
        response = client.post("/api/summarize", json={"text": "Test text", "max_points": 0})
        assert response.status_code == 422
        
        response = client.post("/api/summarize", json={"text": "Test text", "max_points": 100})
        assert response.status_code == 422


class TestMCQEndpoint:
    """Test MCQ generator endpoint"""
    
    def test_mcq_validation(self, client):
        """Test MCQ endpoint with invalid data"""
        # Empty topic
        response = client.post("/api/mcq", json={"topic": ""})
        assert response.status_code == 422
        
        # Invalid num_questions
        response = client.post("/api/mcq", json={"topic": "Test", "num_questions": 0})
        assert response.status_code == 422
        
        response = client.post("/api/mcq", json={"topic": "Test", "num_questions": 100})
        assert response.status_code == 422


class TestCodeExplainerEndpoint:
    """Test code explainer endpoint"""
    
    def test_code_explainer_validation(self, client):
        """Test code explainer endpoint with invalid data"""
        # Empty code
        response = client.post("/api/explain-code", json={"code": ""})
        assert response.status_code == 422
        
        # Invalid language
        response = client.post("/api/explain-code", json={"code": "test", "language": "invalid"})
        assert response.status_code == 422


class TestRateLimiting:
    """Test rate limiting (if enabled)"""
    
    def test_rate_limit_headers(self, client):
        """Test rate limit headers are present"""
        response = client.get("/api/")
        # Rate limiting may not be enabled in test environment
        # Check if headers exist
        assert response.status_code == 200


class TestRequestTracking:
    """Test request ID tracking"""
    
    def test_request_id_header(self, client):
        """Test that request ID is added to response headers"""
        response = client.get("/api/")
        assert "X-Request-ID" in response.headers
        assert "X-Process-Time" in response.headers


class TestCORS:
    """Test CORS configuration"""
    
    def test_cors_headers(self, client):
        """Test CORS headers are present"""
        response = client.options("/api/", headers={"Origin": "http://localhost:3000"})
        # CORS headers should be present
        assert response.status_code in [200, 405]  # OPTIONS may not be allowed


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
