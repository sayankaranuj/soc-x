"""Collect a small, JSON-serializable snapshot of a Linux host."""

import platform
from datetime import datetime, timezone

import psutil


def collect_snapshot() -> dict[str, object]:
    return {
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "hostname": platform.node(),
        "platform": platform.platform(),
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "memory_percent": psutil.virtual_memory().percent,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(collect_snapshot(), indent=2))
