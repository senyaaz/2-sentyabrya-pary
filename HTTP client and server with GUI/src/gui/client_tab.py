"""вкладка клиента"""
import tkinter as tk
import threading
import json as _json
import re
from tkinter import ttk
from src.client.http_client import HttpClient


class ClientTab:
    """вкладка для отправки HTTP запросов"""
    def __init__(self, parent):
        """создание элементов вкладки"""
        self.frame = ttk.Frame(parent, padding=10)
        self.client = HttpClient()

        ttk.Label(self.frame, text="URL:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )

        self.url_entry = ttk.Entry(self.frame, width=70)
        self.url_entry.grid(
            row=0,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=5,
            pady=5,
        )
        self.url_entry.insert(0, "http://localhost:8080/")

        ttk.Label(self.frame, text="Метод:").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )

        self.method = ttk.Combobox(
            self.frame,
            values=["GET", "POST"],
            state="readonly",
            width=10,
        )
        self.method.grid(
            row=1, column=1, sticky="w", padx=5, pady=5
        )
        self.method.set("GET")
        self.method.bind(
            "<<ComboboxSelected>>",
            self.on_method_change,
        )

        ttk.Label(self.frame, text="Заголовки:").grid(
            row=2, column=0, sticky="nw", padx=5, pady=5
        )

        self.headers_table = ttk.Treeview(
            self.frame,
            columns=("name", "value"),
            show="headings",
            height=3,
        )
        self.headers_table.heading("name", text="Имя")
        self.headers_table.heading("value", text="Значение")
        self.headers_table.column("name", width=180)
        self.headers_table.column("value", width=350)

        self.headers_table.grid(
            row=2, column=1, columnspan=2,
            sticky="ew", padx=5, pady=5,
        )

        self.headers_table.bind(
            "<Double-1>", self.edit_header
        )

        headers_buttons = ttk.Frame(self.frame)
        headers_buttons.grid(
            row=3, column=1, columnspan=2,
            sticky="w", padx=5, pady=2,
        )

        ttk.Button(
            headers_buttons,
            text="Добавить",
            command=self.add_header,
        ).pack(side="left", padx=(0, 5))

        ttk.Button(
            headers_buttons,
            text="Удалить",
            command=self.delete_header,
        ).pack(side="left")

        self.header_entry = None

        ttk.Label(self.frame, text="Тело запроса:").grid(
            row=4, column=0, sticky="nw", padx=5, pady=5
        )

        self.body_text = tk.Text(self.frame, height=5, width=60)
        self.body_text.grid(
            row=4,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=5,
            pady=5,
        )

        self.on_method_change()

        buttons_frame = ttk.Frame(self.frame)
        buttons_frame.grid(
            row=5, column=1, columnspan=2,
            sticky="w", padx=5, pady=10,
        )

        self.send_button = ttk.Button(
            buttons_frame,
            text="Отправить запрос",
            command=self.send_request,
        )
        self.send_button.pack(side="left", padx=(0, 5))

        ttk.Button(
            buttons_frame,
            text="Очистить",
            command=self.clear_fields,
        ).pack(side="left")

        ttk.Label(self.frame, text="Ответ сервера:").grid(
            row=6, column=0, sticky="nw", padx=5, pady=5
        )

        self.response_text = tk.Text(
            self.frame, height=18, width=70, state="disabled"
        )
        self.response_text.grid(
            row=6,
            column=1,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
        )

        self.response_text.tag_configure("status_ok", foreground="#008000")
        self.response_text.tag_configure("status_err", foreground="#c00000")
        self.response_text.tag_configure("header", foreground="#0000c0")
        self.response_text.tag_configure("json_key", foreground="#8b008b")
        self.response_text.tag_configure("json_str", foreground="#a0522d")

        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(6, weight=1)

    def on_method_change(self, _event=None):
        """изменяет доступность тела запроса в зависимости от метода"""
        if self.method.get() == "GET":
            self.body_text.config(state="disabled")
        else:
            self.body_text.config(state="normal")

    def add_header(self):
        """добавляет новую строку заголовка"""
        self.headers_table.insert(
            "", tk.END, values=("", "")
        )

    def delete_header(self):
        """удаляет выбранный заголовок"""
        selected = self.headers_table.selection()
        if selected:
            self.headers_table.delete(selected)

    def clear_fields(self):
        """очистка"""
        self.url_entry.delete(0, tk.END)

        self.body_text.config(state="normal")
        self.body_text.delete("1.0", tk.END)

        for item in self.headers_table.get_children():
            self.headers_table.delete(item)

        self.response_text.config(state="normal")
        self.response_text.delete("1.0", tk.END)
        self.response_text.config(state="disabled")

    def edit_header(self, event):
        """редактирование ячейку двойным щелчком"""
        item = self.headers_table.identify_row(event.y)
        column = self.headers_table.identify_column(event.x)

        if not item or column not in ("#1", "#2"):
            return

        bbox = self.headers_table.bbox(item, column)
        if not bbox:
            return

        x, y, width, height = bbox
        values = list(self.headers_table.item(item, "values"))
        index = int(column[1:]) - 1

        editor = ttk.Entry(self.headers_table)
        editor.place(x=x, y=y, width=width, height=height)
        editor.insert(0, values[index])
        editor.focus_set()

        def save_edit(event=None):
            values[index] = editor.get().strip()
            self.headers_table.item(item, values=values)
            editor.destroy()

        editor.bind("<Return>", save_edit)
        editor.bind("<FocusOut>", save_edit)
        editor.bind("<Escape>", lambda event: editor.destroy())

    def send_request(self):
        """отправка запроса в отдельном потоке"""
        self.send_button.config(state="disabled")
        self.response_text.config(state="normal")
        self.response_text.delete("1.0", tk.END)
        self.response_text.insert("1.0", "Отправка запроса...")
        self.response_text.config(state="disabled")

        headers = {}
        for item in self.headers_table.get_children():
            name, value = self.headers_table.item(item, "values")
            if name.strip():
                headers[name.strip()] = value.strip()

        url = self.url_entry.get().strip()
        method = self.method.get()
        body = self.body_text.get("1.0", tk.END).rstrip("\n")

        threading.Thread(
            target=self._perform_request,
            args=(url, method, body, headers),
            daemon=True,
        ).start()

    def _perform_request(self, url, method, body, headers):
        """отправляет запрос и готовит ответ"""
        try:
            if method == "GET":
                response = self.client.get(url, headers=headers)
            else:
                headers.setdefault(
                    "Content-Type", "text/plain; charset=utf-8"
                )
                response = self.client.post(
                    url,
                    body=body.encode("utf-8"),
                    headers=headers,
                )

            response_body = response.body.decode(
                "utf-8", errors="replace"
            )

            self.frame.after(
                0,
                self._show_response,
                None,
                response.status,
                response.headers,
                response_body,
            )
            return

        except Exception as exc:
            result = f"Ошибка: {exc}"

        self.frame.after(0, self._show_response, result)

    def _show_response(self, result, status=None, headers=None, body=None):
        """ответ сервера с подсветкой"""
        self.response_text.config(state="normal")
        self.response_text.delete("1.0", tk.END)

        if status is None:
            self.response_text.insert("1.0", result)
            self.response_text.config(state="disabled")
            self.send_button.config(state="normal")
            return

        tag = "status_ok" if 200 <= status < 400 else "status_err"
        self.response_text.insert(tk.END, f"HTTP {status}\n\n", tag)

        self.response_text.insert(tk.END, "Заголовки:\n", "header")
        for name, value in headers.items():
            self.response_text.insert(
                tk.END, f"  {name}: {value}\n", "header"
            )

        self.response_text.insert(tk.END, "\nТело ответа:\n")

        try:
            parsed = _json.loads(body)
        except (ValueError, TypeError):
            parsed = None

        if parsed is not None:
            pretty = _json.dumps(parsed, ensure_ascii=False, indent=2)
            self.response_text.insert(tk.END, pretty)
            self._highlight_json(pretty)
        else:
            self.response_text.insert(tk.END, body)

        self.response_text.config(state="disabled")
        self.send_button.config(state="normal")

    def _highlight_json(self, text):
        """подсветка ключей JSON"""
        pattern = r'"(?:\\.|[^"\\])*"(?=\s*:)'
        for match in re.finditer(pattern, text):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.response_text.tag_add("json_key", start, end)
