"""
Pytest configuration and fixtures for TramitUp backend tests.
"""
import os
import pytest
from unittest.mock import Mock, AsyncMock
from fastapi.testclient import TestClient
from httpx import AsyncClient

# Set test environment
os.environ["ENVIRONMENT"] = "test"
os.environ["GOOGLE_API_KEY"] = "test-key"
os.environ["SUPABASE_URL"] = "https://test.supabase.co"
os.environ["SUPABASE_SERVICE_ROLE_KEY"] = "test-key"
os.environ["SUPABASE_JWT_SECRET"] = "test-secret"
os.environ["STRIPE_SECRET_KEY"] = "sk_test_123"
os.environ["STRIPE_WEBHOOK_SECRET"] = "whsec_test"
os.environ["RESEND_API_KEY"] = "re_test"
os.environ["FRONTEND_URL"] = "http://localhost:3000"

@pytest.fixture
def mock_supabase():
    """Mock Supabase client."""
    mock = Mock()
    mock.auth.get_user.return_value = {"id": "test-user-id", "email": "test@example.com"}
    mock.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value = {
        "data": {"id": "test-user-id", "plan": "free"},
        "error": None
    }
    return mock

@pytest.fixture
def mock_google_ai():
    """Mock Google AI client."""
    mock = Mock()
    mock.generate_content.return_value.text = "Test response"
    mock.embed_content.return_value.embedding = [0.1, 0.2, 0.3]
    return mock

@pytest.fixture
def test_user_id():
    """Test user ID."""
    return "test-user-123"

@pytest.fixture
def test_user_token():
    """Test JWT token."""
    import jwt
    from app.core.config import get_settings
    
    settings = get_settings()
    payload = {
        "sub": "test-user-123",
        "exp": 9999999999,
        "aud": "authenticated"
    }
    
    # Create a valid JWT token for testing
    token = jwt.encode(payload, settings.supabase_jwt_secret, algorithm="HS256")
    return token

@pytest.fixture
def auth_headers(test_user_token):
    """Authentication headers for requests."""
    return {"Authorization": f"Bearer {test_user_token}"}

@pytest.fixture
async def async_client():
    """Async HTTP client for testing."""
    from app.main import app
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
def client():
    """Sync HTTP client for testing."""
    from app.main import app
    return TestClient(app)

@pytest.fixture
def mock_chat_service():
    """Mock chat service."""
    mock = Mock()
    mock.run_chat.return_value = (
        "conv-123",
        {"category": "test", "subcategory": "test"},
        ["chunk1", "chunk2"]
    )
    mock.save_message = Mock()
    return mock

@pytest.fixture
def mock_rate_limit():
    """Mock rate limiting."""
    def mock_check_rate_limit(user_id, plan):
        return True, 2  # allowed, remaining
    
    def mock_consume_rate_limit(user_id, plan):
        pass
    
    return mock_check_rate_limit, mock_consume_rate_limit