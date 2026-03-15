"""
Simple in-memory cache for TramitUp backend.
In production, this should be replaced with Redis.
"""
import time
from typing import Any, Dict, Optional
from functools import wraps
import json
import hashlib


class SimpleCache:
    """Simple in-memory cache with TTL support."""
    
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if key not in self._cache:
            return None
        
        entry = self._cache[key]
        if entry["expires_at"] < time.time():
            del self._cache[key]
            return None
        
        return entry["value"]
    
    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        """Set value in cache with TTL in seconds."""
        self._cache[key] = {
            "value": value,
            "expires_at": time.time() + ttl,
        }
    
    def delete(self, key: str) -> None:
        """Delete key from cache."""
        self._cache.pop(key, None)
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self._cache.clear()
    
    def cleanup_expired(self) -> None:
        """Remove expired entries."""
        current_time = time.time()
        expired_keys = [
            key for key, entry in self._cache.items()
            if entry["expires_at"] < current_time
        ]
        for key in expired_keys:
            del self._cache[key]


# Global cache instance
_cache = SimpleCache()


def get_cache() -> SimpleCache:
    """Get the global cache instance."""
    return _cache


def cache_key(*args, **kwargs) -> str:
    """Generate a cache key from arguments."""
    # Create a deterministic string from args and kwargs
    key_data = {
        "args": args,
        "kwargs": sorted(kwargs.items()) if kwargs else {}
    }
    key_str = json.dumps(key_data, sort_keys=True, default=str)
    return hashlib.md5(key_str.encode()).hexdigest()


def cached(ttl: int = 300, key_prefix: str = ""):
    """Decorator to cache function results."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            key = f"{key_prefix}:{func.__name__}:{cache_key(*args, **kwargs)}"
            
            # Try to get from cache
            cached_result = _cache.get(key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            _cache.set(key, result, ttl)
            return result
        
        return wrapper
    return decorator


def cached_async(ttl: int = 300, key_prefix: str = ""):
    """Decorator to cache async function results."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            key = f"{key_prefix}:{func.__name__}:{cache_key(*args, **kwargs)}"
            
            # Try to get from cache
            cached_result = _cache.get(key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            _cache.set(key, result, ttl)
            return result
        
        return wrapper
    return decorator


def invalidate_cache_pattern(pattern: str) -> None:
    """Invalidate all cache keys matching a pattern."""
    keys_to_delete = [
        key for key in _cache._cache.keys()
        if pattern in key
    ]
    for key in keys_to_delete:
        _cache.delete(key)