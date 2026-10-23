"""тестирование сериализации запросов и ответов"""
from src.http.request import Request
from src.http.response import Response
from src.http.serializer import Serializer


def test_serialize_request():
    """проверка преобразования запроса в байты"""
    request = Request(
        method="GET",
        path="/hello",
        headers={"Host": "localhost"},
    )

    data = Serializer.serialize_request(request)

    assert data.startswith(b"GET /hello HTTP/1.1\r\n")
    assert b"Host: localhost\r\n" in data
    assert b"Content-Length: 0\r\n" in data
    assert data.endswith(b"\r\n\r\n")


def test_serialize_response():
    """проверка преобразования ответа в байты"""
    response = Response(
        status=200,
        reason="OK",
        headers={"Content-Type": "text/plain"},
        body=b"Hello",
    )

    data = Serializer.serialize_response(response)

    assert data.startswith(b"HTTP/1.1 200 OK\r\n")
    assert b"Content-Type: text/plain\r\n" in data
    assert b"Content-Length: 5\r\n" in data
    assert data.endswith(b"\r\n\r\nHello")
