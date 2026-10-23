"""работа TCP клиента"""
from src.net.socket_wrapper import SocketWrapper


class TcpClient:
    """отправка данных"""
    def __init__(self, timeout: float = 5.0):
        """создание клиента и времени ожидания"""
        self.timeout = timeout

    def send_request(
        self,
        host: str,
        port: int,
        data: bytes,
        use_tls: bool = False,
    ):
        """отправка запроса и получение ответа"""
        with SocketWrapper(timeout=self.timeout) as connection:
            connection.connect(
                host,
                port,
                use_tls=use_tls,
            )
            connection.send(data)

            chunks = []

            while True:
                chunk = connection.receive()
                if not chunk:
                    break

                chunks.append(chunk)

            return b"".join(chunks)
