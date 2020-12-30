import tkinter as tk
from tkinter import ttk
import ftp_client.ScrolledWindow as scr_win
import ftp_client.Interior as inter
from ftp_client.Config import gconfig
import ftp_client.ftp as ftp
from ftp_client.ftp import the_ftp

class InteriorLeftPane(inter.Interior):
    def __init__(self, *args, **kwargs):
        self.ftp=the_ftp
        the_ftp.set_interior_left_pane(self)

        super().__init__(*args, **kwargs)

    def initContainer(self):
        _height_up_left_window=40
        _height_down_left_window = 50
        _height_middle_left_window = self.root.winfo_reqheight()-\
                                     _height_up_left_window-\
                                     _height_down_left_window

        self.up_frame=ttk.Frame(self.root,
                                relief="groove",
                                borderwidth=2,
                                height=_height_up_left_window)
        self.up_frame.pack(fill=tk.X, expand=True, side=tk.TOP)
        self.root.add(self.up_frame, stretch="always")

        self.middle_frame = scr_win.ScrolledWindow(self.root)

        self.root.add(self.middle_frame, stretch="always")

        self.down_frame=ttk.Frame(self.root,
                                  relief="groove",
                                  borderwidth=2,
                                  height=_height_up_left_window)
        self.down_frame.pack(fill=tk.X, expand=True, side=tk.BOTTOM)
        self.root.add(self.down_frame, stretch="always")

        self.up_frame_interior()
        self.middle_frame_interior()
        self.down_frame_interior()

    def up_frame_interior(self):

        _label=ttk.Label(self.up_frame, text=u"Список СПУС серверов:")
        _label.pack(side=tk.TOP, padx=2, pady=2)

    def middle_frame_interior(self):

        self.server_name_list = tk.Listbox(self.middle_frame.canvas,
                                           width=self.middle_frame.canvas.winfo_reqwidth(),
                                           height=self.middle_frame.canvas.winfo_reqheight()
                                           )

        self.server_name_list.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.server_name_list.insert(0, *gconfig.server_name_list)

    def down_frame_interior(self):
        _button_width= self.down_frame.winfo_reqwidth() // 2 - 10

        self.button_connect = ttk.Button(self.down_frame,
                                         text = u'Соединение',
                                         command=self.connect_press,
                                         width=_button_width)
        self.button_connect.pack(side=tk.LEFT, padx=2, pady=2, fill=tk.X, expand=True)

        self.button_reset = ttk.Button(self.down_frame,
                                       text = u'Сброс соединения',
                                       command=self.reset_press,
                                       width=_button_width)
        self.button_reset.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.X, expand=True)

    def connect_press(self):
        if self.server_name_list.curselection():
            self.button_connect.configure(state=tk.DISABLED)
            _selected_item_index = self.server_name_list.curselection()[0]
            #print( gconfig.server_name_list[_selected_item_index] )
            gconfig.set_server_descriptor(gconfig.server_name_list[_selected_item_index])
            self.ftp.connect()

    def reset_press(self):
        self.ftp.disconnect()
        self.button_connect.configure(state=tk.NORMAL)

