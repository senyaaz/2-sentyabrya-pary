"""обработчики HTTP запросов"""
import json
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from src.http.request import Request
from src.http.response import Response


class RequestHandler(ABC):
    """базовый абстрактный класс обработчика запросов"""
    @abstractmethod
    def handle(self, request: Request):
        """обрабатывает запрос и возвращает HTTP ответ"""


class HomeHandler(RequestHandler):
    """обработчик главной страницы"""
    def handle(self, request: Request):
        body = (
            b"<!doctype html><html><body>"
            b"<h1>Hello</h1>"
            b"</body></html>"
        )

        return Response(
            status=200,
            reason="OK",
            headers={"Content-Type": "text/html; charset=utf-8"},
            body=body,
        )


class EchoHandler(RequestHandler):
    """возвращает тело запроса"""
    def handle(self, request: Request):
        return Response(
            status=200,
            reason="OK",
            headers={
                "Content-Type": request.headers.get(
                    "Content-Type", "application/octet-stream"
                )
            },
            body=request.body,
        )


class TimeHandler(RequestHandler):
    """получение текущего времени"""
    def handle(self, request: Request):
        current_time = datetime.now(timezone.utc).isoformat()
        body = json.dumps({"time": current_time}).encode("utf-8")

        return Response(
            status=200,
            reason="OK",
            headers={"Content-Type": "application/json"},
            body=body,
        )


class HeadersHandler(RequestHandler):
    """просмотр заголовков запроса"""
    def handle(self, request: Request):
        body = json.dumps(request.headers).encode("utf-8")

        return Response(
            status=200,
            reason="OK",
            headers={"Content-Type": "application/json"},
            body=body,
        )


class StatusHandler(RequestHandler):
    """обработчик запросов с заданным статус кодом"""
    def __init__(self, code: int):
        self.code = code

    def handle(self, request: Request):
        """формирование ответа"""
        reasons = {
            200: "OK",
            201: "Created",
            204: "No Content",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
            503: "Service Unavailable",
        }

        reason = reasons.get(self.code, "Status")

        body = f"HTTP status: {self.code} {reason}".encode("utf-8")

        return Response(
            status=self.code,
            reason=reason,
            headers={"Content-Type": "text/plain; charset=utf-8"},
            body=body,
        )
