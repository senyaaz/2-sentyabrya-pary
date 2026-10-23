"""работа с HTTP клиентом"""
from urllib.parse import urljoin
from src.http.url import Url
from src.http.request import Request
from src.http.parser import Parser
from src.http.serializer import Serializer
from src.net.tcp_client import TcpClient
from src.http.errors import HttpError


class HttpClient:
    """отправляет запросы серверу"""

    def __init__(self, timeout: float = 5.0):
        self.timeout = timeout
        self.tcp_client = TcpClient(timeout=timeout)

    def set_timeout(self, ms: int):
        """установка таймаута"""
        if ms <= 0:
            raise ValueError("Таймаут должен быть больше нуля")

        self.timeout = ms / 1000
        self.tcp_client.timeout = self.timeout

    def get(
        self,
        address: str,
        headers: dict[str, str] | None = None,
    ):
        """отправка GET запроса серверу"""
        return self.request("GET", address, headers=headers)

    def post(
        self,
        address: str,
        body: bytes,
        content_type: str = "text/plain; charset=utf-8",
        headers: dict[str, str] | None = None,
    ):
        """отправка POST запроса"""
        request_headers = dict(headers or {})
        request_headers.setdefault("Content-Type", content_type)

        return self.request(
            "POST",
            address,
            headers=request_headers,
            body=body,
        )

    def request(
        self,
        method: str,
        address: str,
        headers: dict[str, str] | None = None,
        body: bytes = b"",
        max_redirects: int = 0,
    ):
        """создание отправка запроса и получение ответа"""
        url = Url.parse(address)

        request_headers = dict(headers or {})
        request_headers.setdefault("Host", url.host)
        request_headers.setdefault("Connection", "close")

        if body:
            request_headers.setdefault("Content-Length", str(len(body)))

        path = url.path
        if url.query:
            path += f"?{url.query}"

        http_request = Request(
            method=method.upper(),
            path=path,
            headers=request_headers,
            body=body,
        )

        raw_request = Serializer.serialize_request(http_request)

        raw_response = self.tcp_client.send_request(
            host=url.host,
            port=url.port,
            data=raw_request,
            use_tls=(url.scheme == "https"),
        )

        response = Parser.parse_response(raw_response)

        redirect_codes = {301, 302, 303, 307, 308}
        location = response.headers.get("Location")

        if (
            response.status in redirect_codes
            and location
            and max_redirects > 0
        ):
            redirect_url = self._resolve_redirect(address, location)

            if response.status == 303:
                method = "GET"
                body = b""

            return self.request(
                method=method,
                address=redirect_url,
                headers=headers,
                body=body,
                max_redirects=max_redirects - 1,
            )

        if response.status >= 400:
            raise HttpError(response.status, response.reason)
        return response

    def follow_redirects(
        self,
        address: str,
        max_redirects: int = 5,
        headers: dict[str, str] | None = None,
    ):
        """отправка GET запроса с переходами по редиректам"""
        if max_redirects < 0:
            raise ValueError(
                "Количество редиректов не может быть отрицательным"
            )

        return self.request(
            "GET",
            address,
            headers=headers,
            max_redirects=max_redirects,
        )

    @staticmethod
    def _resolve_redirect(current_url: str, location: str):
        """обработка абсолютного и относительного адреса редиректа"""
        return urljoin(current_url, location)
