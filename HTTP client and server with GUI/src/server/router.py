"""маршрутизация запросов"""
from src.http.request import Request
from src.http.response import Response
from src.server.handlers import (
    HomeHandler,
    EchoHandler,
    TimeHandler,
    HeadersHandler,
    StatusHandler,
)


class Router:
    """выбор обработчика в зависимости от метода и пути"""
    def __init__(self):
        self.routes = {
            ("GET", "/"): HomeHandler(),
            ("POST", "/echo"): EchoHandler(),
            ("GET", "/time"): TimeHandler(),
            ("GET", "/headers"): HeadersHandler(),
        }

    def dispatch(self, request: Request):
        """поиск маршрута и формирование ответа"""
        method = request.method.upper()
        path = request.path

        if method == "GET" and path.startswith("/status/"):
            code_text = path.removeprefix("/status/")

            if not code_text.isdigit():
                return Response(
                    status=400,
                    reason="Bad Request",
                    headers={
                        "Content-Type": "text/plain; charset=utf-8"
                    },
                    body=b"Invalid status code",
                )

            code = int(code_text)

            if not 100 <= code <= 599:
                return Response(
                    status=400,
                    reason="Bad Request",
                    headers={
                        "Content-Type": "text/plain; charset=utf-8"
                    },
                    body=b"Status code must be between 100 and 599",
                )

            return StatusHandler(code).handle(request)

        route = self.routes.get((method, path))

        if route is None:
            return Response(
                status=404,
                reason="Not Found",
                headers={"Content-Type": "text/plain; charset=utf-8"},
                body=b"404 Not Found",
            )

        return route.handle(request)
