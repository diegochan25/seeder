from datetime import datetime, timezone

def utcnow() -> datetime:
    return datetime.now(timezone.utc)

class ReadonlyKVP[K, V]:
    _key: K
    _value: V

    def __init__(self, key: K, value: V):
        self._key = key
        self._value = value

    def key(self) -> K:
        return self._key

    def value(self) -> V:
        return self._value