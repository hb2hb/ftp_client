import tkinter as tk
from tkinter import ttk
from ftp_client.Config import gconfig

class TabsPane(object):
    def __init__(self, root, *args, **kwargs):
        self.root=root
        self.internal_panes = {}    #Tab name => pane
        self.note_book = ttk.Notebook(self.root)
        self.note_book.enable_traversal()
        self.note_book.pack(fill=tk.BOTH, expand=True)

        super().__init__(*args, **kwargs)

    def add_tabs(self, tabs_name=None):
        if not tabs_name:
            return

        if self.internal_panes.get(tabs_name) is None:
            _frame=ttk.Frame(self.note_book)
            _frame.pack(fill=tk.BOTH, expand=True)
            self.note_book.add(_frame, text=tabs_name)
            self.internal_panes[tabs_name]=_frame

    def get_tab(self, tabs_name=None):
        if not tabs_name:
            return None

        if self.internal_panes.get(tabs_name) is None:
            return None
        else:
            return self.internal_panes[tabs_name]


