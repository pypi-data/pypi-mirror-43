from typing import Callable

def xframe_options_deny(view_func: Callable) -> Callable: ...
def xframe_options_sameorigin(view_func: Callable) -> Callable: ...
def xframe_options_exempt(view_func: Callable) -> Callable: ...
