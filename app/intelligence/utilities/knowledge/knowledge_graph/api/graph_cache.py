"""
Enterprise Graph Cache

Enterprise Version

Provides lightweight in-memory caching for graph queries.

Responsibilities
----------------
• Cache query results
• Retrieve cached results
• Invalidate individual keys
• Clear cache
• Track cache statistics
• Keep caching separate from KnowledgeGraph
"""


class GraphCache:

    # ==========================================================
    # INITIALIZATION
    # ==========================================================

    def __init__(self):

        self._cache = {}

        self._hits = 0

        self._misses = 0

    # ==========================================================
    # GET
    # ==========================================================

    def get(
        self,
        key,
        default=None,
    ):

        if key in self._cache:

            self._hits += 1

            return self._cache[key]

        self._misses += 1

        return default

    # ==========================================================
    # SET
    # ==========================================================

    def set(
        self,
        key,
        value,
    ):

        self._cache[key] = value

        return value

    # ==========================================================
    # EXISTS
    # ==========================================================

    def contains(self, key):

        return key in self._cache

    # ==========================================================
    # ALIAS
    # ==========================================================

    def has(self, key):

        return self.contains(key)

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete(self, key):

        if key in self._cache:

            del self._cache[key]

            return True

        return False

    # ==========================================================
    # INVALIDATE
    # ==========================================================

    def invalidate(self, key):

        return self.delete(key)

    # ==========================================================
    # CLEAR
    # ==========================================================

    def clear(self):

        self._cache.clear()

        self._hits = 0

        self._misses = 0

    # ==========================================================
    # SIZE
    # ==========================================================

    def size(self):

        return len(
            self._cache
        )

    # ==========================================================
    # STATISTICS
    # ==========================================================

    def statistics(self):

        total = (
            self._hits
            + self._misses
        )

        hit_rate = (
            self._hits / total
            if total
            else 0.0
        )

        return {
            "size": self.size(),
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": hit_rate,
        }

    # ==========================================================
    # KEYS
    # ==========================================================

    def keys(self):

        return list(
            self._cache.keys()
        )