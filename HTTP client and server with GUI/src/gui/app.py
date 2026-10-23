"""главное окно"""
import tkinter as tk
from tkinter import ttk
from src.gui.client_tab import ClientTab
from src.gui.server_tab import ServerTab


class App:
    """вкладки клиента и сервера"""
    def __init__(self, root):
        self.root = root
        self.root.title("клиент и сервер")
        self.root.geometry("1600x900")

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill="both", expand=True)

        client_frame = ttk.Frame(self.tabs)
        server_frame = ttk.Frame(self.tabs)

        self.tabs.add(client_frame, text="клиент")
        self.tabs.add(server_frame, text="сервер")

        self.client_ui = ClientTab(client_frame)
        self.client_ui.frame.pack(fill="both", expand=True)

        self.server_ui = ServerTab(
            server_frame,
            self.client_ui,
        )
        self.server_ui.frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
