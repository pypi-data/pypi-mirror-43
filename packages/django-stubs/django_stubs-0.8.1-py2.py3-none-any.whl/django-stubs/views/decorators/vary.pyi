from typing import Any, Callable

def vary_on_headers(*headers: Any) -> Callable: ...
def vary_on_cookie(func: Callable) -> Callable: ...
