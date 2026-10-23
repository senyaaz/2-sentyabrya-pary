"""сервер для обработки клиентских запросов"""
import socket
import threading
import logging
from typing import Callable
from src.http.parser import Parser, ParseError
from src.http.response import Response
from src.http.serializer import Serializer
from src.server.router import Router


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
        self._socket = None
        self._thread = None
        self._running = False

    def _log(self, message: str):
        """записывает сообщение в лог и передаёт его в gui"""
        logging.info(message)

        if self.log_callback is not None:
            self.log_callback(message)

    def start(self):
        """запуск сервера"""
        if self._running:
            return

        self._socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )
        self._socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1,
        )
        self._socket.bind((self.host, self.port))
        self._socket.listen()
        self._socket.settimeout(0.5)

        self._running = True
        self._thread = threading.Thread(
            target=self._serve,
            daemon=True,
        )
        self._thread.start()

        self._log(
            f"HTTP-сервер запущен: http://{self.host}:{self.port}"
        )

    def _serve(self):
        """приём соединений и обработка запросов"""
        while self._running:
            try:
                connection, address = self._socket.accept()
            except socket.timeout:
                continue
            except OSError:
                break

            with connection:
                connection.settimeout(2.0)

                try:
                    data = connection.recv(65536)

                    if not data:
                        continue
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
                    continue

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
                    response_data = Serializer.serialize_response(
                        response
                    )
                    connection.sendall(response_data)
                except OSError as exc:
                    self._log(f"Ошибка отправки ответа: {exc}")

    def stop(self):
        """остановка сервера"""
        self._running = False

        if self._socket is not None:
            self._socket.close()
            self._socket = None

        if self._thread is not None:
            self._thread.join(timeout=2)
            self._thread = None

        self._log("HTTP-сервер остановлен")
