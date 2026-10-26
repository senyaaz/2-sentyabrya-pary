"""сервер для обработки клиентских запросов"""
import socket
import threading
import logging
from typing import Callable
from src.http.parser import Parser, ParseError
from src.http.response import Response
from src.http.serializer import Serializer
from src.server.router import Router
from src.net.tcp_server import TcpServer


class HttpServer:
    """сервер с обработкой запросов"""
    def __init__(
        self,
        host: str = "localhost",
        port: int = 8080,
        log_callback: Callable[[str], None] | None = None,
    ):
        self.host = host
        self.port = port
        self.router = Router()
        self.log_callback = log_callback
        self._tcp_server = None

    def _log(self, message: str):
        """записывает сообщение в лог и передаёт его в gui"""
        logging.info(message)

        if self.log_callback is not None:
            self.log_callback(message)

    def start(self):
        """запуск сервера"""
        if self._tcp_server is not None:
            return

        self._tcp_server = TcpServer(
            host=self.host,
            port=self.port,
            client_handler=self._handle_connection,
        )

        try:
            self._tcp_server.start()
        except OSError:
            self._tcp_server = None
            raise

        self._log(
            f"HTTP-сервер запущен: http://{self.host}:{self.port}"
        )

    
    def _handle_connection(self, connection, address):
        """обработка одного клиентского HTTP-соединения"""
        with connection:
            connection.settimeout(2.0)

            try:
                data = connection.recv(65536)

                if not data:
                    return

                request = Parser.parse_request(data)

                if (
                    request.version == "HTTP/1.1"
                    and not request.headers.get("Host", "").strip()
                ):
                    raise ParseError(
                        "Отсутствует обязательный заголовок Host"
                    )

                response = self.router.dispatch(request)

                self._log(
                    f"{address[0]}:{address[1]} — "
                    f"{request.method} {request.path} — "
                    f"{response.status} {response.reason}"
                )

            except socket.timeout:
                self._log("Клиент не прислал данные вовремя")
                return

            except (ParseError, ValueError):
                logging.warning("Получен некорректный HTTP-запрос")
                response = Response(
                    status=400,
                    reason="Bad Request",
                    headers={
                        "Content-Type": "text/plain; charset=utf-8"
                    },
                    body=b"400 Bad Request",
                )

            except Exception as exc:
                logging.exception("Ошибка обработки запроса")
                self._log(f"Ошибка обработки запроса: {exc}")
                response = Response(
                    status=500,
                    reason="Internal Server Error",
                    headers={
                        "Content-Type": "text/plain; charset=utf-8"
                    },
                    body=b"500 Internal Server Error",
                )

            try:
                response.headers["Connection"] = "close"
                response_data = Serializer.serialize_response(response)
                connection.sendall(response_data)
            except OSError as exc:
                self._log(f"Ошибка отправки ответа: {exc}")


    def stop(self):
            """остановка сервера"""
            if self._tcp_server is not None:
                self._tcp_server.stop()
                self._tcp_server = None
    
            self._log("HTTP-сервер остановлен")
