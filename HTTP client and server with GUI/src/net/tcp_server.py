
"""работа TCP сервера"""
import socket
import threading
from typing import Callable


class TcpServer:
    """TCP сервер для приёма клиентских подключений"""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 8080,
        client_handler: Callable[[socket.socket, tuple], None] | None = None,
    ):
        self.host = host
        self.port = port
        self.client_handler = client_handler
        self._socket = None
        self._thread = None
        self._running = False

    def start(self):
        """запуск TCP сервера"""
        if self._running:
            return

        server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )
        server_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1,
        )

        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            server_socket.settimeout(0.5)
        except OSError:
            server_socket.close()
            raise

        self._socket = server_socket
        self._running = True
        self._thread = threading.Thread(
            target=self._serve,
            daemon=True,
        )
        self._thread.start()

    def _serve(self):
        """приём клиентских подключений"""
        while self._running:
            try:
                connection, address = self._socket.accept()
            except socket.timeout:
                continue
            except OSError:
                break

            if self.client_handler is None:
                connection.close()
                continue

            threading.Thread(
                target=self._handle_client,
                args=(connection, address),
                daemon=True,
            ).start()

    def _handle_client(self, connection, address):
        """передача подключения обработчику"""
        try:
            self.client_handler(connection, address)
        except Exception:
            connection.close()

    def stop(self):
        """остановка TCP сервера"""
        self._running = False

        if self._socket is not None:
            self._socket.close()
            self._socket = None

        if self._thread is not None:
            self._thread.join(timeout=2)
            self._thread = None
