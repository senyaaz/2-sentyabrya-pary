"""разбор и проверка url"""
from dataclasses import dataclass
from urllib.parse import urlsplit


class ParseError(ValueError):
    """ошибка при разборе или проверке url"""


@dataclass
class Url:
    """хранение частей URL адреса"""

    scheme: str
    host: str
    port: int
    path: str
    query: str = ""

    @classmethod
    def parse(cls, address: str):
        """разбор url и возврат объекта url"""
        parts = urlsplit(address)

        if parts.scheme not in ("http", "https"):
            raise ParseError("Поддерживаются только http и https")

        if not parts.hostname:
            raise ParseError("В URL не указан хост")

        try:
            port = parts.port
        except ValueError as exc:
            raise ParseError("Некорректный порт") from exc

        if port is None:
            port = 443 if parts.scheme == "https" else 80

        if not 1 <= port <= 65535:
            raise ParseError("Порт должен быть от 1 до 65535")

        return cls(
            scheme=parts.scheme,
            host=parts.hostname,
            port=port,
            path=parts.path or "/",
            query=parts.query,
        )
