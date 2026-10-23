"""класс HTTP ответа"""
from dataclasses import dataclass, field


@dataclass
class Response:
    """представляет HTTP ответ"""
    status: int
    reason: str = ""
    version: str = "HTTP/1.1"
    headers: dict[str, str] = field(default_factory=dict)
    body: bytes = b""
