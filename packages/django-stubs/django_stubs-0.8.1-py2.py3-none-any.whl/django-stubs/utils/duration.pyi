from datetime import timedelta
from typing import Any, Optional

def duration_string(duration: timedelta) -> str: ...
def duration_iso_string(duration: timedelta) -> str: ...
def duration_microseconds(delta: timedelta) -> int: ...
