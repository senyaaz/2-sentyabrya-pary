"""разбор HTTP запросов и ответов"""
from src.http.request import Request
from src.http.response import Response


class ParseError(ValueError):
    """ошибка разбора HTTP сообщения"""


class Parser:
    """разбирает HTTP запросы и ответы"""

    MAX_HEADER_BYTES = 8 * 1024

    @staticmethod
    def _split_message(data: bytes):
        """разделение сообщения"""
        separator = b"\r\n\r\n"

        if len(data) > Parser.MAX_HEADER_BYTES:
            if separator in data:
                head_part = data.split(separator, 1)[0]
            else:
                head_part = data

            if len(head_part) > Parser.MAX_HEADER_BYTES:
                raise ParseError("Слишком большой блок заголовков")

        if separator not in data:
            raise ParseError("Не найдена граница заголовков и тела")

        head, body = data.split(separator, 1)
        lines = head.decode("iso-8859-1").split("\r\n")

        if not lines or not lines[0]:
            raise ParseError("Пустая стартовая строка")

        start_line = lines[0]
        headers = {}

        for line in lines[1:]:
            if ":" not in line:
                raise ParseError(f"Некорректный заголовок: {line}")

            name, value = line.split(":", 1)
            name = name.strip()
            value = value.strip()

            if not name:
                raise ParseError("Пустое имя заголовка")

            headers[name] = value

        return start_line, headers, body

    @staticmethod
    def parse_request(data: bytes):
        """разбор HTTP запроса и создание объекта request"""
        start_line, headers, body = Parser._split_message(data)
        parts = start_line.split()

        if len(parts) != 3:
            raise ParseError("Некорректная стартовая строка запроса")

        method, path, version = parts

        if not version.startswith("HTTP/"):
            raise ParseError("Некорректная версия HTTP")

        content_length = headers.get("Content-Length")

        if content_length is not None:
            try:
                length = int(content_length)
            except ValueError as exc:
                raise ParseError("Некорректный Content-Length") from exc

            if length < 0 or len(body) < length:
                raise ParseError("Тело запроса неполное")

            body = body[:length]

        return Request(
            method=method,
            path=path,
            version=version,
            headers=headers,
            body=body,
        )

    @staticmethod
    def parse_response(data: bytes):
        """разбор HTTP ответа"""
        start_line, headers, body = Parser._split_message(data)
        parts = start_line.split(" ", 2)

        if len(parts) < 2:
            raise ParseError("Некорректная стартовая строка ответа")

        version, status_text = parts[:2]

        if not version.startswith("HTTP/"):
            raise ParseError("Некорректная версия HTTP")

        try:
            status = int(status_text)
        except ValueError as exc:
            raise ParseError("Некорректный статус ответа") from exc

        reason = parts[2] if len(parts) == 3 else ""

        transfer_encoding = headers.get("Transfer-Encoding", "")
        if "chunked" in transfer_encoding.lower():
            body = Parser._decode_chunked(body)

        content_length = headers.get("Content-Length")

        if content_length is not None:
            try:
                length = int(content_length)
            except ValueError as exc:
                raise ParseError("Некорректный Content-Length") from exc

            if length < 0 or len(body) < length:
                raise ParseError("Тело ответа неполное")

            body = body[:length]

        return Response(
            status=status,
            reason=reason,
            version=version,
            headers=headers,
            body=body,
        )

    @staticmethod
    def _decode_chunked(body: bytes):
        """извлечение тела ответа из chunked формата"""
        decoded = bytearray()
        position = 0

        while True:
            line_end = body.find(b"\r\n", position)
            if line_end == -1:
                raise ParseError("Некорректный chunked-ответ")

            size_line = body[position:line_end].split(b";", 1)[0]

            try:
                size = int(size_line, 16)
            except ValueError as exc:
                raise ParseError("Некорректный размер chunk") from exc

            position = line_end + 2

            if size == 0:
                return bytes(decoded)

            chunk_end = position + size
            if chunk_end + 2 > len(body):
                raise ParseError("Неполный chunk в ответе")

            if body[chunk_end:chunk_end + 2] != b"\r\n":
                raise ParseError("Некорректное окончание chunk")

            decoded.extend(body[position:chunk_end])
            position = chunk_end + 2
