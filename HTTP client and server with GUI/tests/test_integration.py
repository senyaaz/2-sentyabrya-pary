"""интеграционные тесты клиента и сервера"""
import socket
import threading
import time
import pytest
from src.http.errors import HttpError
from src.client.http_client import HttpClient
from src.server.http_server import HttpServer


def _free_port():
    """находит свободный TCP порт"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("localhost", 0))
        return sock.getsockname()[1]


def _start_server():
    """запускает HTTP сервер на свободном порту"""
    port = _free_port()
    server = HttpServer(host="localhost", port=port)
    server.start()
    time.sleep(0.05)
    return server, port


def test_get_home():
    """проверка получения главной страницы"""
    server, port = _start_server()

    try:
        client = HttpClient()
        response = client.get(f"http://localhost:{port}/")

        assert response.status == 200
        assert b"Hello" in response.body
    finally:
        server.stop()


def test_post_echo():
    """проверка возврата тела POST запроса"""
    server, port = _start_server()

    try:
        client = HttpClient()
        response = client.post(
            f"http://localhost:{port}/echo",
            body="hello",
        )

        assert response.status == 200
        assert response.body == b"hello"
    finally:
        server.stop()


def test_status_404():
    """проверка маршрута с кодом 404"""
    server, port = _start_server()

    try:
        client = HttpClient()

        try:
            client.get(f"http://localhost:{port}/status/404")
            assert False, "Ожидалось исключение HttpError"
        except HttpError as exc:
            assert exc.status == 404
    finally:
        server.stop()


def test_nonexistent_route():
    """проверка несуществующего маршрута"""
    server, port = _start_server()

    try:
        client = HttpClient()

        try:
            client.get(f"http://localhost:{port}/nonexistent")
            assert False, "Ожидалось исключение HttpError"
        except HttpError as exc:
            assert exc.status == 404
    finally:
        server.stop()


def test_100_sequential_gets():
    """проверка 100 последовательных GET запросов"""
    server, port = _start_server()

    try:
        client = HttpClient()

        for _ in range(100):
            response = client.get(f"http://localhost:{port}/")
            assert response.status == 200
    finally:
        server.stop()


def test_10_parallel_gets():
    """проверка 10 параллельных GET запросов"""
    server, port = _start_server()
    results = []
    errors = []
    lock = threading.Lock()

    def worker():
        try:
            client = HttpClient()
            response = client.get(f"http://localhost:{port}/")

            with lock:
                results.append(response.status)
        except Exception as exc:
            with lock:
                errors.append(exc)

    try:
        threads = [
            threading.Thread(target=worker)
            for _ in range(10)
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join(timeout=10)

        assert all(not thread.is_alive() for thread in threads)
        assert not errors
        assert results == [200] * 10
    finally:
        server.stop()


def test_missing_host_returns_400():
    """проверка ответа 400 при отсутствии заголовка Host"""
    server, port = _start_server()

    try:
        with socket.create_connection(("localhost", port)) as sock:
            sock.sendall(b"GET / HTTP/1.1\r\n\r\n")
            response = sock.recv(4096)

        assert b"400 Bad Request" in response
    finally:
        server.stop()


def test_timeout_on_slow_server():
    """клиент должен бросить TimeoutError при медленном сервере"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.bind(("localhost", 0))
        srv.listen(1)
        port = srv.getsockname()[1]

        def slow_server():
            conn, _ = srv.accept()
            time.sleep(1.0)
            conn.close()

        threading.Thread(target=slow_server, daemon=True).start()

        client = HttpClient(timeout=0.1)

        with pytest.raises((TimeoutError, ConnectionError, OSError)):
            client.get(f"http://localhost:{port}/")


def test_garbage_returns_400_and_server_survives():
    """мусор вместо HTTP 400, сервер продолжает работать"""
    server, port = _start_server()

    try:
        with socket.create_connection(("localhost", port), timeout=2) as sock:
            sock.sendall(b"THIS IS NOT HTTP\r\n\r\n")
            response = sock.recv(4096)

        assert b"400 Bad Request" in response

        client = HttpClient()
        response = client.get(f"http://localhost:{port}/")
        assert response.status == 200
    finally:
        server.stop()


def test_1000_requests_no_crash():
    """1000 запросов без падений и зависаний"""
    server, port = _start_server()

    try:
        client = HttpClient()

        for _ in range(1000):
            response = client.get(f"http://localhost:{port}/")
            assert response.status == 200
    finally:
        server.stop()
