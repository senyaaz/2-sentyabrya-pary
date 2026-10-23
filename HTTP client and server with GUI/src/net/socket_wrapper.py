"""сетевое соединение"""
import socket
import ssl
from abc import ABC, abstractmethod


class Connection(ABC):
    """абстрактный интерфейс сетевого соединения"""

    @abstractmethod
    def connect(
        self,
        host: str,
        port: int,
        use_tls: bool = False,
    ):
        """подключение к серверу"""

    @abstractmethod
    def send(self, data: bytes):
        """отправка данных"""

    @abstractmethod
    def receive(self, size: int = 4096):
        """приём данных"""

    @abstractmethod
    def close(self):
        """закрытие соединения"""


class SocketWrapper(Connection):
    """сетевое соединение через сокет"""

    def __init__(self, timeout: float = 5.0):
        """создание объекта и задаётся время ожидания"""
        self.timeout = timeout
        self._socket = None

    def connect(
        self,
        host: str,
        port: int,
        use_tls: bool = False,
    ):
        """подключение к серверу"""
        connection = socket.create_connection(
            (host, port),
            timeout=self.timeout,
        )

        if use_tls:
            context = ssl.create_default_context()
            try:
                connection = context.wrap_socket(
                    connection,
                    server_hostname=host,
                )
            except Exception:
                connection.close()
                raise

        self._socket = connection

    def send(self, data: bytes):
        """отправка данных"""
        if self._socket is None:
            raise RuntimeError("Сначала нужно установить соединение")

        self._socket.sendall(data)

    def receive(self, size: int = 4096):
        """Принимает данные."""
        if self._socket is None:
            raise RuntimeError("Сначала нужно установить соединение")

        return self._socket.recv(size)

    def close(self):
        """закрытие соединения"""
        if self._socket is not None:
            self._socket.close()
            self._socket = None

    def __enter__(self):
        """использования объекта с оператором with"""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """закрытие соединения после завершения блока with"""
        self.close()
