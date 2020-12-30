'''

'''
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

class Main_menu(object):
    def __init__(self, root, *args, **kwargs) -> object:
        self.root = root
        super().__init__(*args, **kwargs)

        self.menubar = tk.Menu(self.root)

        self.file_item = tk.Menu(self.menubar, tearoff=0)

        self.file_item.add_command(label=u'Открыть',
                                   accelerator='Ctrl+O',
                                   compound='left', underline=0,
                                   command=lambda: self.open_config())


        self.file_item.add_separator()

        self.file_item.add_command(label=u'Выход',
                                   accelerator='Alt+X',
                                   command=self.root.quit)

        self.menubar.add_cascade(label=u'Файл', menu=self.file_item)

        self.about_item = tk.Menu(self.menubar, tearoff=0)
        self.about_item.add_command(label=u'О проекте',
                                    compound='left', underline=0,
                                    command=lambda: self.about_project())
        self.about_item.add_command(label=u'Разработчик',
                                    compound='left', underline=0,
                                    command=lambda: self.about_developer())

        self.menubar.add_cascade(label=u'Помощь', menu=self.about_item)

    def open_config(self):
        self.projectNameFile = tk.filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("project files","*.prj"),("all files","*.*")))
        print(self.projectNameFile)

    def about_project(self):
        tk.messagebox.showinfo('Project ftp client',
                               'Project ftp client created\nto explore ftp server')

    def about_developer(self):
        tk.messagebox.showinfo("Developers",
                               "created by:\nHB\nhb2hb@yandex.ru")

