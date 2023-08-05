from typing import Any, Iterator, List, Optional, Tuple, Union

class ArchiveException(Exception): ...
class UnrecognizedArchiveFormat(ArchiveException): ...

def extract(path: str, to_path: str = ...) -> None: ...

class Archive:
    def __init__(self, file: str) -> None: ...
    def __enter__(self) -> Archive: ...
    def __exit__(self, exc_type: None, exc_value: None, traceback: None) -> None: ...
    def extract(self, to_path: str = ...) -> None: ...
    def list(self) -> None: ...
    def close(self) -> None: ...

class BaseArchive:
    def split_leading_dir(self, path: str) -> Union[List[str], Tuple[str, str]]: ...
    def has_leading_dir(self, paths: Union[Iterator[Any], List[str]]) -> bool: ...
    def extract(self) -> None: ...
    def list(self) -> None: ...

class TarArchive(BaseArchive):
    def __init__(self, file: str) -> None: ...
    def list(self, *args: Any, **kwargs: Any) -> None: ...
    def extract(self, to_path: str) -> None: ...
    def close(self) -> None: ...

class ZipArchive(BaseArchive):
    def __init__(self, file: str) -> None: ...
    def list(self, *args: Any, **kwargs: Any) -> None: ...
    def extract(self, to_path: str) -> None: ...
    def close(self) -> None: ...

extension_map: Any
