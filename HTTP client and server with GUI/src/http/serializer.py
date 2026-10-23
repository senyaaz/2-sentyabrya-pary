"""преобразования HTTP сообщений в байты"""
from src.http.request import Request
from src.http.response import Response
from email.utils import formatdate


class Serializer:
    """преобразование HTTP запросы и ответы в байты"""
    @staticmethod
    def serialize_request(request: Request):
        lines = [
            f"{request.method} {request.path} {request.version}"
        ]

        headers = dict(request.headers)

        if not any(name.lower() == "host" for name in headers):
            raise ValueError("Для HTTP-запроса нужен заголовок Host")

        if not any(
            name.lower() == "content-length"
            for name in headers
        ):
            headers["Content-Length"] = str(len(request.body))

        for name, value in headers.items():
            lines.append(f"{name}: {value}")

        head = "\r\n".join(lines) + "\r\n\r\n"
        body = request.body

        if isinstance(body, str):
            body = body.encode("utf-8")

        return head.encode("iso-8859-1") + body

    @staticmethod
    def serialize_response(response: Response):
        lines = [
            f"{response.version} {response.status} {response.reason}"
        ]

        headers = dict(response.headers)

        if not any(
            name.lower() == "content-length"
            for name in headers
        ):
            headers["Content-Length"] = str(len(response.body))

        if not any(name.lower() == "date" for name in headers):
            headers["Date"] = formatdate(usegmt=True)

        for name, value in headers.items():
            lines.append(f"{name}: {value}")

        head = "\r\n".join(lines) + "\r\n\r\n"
        return head.encode("iso-8859-1") + response.body
