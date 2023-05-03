import logging
from django.core.cache import caches
from django.core.cache.backends.base import BaseCache, DEFAULT_TIMEOUT
from django.core.cache import cache as default_cache

log = logging.getLogger("caching.invalidation")


class CacheSelector:
    CURRENT_CACHE = None

    @classmethod
    def set_cache(cls, cache_name: str) -> None:
        if cache_name in caches:
            cls.CURRENT_CACHE = caches[cache_name]
        else:
            log.warning(f"Invalid cache name: {cache_name}")
            if 'cache_machine' in caches:
                cls.CURRENT_CACHE = caches['cache_machine']
            else:
                cls.CURRENT_CACHE = default_cache

    @classmethod
    def get_cache(cls):
        if cls.CURRENT_CACHE is None:
            cls.set_cache("")
        return cls.CURRENT_CACHE


class CacheProxy(BaseCache):
    def __init__(self):
        pass

    @property
    def real_cache(self) -> BaseCache:
        return CacheSelector.get_cache()

    def get_backend_timeout(self, timeout=DEFAULT_TIMEOUT):
        return self.real_cache.get_backend_timeout(timeout)

    def make_key(self, key, version=None):
        return self.real_cache.make_key(key, version)

    def add(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        return self.real_cache.add(key, value, timeout, version)

    def get(self, key, default=None, version=None):
        return self.real_cache.get(key, default, version)

    def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        return self.real_cache.set(key, value, timeout, version)

    def touch(self, key, timeout=DEFAULT_TIMEOUT, version=None):
        return self.real_cache.touch(key, timeout, version)

    def delete(self, key, version=None):
        return self.real_cache.delete(key, version)

    def get_many(self, keys, version=None):
        return self.real_cache.get_many(keys, version)

    def get_or_set(self, key, default, timeout=DEFAULT_TIMEOUT, version=None):
        return self.real_cache.get_or_set(key, default, timeout, version)

    def has_key(self, key, version=None):
        return self.real_cache.has_key(key, version)

    def incr(self, key, delta=1, version=None):
        return self.real_cache.incr(key, delta, version)

    def decr(self, key, delta=1, version=None):
        return self.real_cache.decr(key, delta, version)

    def __contains__(self, key):
        return self.real_cache.__contains__(key)

    def set_many(self, data, timeout=DEFAULT_TIMEOUT, version=None):
        return self.real_cache.set_many(data, timeout, version)

    def delete_many(self, keys, version=None):
        return self.real_cache.delete_many(keys, version)

    def clear(self):
        return self.real_cache.clear()

    def validate_key(self, key):
        return self.real_cache.validate_key()

    def incr_version(self, key, delta=1, version=None):
        return self.real_cache.incr(key, delta, version)

    def decr_version(self, key, delta=1, version=None):
        return self.real_cache.decr_version(key, delta, version)

    def close(self, **kwargs):
        return self.real_cache.close(**kwargs)
