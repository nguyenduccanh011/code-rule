from functools import wraps
import time
from typing import Any, Callable, Dict, Optional, TypeVar

T = TypeVar('T')

class Cache:
    """
    Simple in-memory cache implementation with TTL support
    """
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        
    def memoize(self, ttl: int = 3600):
        """
        Decorator to cache function results with TTL
        
        Args:
            ttl: Time to live in seconds (default: 1 hour)
        """
        def decorator(func: Callable[..., T]) -> Callable[..., T]:
            @wraps(func)
            def wrapper(*args, **kwargs) -> T:
                # Create a cache key from function name and arguments
                key_parts = [func.__name__]
                key_parts.extend([str(arg) for arg in args])
                key_parts.extend([f"{k}:{v}" for k, v in sorted(kwargs.items())])
                cache_key = ":".join(key_parts)
                
                # Check if result is in cache and not expired
                if cache_key in self._cache:
                    cache_entry = self._cache[cache_key]
                    if time.time() - cache_entry['timestamp'] < ttl:
                        return cache_entry['value']
                
                # Call function and cache result
                result = func(*args, **kwargs)
                self._cache[cache_key] = {
                    'value': result,
                    'timestamp': time.time()
                }
                
                return result
            return wrapper
        return decorator
    
    def clear(self, key: Optional[str] = None) -> None:
        """
        Clear cache entries
        
        Args:
            key: Optional key to clear specific entry
        """
        if key:
            if key in self._cache:
                del self._cache[key]
        else:
            self._cache.clear()

# Create a global cache instance
cache = Cache() 