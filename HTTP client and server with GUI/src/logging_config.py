"""настройка логирования"""
import logging
from pathlib import Path


def setup_logging():
    """настройка записей логов в файл и консоль"""
    log_file = Path(__file__).resolve().parent.parent / "app.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
