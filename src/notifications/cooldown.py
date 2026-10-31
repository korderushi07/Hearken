import time

_last_alerts = {}
COOLDOWN_SECONDS = 20


def should_alert(key: str) -> bool:
    now = time.monotonic()
    last_time = _last_alerts.get(key, 0)

    if now - last_time >= COOLDOWN_SECONDS:
        _last_alerts[key] = now
        return True

    return False

