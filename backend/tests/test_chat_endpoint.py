"""
Tests for chat endpoint functionality.
"""
import pytest
import json
from unittest.mock import patch, Mock, AsyncMock
from fastapi.testclient import TestClient
from fastapi.security import HTTPAuthorizationCredentials


class TestChatEndpoint:
    """Test chat endpoint."""

    @pytest.mark.asyncio
    async def test_chat_endpoint_success(self, client, auth_headers):
        """Test successful chat request."""
        with patch("app.core.auth.require_auth") as mock_auth, \
             patch("app.api.v1.endpoints.chat.generate_sse") as mock_generate:
            
            # Mock authentication to return test user ID
            mock_auth.return_value = "test-user-123"
            
            # Mock SSE generator
            async def mock_sse_generator(user_id, request):
                yield {"data": json.dumps([{"type": "conversation_id", "id": "conv-123"}])}
                yield {"data": json.dumps([{"type": "classification", "category": "test", "subcategory": "test"}])}
                yield {"data": json.dumps([{"type": "chunk", "content": "Hello"}])}
                yield {"data": json.dumps([{"type": "chunk", "content": " World"}])}
            
            mock_generate.return_value = mock_sse_generator("test-user-123", Mock())
            
            response = client.post(
                "/api/v1/chat",
                json={"message": "Hello", "conversation_id": None},
                headers=auth_headers
            )
            
            assert response.status_code == 200
            assert response.headers["content-type"] == "text/event-stream; charset=utf-8"

    def test_chat_endpoint_unauthorized(self, client):
        """Test chat request without authentication."""
        response = client.post(
            "/api/v1/chat",
            json={"message": "Hello", "conversation_id": None}
        )
        
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_chat_rate_limit_exceeded(self, client, auth_headers):
        """Test chat request when rate limit is exceeded."""
        with patch("app.core.auth.require_auth") as mock_auth, \
             patch("app.api.v1.endpoints.chat.generate_sse") as mock_generate:
            
            # Mock authentication to return test user ID
            mock_auth.return_value = "test-user-123"
            
            # Mock rate limit exceeded
            async def mock_sse_generator(user_id, request):
                yield {"data": json.dumps([{"type": "error", "message": "Has usado tus 2 consultas gratuitas de hoy."}])}
            
            mock_generate.return_value = mock_sse_generator("test-user-123", Mock())
            
            response = client.post(
                "/api/v1/chat",
                json={"message": "Hello", "conversation_id": None},
                headers=auth_headers
            )
            
            assert response.status_code == 200
            # Should still return 200 but with error in SSE stream

    def test_chat_endpoint_invalid_payload(self, client, auth_headers):
        """Test chat request with invalid payload."""
        with patch("app.core.auth.require_auth") as mock_auth:
            # Mock authentication to return test user ID
            mock_auth.return_value = "test-user-123"
            
            response = client.post(
                "/api/v1/chat",
                json={"invalid": "payload"},
                headers=auth_headers
            )
            
            assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_generate_sse_success(self):
        """Test SSE generation with successful flow."""
        from app.api.v1.endpoints.chat import generate_sse
        from app.schemas.chat import ChatRequest
        
        request = ChatRequest(message="Hello", conversation_id=None)
        
        with patch("app.api.v1.endpoints.chat.check_rate_limit") as mock_check, \
             patch("app.api.v1.endpoints.chat.get_user_plan") as mock_plan, \
             patch("app.api.v1.endpoints.chat.run_chat") as mock_run_chat, \
             patch("app.api.v1.endpoints.chat.consume_rate_limit") as mock_consume, \
             patch("app.api.v1.endpoints.chat.save_message") as mock_save:
            
            # Setup mocks
            mock_check.return_value = (True, 2)  # allowed, remaining
            mock_plan.return_value = "free"
            mock_run_chat.return_value = (
                "conv-123",
                {"category": "test", "subcategory": "test"},
                ["chunk1", "chunk2"]
            )
            
            # Collect SSE events
            events = []
            async for event in generate_sse("test-user", request):
                events.append(event)
            
            # Verify events
            assert len(events) >= 4  # conversation_id, classification, 2 chunks
            
            # Verify rate limit was consumed after success
            mock_consume.assert_called_once()
            mock_save.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_sse_rate_limit_exceeded(self):
        """Test SSE generation when rate limit is exceeded."""
        from app.api.v1.endpoints.chat import generate_sse
        from app.schemas.chat import ChatRequest
        
        request = ChatRequest(message="Hello", conversation_id=None)
        
        with patch("app.api.v1.endpoints.chat.check_rate_limit") as mock_check, \
             patch("app.api.v1.endpoints.chat.get_user_plan") as mock_plan:
            
            # Setup mocks for rate limit exceeded
            mock_check.return_value = (False, 0)  # not allowed, 0 remaining
            mock_plan.return_value = "free"
            
            # Collect SSE events
            events = []
            async for event in generate_sse("test-user", request):
                events.append(event)
            
            # Should only have error event
            assert len(events) == 1
            event_data = json.loads(events[0]["data"])
            assert event_data[0]["type"] == "error"
            assert "consultas gratuitas" in event_data[0]["message"]

    @pytest.mark.asyncio
    async def test_generate_sse_processing_error(self):
        """Test SSE generation when processing fails."""
        from app.api.v1.endpoints.chat import generate_sse
        from app.schemas.chat import ChatRequest
        
        request = ChatRequest(message="Hello", conversation_id=None)
        
        with patch("app.api.v1.endpoints.chat.check_rate_limit") as mock_check, \
             patch("app.api.v1.endpoints.chat.get_user_plan") as mock_plan, \
             patch("app.api.v1.endpoints.chat.run_chat") as mock_run_chat, \
             patch("app.api.v1.endpoints.chat.consume_rate_limit") as mock_consume:
            
            # Setup mocks
            mock_check.return_value = (True, 2)
            mock_plan.return_value = "free"
            
            # Mock run_chat to return valid data but make the stream fail
            def failing_stream():
                yield "chunk1"
                raise Exception("Stream processing failed")
            
            mock_run_chat.return_value = (
                "conv-123",
                {"category": "test", "subcategory": "test"},
                failing_stream()
            )
            
            # Collect SSE events
            events = []
            async for event in generate_sse("test-user", request):
                events.append(event)
            
            # Should have conversation_id, classification, chunk1, and error events
            assert len(events) >= 3
            
            # Check that we have an error event
            error_events = []
            for event in events:
                event_data = json.loads(event["data"])
                if isinstance(event_data, list) and len(event_data) > 0:
                    if event_data[0].get("type") == "error":
                        error_events.append(event)
            
            assert len(error_events) > 0
            assert "Error procesando respuesta" in json.loads(error_events[0]["data"])[0]["message"]
            
            # Rate limit should not be consumed on failure
            mock_consume.assert_not_called()