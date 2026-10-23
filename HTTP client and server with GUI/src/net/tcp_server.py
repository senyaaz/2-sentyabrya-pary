"""интеграционные тесты клиента и сервера"""
import socket
import threading
import time
import pytest
from src.client.http_client import HttpClient
from src.server.http_server import HttpServer


def _free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("localhost", 0))
        return s.getsockname()[1]


@pytest.fixture()
def server():
    """запуск тестового HTTP-сервера и его остановка после теста"""
    port = _free_port()
    port = _free_port()
    srv = HttpServer(host="localhost", port=port)
    srv.start()
    time.sleep(0.05)
    try:
        yield srv, port
    finally:
        srv.stop()


def test_get_home(server):
    """главная страница"""
    _, port = server
    client = HttpClient()
    response = client.get(f"http://localhost:{port}/")
    assert response.status == 200
    assert b"Hello" in response.body


def test_post_echo(server):
    """эхо POST"""
    _, port = server
    client = HttpClient()
    response = client.post(f"http://localhost:{port}/echo", body=b"abc")
    assert response.status == 200
    assert response.body == b"abc"
    assert response.headers.get("Content-Type") == "text/plain; charset=utf-8"


def test_status_route(server):
    """/status/404"""
    _, port = server
    client = HttpClient()
    response = client.get(f"http://localhost:{port}/status/404")
    assert response.status == 404


def test_nonexistent(server):
    """неизвестный маршрут"""
    _, port = server
    client = HttpClient()
    response = client.get(f"http://localhost:{port}/nonexistent")
    assert response.status == 404


def test_sequential_100_gets(server):
    """100 последовательных GET"""
    _, port = server
    client = HttpClient()
    for _ in range(100):
        response = client.get(f"http://localhost:{port}/")
        assert response.status == 200


def test_parallel_10_gets(server):
    """10 параллельных GET"""
    _, port = server
    results = []
    errors = []

    def worker():
        try:
            client = HttpClient()
            results.append(
                client.get(f"http://localhost:{port}/").status
            )
        except Exception as exc:
            errors.append(exc)

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors
    assert results == [200] * 10


def test_timeout():
    """таймаут при медленном сервере"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.bind(("localhost", 0))
        srv.listen(1)
        port = srv.getsockname()[1]

        def slow():
            conn, _ = srv.accept()
            time.sleep(1.0)
            conn.close()

        threading.Thread(target=slow, daemon=True).start()

        client = HttpClient(timeout=0.1)
        with pytest.raises((TimeoutError, ConnectionError, OSError)):
            client.get(f"http://localhost:{port}/")


def test_garbage_request_returns_400():
    """мусор вместо HTTP 400, сервер жив"""
    port = _free_port()
    srv = HttpServer(host="localhost", port=port)
    srv.start()
    time.sleep(0.05)
    try:
        with socket.create_connection(("localhost", port), timeout=2) as s:
            s.sendall(b"GARBAGE\r\n\r\n")
            data = s.recv(4096)
        assert b"400" in data

        client = HttpClient()
        assert client.get(f"http://localhost:{port}/").status == 200
    finally:
        srv.stop()


def test_1000_requests_no_crash():
    """1000 запросов без падений"""
    port = _free_port()
    srv = HttpServer(host="localhost", port=port)
    srv.start()
    time.sleep(0.05)
    try:
        client = HttpClient()
        for _ in range(1000):
            assert client.get(f"http://localhost:{port}/").status == 200
    finally:
        srv.stop()
