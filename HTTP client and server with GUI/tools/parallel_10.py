"""10 параллельных GET запросов к локальному серверу"""
import threading
from src.client.http_client import HttpClient

PORT = 8080
N = 100

results = []
errors = []
lock = threading.Lock()


def worker():
    try:
        client = HttpClient()
        response = client.get(f"http://localhost:{PORT}/")
        with lock:
            results.append(response.status)
    except Exception as exc:
        with lock:
            errors.append(repr(exc))


threads = [threading.Thread(target=worker) for _ in range(N)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"Успешных ответов: {len(results)}")
print(f"Ошибок: {len(errors)}")
print(f"Все 200: {all(status == 200 for status in results)}")
if errors:
    print("Ошибки:", errors)