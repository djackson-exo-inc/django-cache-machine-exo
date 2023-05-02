import logging
from django.core.cache import caches
from django.core.cache import cache as default_cache

log = logging.getLogger("caching.invalidation")


class CacheSelector:
    CURRENT_CACHE = None
    CURRENT_CACHE_PREFIX = None

    @classmethod
    def set_cache(cls, cache_name: str, cache_prefix: str) -> None:
        if cache_name in caches:
            cls.CURRENT_CACHE = caches[cache_name]
        else:
            log.warning(f"Invalid cache name: {cache_name}")
            if 'cache_machine' in caches:
                cls.CURRENT_CACHE = caches['cache_machine']
            else:
                cls.CURRENT_CACHE = default_cache
        cls.CURRENT_CACHE_PREFIX = cache_prefix

    @classmethod
    def get_cache(cls):
        if cls.CURRENT_CACHE is None:
            cls.set_cache("")
            return cls.CURRENT_CACHE

    @classmethod
    def get_cache_prefix(cls):
        return cls.CURRENT_CACHE_PREFIX
