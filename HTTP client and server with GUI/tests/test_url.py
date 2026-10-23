"""тестирование разбора URL"""
import pytest
from src.http.url import Url, ParseError


def test_parse_url_with_port_path_and_query():
    """проверка url с портом, путём и параметрами"""
    url = Url.parse("http://host:8080/path?q=1")

    assert url.scheme == "http"
    assert url.host == "host"
    assert url.port == 8080
    assert url.path == "/path"
    assert url.query == "q=1"


def test_http_default_port():
    """проверка стандартного порта HTTP"""
    url = Url.parse("http://host/path")

    assert url.port == 80


def test_invalid_url():
    """проверка обработки неправильного url"""
    with pytest.raises(ParseError):
        Url.parse("garbage")
