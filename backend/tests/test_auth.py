"""
Tests for authentication functionality.
"""
import pytest
from unittest.mock import patch, Mock
from fastapi import HTTPException
from app.core.auth import require_auth, _verify_jwt


class TestAuth:
    """Test authentication functions."""

    def test_verify_jwt_valid(self):
        """Test JWT token verification with valid token."""
        # Mock JWT payload
        mock_payload = {"sub": "user-123", "exp": 9999999999}
        
        with patch("app.core.auth.jwt.decode") as mock_decode:
            mock_decode.return_value = mock_payload
            
            payload = _verify_jwt("valid-token")
            assert payload["sub"] == "user-123"
            mock_decode.assert_called_once()

    def test_verify_jwt_invalid(self):
        """Test JWT token verification with invalid token."""
        import jwt as pyjwt
        
        with patch("app.core.auth.jwt.decode") as mock_decode:
            mock_decode.side_effect = pyjwt.PyJWTError("Invalid token")
            
            payload = _verify_jwt("invalid-token")
            assert payload is None

    def test_verify_jwt_expired(self):
        """Test JWT token verification with expired token."""
        import jwt as pyjwt
        
        with patch("app.core.auth.jwt.decode") as mock_decode:
            mock_decode.side_effect = pyjwt.PyJWTError("Token expired")
            
            payload = _verify_jwt("expired-token")
            assert payload is None

    @pytest.mark.asyncio
    async def test_require_auth_valid_token(self):
        """Test require_auth dependency with valid token."""
        from fastapi.security import HTTPAuthorizationCredentials
        
        mock_credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="valid-token"
        )
        
        with patch("app.core.auth._verify_jwt") as mock_verify:
            mock_verify.return_value = {"sub": "user-123"}
            
            user_id = await require_auth(mock_credentials)
            assert user_id == "user-123"

    @pytest.mark.asyncio
    async def test_require_auth_no_token(self):
        """Test require_auth dependency without token."""
        with pytest.raises(HTTPException) as exc_info:
            await require_auth(None)
        
        assert exc_info.value.status_code == 401
        assert "No autorizado" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_require_auth_invalid_token(self):
        """Test require_auth dependency with invalid token."""
        from fastapi.security import HTTPAuthorizationCredentials
        
        mock_credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="invalid-token"
        )
        
        with patch("app.core.auth._verify_jwt") as mock_verify:
            mock_verify.return_value = None  # Invalid token
            
            with pytest.raises(HTTPException) as exc_info:
                await require_auth(mock_credentials)
            
            assert exc_info.value.status_code == 401