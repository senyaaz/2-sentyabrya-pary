"""класс HTTP запроса"""
from dataclasses import dataclass, field


@dataclass
class Request:
    """представляет HTTP запрос"""
    method: str
    path: str
    version: str = "HTTP/1.1"
    headers: dict[str, str] = field(default_factory=dict)
    body: bytes = b""
