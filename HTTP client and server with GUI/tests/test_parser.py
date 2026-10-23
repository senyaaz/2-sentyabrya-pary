"""тестирование разбора запросов и ответов"""
import pytest
from src.http.parser import Parser, ParseError


def test_parse_request():
    """проверка разбора GET запроса"""
    raw = (
        b"GET /hello HTTP/1.1\r\n"
        b"Host: localhost\r\n"
        b"Connection: close\r\n"
        b"\r\n"
    )

    request = Parser.parse_request(raw)

    assert request.method == "GET"
    assert request.path == "/hello"
    assert request.version == "HTTP/1.1"
    assert request.headers["Host"] == "localhost"


def test_parse_post_request_body():
    """проверка чтения тела POST запроса"""
    raw = (
        b"POST /echo HTTP/1.1\r\n"
        b"Host: localhost\r\n"
        b"Content-Length: 5\r\n"
        b"\r\n"
        b"Hello"
    )

    request = Parser.parse_request(raw)

    assert request.method == "POST"
    assert request.path == "/echo"
    assert request.body == b"Hello"


def test_parse_chunked_response():
    """проверка разбора ответа с chunked кодированием"""
    raw = (
        b"HTTP/1.1 200 OK\r\n"
        b"Transfer-Encoding: chunked\r\n"
        b"Content-Type: text/plain\r\n"
        b"\r\n"
        b"5\r\nHello\r\n"
        b"6\r\n World\r\n"
        b"0\r\n\r\n"
    )

    response = Parser.parse_response(raw)

    assert response.status == 200
    assert response.body == b"Hello World"


def test_header_too_large():
    """проверка ограничения размера заголовков в 8 КБ"""
    raw = (
        b"GET / HTTP/1.1\r\n"
        b"Host: localhost\r\n"
        b"X-Large-Header: " + b"A" * (9 * 1024) + b"\r\n\r\n"
    )

    with pytest.raises(ParseError):
        Parser.parse_request(raw)
