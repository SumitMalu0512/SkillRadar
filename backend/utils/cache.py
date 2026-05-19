"""
Simple file based cache for API responses.
We use this to avoid hitting API rate limits during development
and to make demos fast (cached responses load instantly).

Note: in production we would use Redis, but for a college project
file based caching is simpler and works fine.
"""
import json
import os
import hashlib
from datetime import datetime, timedelta
from pathlib import Path


class FileCache:
    def __init__(self, cache_dir="./cache", ttl_hours=6):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)

    def _key_to_path(self, key):
        # hash the key so weird characters don't break filenames
        h = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{h}.json"

    def get(self, key):
        path = self._key_to_path(key)
        if not path.exists():
            return None

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            cached_at = datetime.fromisoformat(data["cached_at"])
            if datetime.now() - cached_at > self.ttl:
                # expired - clean it up
                path.unlink()
                return None

            return data["payload"]
        except (json.JSONDecodeError, KeyError, ValueError):
            # corrupted cache, just delete it
            path.unlink(missing_ok=True)
            return None

    def set(self, key, payload):
        path = self._key_to_path(key)
        data = {
            "cached_at": datetime.now().isoformat(),
            "key": key,
            "payload": payload,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def clear(self):
        """Clear all cached responses. Useful during development."""
        for f in self.cache_dir.glob("*.json"):
            f.unlink()
