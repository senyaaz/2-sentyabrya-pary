"""вкладка сервера"""
import tkinter as tk
import webbrowser
from tkinter import ttk
from src.server.http_server import HttpServer


class ServerTab:
    """вкладка для управления сервером"""
    def __init__(self, parent, client_tab):
        """элементы вкладки"""
        self.frame = ttk.Frame(parent, padding=10)
        self.client_tab = client_tab
        self.server = None

        ttk.Label(self.frame, text="Порт:").grid(
            row=0, column=0, padx=5, pady=5
        )

        self.port_entry = ttk.Entry(self.frame, width=10)
        self.port_entry.grid(row=0, column=1, padx=5, pady=5)
        self.port_entry.insert(0, "8080")

        self.start_button = ttk.Button(
            self.frame,
            text="Запустить",
            command=self.start_server,
        )
        self.start_button.grid(row=0, column=2, padx=5, pady=5)

        self.stop_button = ttk.Button(
            self.frame,
            text="Остановить",
            command=self.stop_server,
            state="disabled",
        )
        self.stop_button.grid(row=0, column=3, padx=5, pady=5)

        self.browser_button = ttk.Button(
            self.frame,
            text="Открыть в браузере",
            command=self.open_browser,
        )
        self.browser_button.grid(row=0, column=4, padx=5, pady=5)

        self.status_label = ttk.Label(
            self.frame,
            text="● Сервер остановлен",
            foreground="red",
        )
        self.status_label.grid(
            row=1,
            column=0,
            columnspan=5,
            sticky="w",
            padx=5,
            pady=10,
        )

        ttk.Label(self.frame, text="Логи сервера:").grid(
            row=2,
            column=0,
            columnspan=4,
            sticky="w",
            padx=5,
            pady=5,
        )

        self.clear_button = ttk.Button(
            self.frame,
            text="Очистить лог",
            command=self.clear_log,
        )
        self.clear_button.grid(row=2, column=4, padx=5, pady=5)

        self.log_text = tk.Text(
            self.frame,
            height=20,
            state="disabled",
        )
        self.log_text.grid(
            row=3,
            column=0,
            columnspan=5,
            sticky="nsew",
            padx=5,
            pady=5,
        )

        self.frame.columnconfigure(3, weight=1)
        self.frame.rowconfigure(3, weight=1)

    def clear_log(self):
        """очистка логов"""
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")

    def start_server(self):
        """запуск сервера"""
        try:
            port = int(self.port_entry.get())

            if not 1 <= port <= 65535:
                raise ValueError("Порт должен быть от 1 до 65535")

            self.server = HttpServer(
                host="localhost",
                port=port,
                log_callback=lambda message: self.frame.after(
                    0, self.add_log, message
                ),
            )

            self.server.start()

            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.port_entry.config(state="disabled")
            self.status_label.config(
                text=f"● Сервер запущен на порту {port}",
                foreground="green",
            )
            self.add_log(f"Сервер запущен на порту {port}")

        except (ValueError, OSError) as error:
            self.server = None
            self.add_log(f"Ошибка запуска: {error}")

    def stop_server(self):
        """остановка сервера"""
        if self.server is not None:
            self.server.stop()
            self.server = None

        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.port_entry.config(state="normal")
        self.status_label.config(
            text="● Сервер остановлен",
            foreground="red",
        )
        self.add_log("Сервер остановлен")

    def add_log(self, message):
        """добавление логов"""
        self.log_text.config(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def open_browser(self):
        """открытие браузера"""
        address = self.client_tab.url_entry.get().strip()

        if not address:
            self.add_log("Ошибка: поле URL в HTTP-клиенте пустое")
            return

        if not address.startswith(("http://", "https://")):
            self.add_log(
                "Ошибка: URL должен начинаться с http:// или https://"
            )
            return

        webbrowser.open(address)
