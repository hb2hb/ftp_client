'''


'''
# import matplotlib
import matplotlib

matplotlib.use('TkAgg')

# import matplotlib.pyplot as plt
# matplotlib.use('TkAgg')

import tkinter as tk
from tkinter import ttk
from ftp_client.Menus import Main_menu
import ftp_client.ScrolledWindow as scr_win
import ftp_client.Interior as inter_pane
from ftp_client.Config import gconfig
import ftp_client.InteriorLeftPane as ilp
import ftp_client.InteriorRightPane as irp
import ftp_client.ftp as ftp
from ftp_client.ftp import the_ftp
import ftp_client.TabsPane as tp
import ftp_client.InteriorObserver as int_obs

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        self.width_left_pane=300
        self.width_observer_left_pane=300

        super().__init__(*args, **kwargs)

        self.title("SPUS servers explorer")
        self.minsize(gconfig.get_min_size_width(),
                     gconfig.get_min_size_height())
        self.geometry("{}x{}+{}+{}".format(self.winfo_screenwidth() - 400, self.winfo_screenheight() - 300, 50, 100))
        mmenu: Main_menu = Main_menu(self)
        self.config(menu=mmenu.menubar)

        self.it_self = self
        self.tab_pane=tp.TabsPane(self)
        self.tab_pane.add_tabs(tabs_name=gconfig.value_servers)
        self.tab_pane.add_tabs(tabs_name=gconfig.value_observer)

        gconfig.get_server_name_list()

    def _build_servers_pane(self):

        self.main_pane = tk.PanedWindow(self.tab_pane.get_tab(gconfig.value_servers),
                                        orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True)
        #self.main_pane = self.tab_pane.get_tab(gconfig.value_servers)

        self.left_pane = tk.PanedWindow(self.main_pane,
                                        orient=tk.VERTICAL,
                                        width=self.width_left_pane)
        self.left_pane.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.main_pane.add(self.left_pane)

        self.right_pane = tk.PanedWindow(self.main_pane,
                                         orient=tk.VERTICAL)
        self.right_pane.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)
        self.main_pane.add(self.right_pane)

        self.main_pane.update()

        lp=ilp.InteriorLeftPane(self.left_pane)
        lp.set_application_reference(self.get_it_self())

        rp=irp.InteriorRightPane(self.right_pane)
        rp.set_application_reference(self.get_it_self())


    def _build_observer_pane(self):
        self.observer_pane = tk.PanedWindow(self.tab_pane.get_tab(gconfig.value_observer),
                                        orient=tk.HORIZONTAL)
        self.observer_pane.pack(fill=tk.BOTH, expand=True)

        self.observer_left_pane = tk.PanedWindow(self.observer_pane,
                                                 orient=tk.VERTICAL,
                                                 width=self.width_observer_left_pane)
        self.observer_left_pane.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.observer_pane.add(self.observer_left_pane)

        self.observer_right_pane = tk.PanedWindow(self.observer_pane,
                                                  orient=tk.VERTICAL)
        self.observer_right_pane.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)
        self.observer_pane.add(self.observer_right_pane)

        observer_left_pane=int_obs.InteriorObserverLeftPane(self.observer_left_pane)
        observer_left_pane.set_application_reference(self.get_it_self())

        observer_right_pane=int_obs.InteriorObserverRightPane(self.observer_right_pane)
        observer_right_pane.set_application_reference(self.get_it_self())

    def get_it_self(self):
        return self.it_self

    def run(self):
        self._build_servers_pane()
        self._build_observer_pane()
        self.mainloop()


#https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/index.html
# self.left_pane.update()
# self.left_pane.winfo_reqheight()
# somewidget.update()
# somewidget.winfo_reqheight()   somewidget.winfo_height()
# somewidget.winfo_reqwidth()    somewidget.winfo_width()
#width = _width_left_pane,
#height = _height_up_left_window
