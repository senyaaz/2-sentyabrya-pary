"""вход"""
import tkinter as tk
from src.gui.app import App
from src.logging_config import setup_logging


def main():
    """запуск приложения"""
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    setup_logging()
    main()
