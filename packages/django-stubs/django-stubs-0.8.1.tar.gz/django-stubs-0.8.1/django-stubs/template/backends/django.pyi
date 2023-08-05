from typing import Any, Dict, Iterator, Optional, List

from django.template.base import Template as Template
from django.template.exceptions import TemplateDoesNotExist

from django.template.engine import Engine
from .base import BaseEngine

class DjangoTemplates(BaseEngine):
    app_dirs: bool
    dirs: List[str]
    name: str
    app_dirname: str = ...
    engine: Engine = ...
    def __init__(self, params: Dict[str, Any]) -> None: ...
    def from_string(self, template_code: str) -> Template: ...
    def get_template(self, template_name: str) -> Template: ...
    def get_templatetag_libraries(self, custom_libraries: Dict[str, str]) -> Dict[str, str]: ...

def copy_exception(exc: TemplateDoesNotExist, backend: Optional[DjangoTemplates] = ...) -> TemplateDoesNotExist: ...
def reraise(exc: TemplateDoesNotExist, backend: DjangoTemplates) -> Any: ...
def get_installed_libraries() -> Dict[str, str]: ...
def get_package_libraries(pkg: Any) -> Iterator[str]: ...
