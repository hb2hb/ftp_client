from ftp_client.Config import gconfig
import tkinter as tk
from tkinter import ttk
import ftp_client.ScrolledWindow as scr_win
import ftp_client.Interior as inter
from ftp_client.Config import gconfig
import ftp_client.FileWorks as fw


class InteriorObserverLeftPane(inter.Interior):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    def initContainer(self):
        _height_up_left_window = 50
        _height_down_left_window = 60
        _height_middle_left_window = self.root.winfo_height() - \
                                     _height_up_left_window - \
                                     _height_down_left_window

        self.up_frame = ttk.Frame(self.root,
                                  relief="groove",
                                  borderwidth=2,
                                  height=_height_up_left_window)
        self.up_frame.pack(fill=tk.X, expand=True, side=tk.TOP)
        self.root.add(self.up_frame, stretch="always")

        self.middle_frame = scr_win.ScrolledWindow(self.root)
        self.root.add(self.middle_frame, stretch="always")

        self.down_frame = ttk.Frame(self.root,
                                    relief="groove",
                                    borderwidth=2,
                                    height=_height_up_left_window)
        self.down_frame.pack(fill=tk.X, expand=True, side=tk.BOTTOM)
        self.root.add(self.down_frame, stretch="always")

        self.up_frame_interior()
        self.middle_frame_interior()
        self.down_frame_interior()

    def up_frame_interior(self):
        _label = ttk.Label(self.up_frame, text=u"Список СПУС серверов:")
        _label.pack(side=tk.TOP, padx=2, pady=2)

    def middle_frame_interior(self):
        self.server_name_list = tk.Listbox(self.middle_frame.canvas,    #inner_frame,
                                           width=self.middle_frame.canvas.winfo_reqwidth(),
                                           height=self.middle_frame.canvas.winfo_reqheight()
                                           )

        self.server_name_list.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        for i in range(10):
            self.server_name_list.insert(i, str(i)*i)

    def down_frame_interior(self):
        _button_width = self.down_frame.winfo_reqwidth()

        self.button_pdf = ttk.Button(self.down_frame,
                                         text=u'Печать в PDF',
                                         command=self.button_pdf_press,
                                         width=_button_width)
        self.button_pdf.pack(side=tk.LEFT, padx=2, pady=2, fill=tk.X, expand=True)

    def button_pdf_press(self):
        pass
#######################################################################################
#
#######################################################################################
class InteriorObserverRightPane(inter.Interior):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    def initContainer(self):
        _height_up_left_window = 50
        _height_down_left_window = 60
        _height_middle_left_window = self.root.winfo_height() - \
                                     _height_up_left_window - \
                                     _height_down_left_window

        self.up_frame = ttk.Frame(self.root,
                                  relief="groove",
                                  borderwidth=2,
                                  height=_height_up_left_window)
        self.up_frame.pack(fill=tk.X, expand=True, side=tk.TOP)
        self.root.add(self.up_frame, stretch="always")

        self.middle_frame = scr_win.ScrolledWindow(self.root)
        self.root.add(self.middle_frame, stretch="always")

        self.down_frame = ttk.Frame(self.root,
                                    relief="groove",
                                    borderwidth=2,
                                    height=_height_up_left_window)
        self.down_frame.pack(fill=tk.X, expand=True, side=tk.BOTTOM)
        self.root.add(self.down_frame, stretch="always")

        self.up_frame_interior()
        self.middle_frame_interior()
        self.down_frame_interior()

    def up_frame_interior(self):
        _label = ttk.Label(self.up_frame, text=u"Фильтр")
        _label.pack(side=tk.LEFT, padx=2, pady=2)

        self.up_frame_var_filter = tk.StringVar()
        self._entry = ttk.Entry(self.up_frame, textvariable=self.up_frame_var_filter)
        self.up_frame_var_filter.set(gconfig.get_filter_pattern())  # set filter pattern;

        self._entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2, pady=2)

        _button_ok = ttk.Button(self.up_frame, text='Ok',
                                command=self.up_frame_button_ok_press)
        _button_ok.pack(side=tk.LEFT, expand=False)
        _button_reset = ttk.Button(self.up_frame, text=u'Сброс',
                                   command=self.up_frame_button_reset_press)
        _button_reset.pack(side=tk.RIGHT, expand=False)

    def up_frame_button_ok_press(self):
        self.redraw_middle_frame_interior(file_name_list=self.file_name_list)

    def up_frame_button_reset_press(self):
        # self._entry.insert(0, the_app_config.get_filter_pattern() ) #set filter pattern;
        self.up_frame_var_filter.set(gconfig.get_filter_pattern())  # set filter pattern;

    def middle_frame_interior(self):
        self.file_name_list_listbox = tk.Listbox(self.middle_frame.canvas,
                                                 yscrollcommand=self.middle_frame.vertical_scroll_bar.set,
                                                 width=self.middle_frame.canvas.winfo_reqwidth(),
                                                 height=self.middle_frame.canvas.winfo_reqheight()
                                                 )
        self.file_name_list_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        for i in range(10):
            self.file_name_list_listbox.insert(0, str(i)*i)

    def redraw_middle_frame_interior(self, file_name_list=None):
        if not file_name_list and not file_name_list:
            return
        if file_name_list:
            self.file_name_list = file_name_list

        self.filtered_file_name_list = gconfig.get_filtered_list(self.file_name_list,
                                                                 self._entry.get())
        if not self.filtered_file_name_list:
            tk.messagebox.showwarning("Warning",
                                      "List is empty for " + self._entry.get())
            return

        self.file_name_list_listbox.delete(0, self.file_name_list_listbox.size())
        self.file_name_list_listbox.insert(0, *self.filtered_file_name_list)
        self.middle_frame.update()

    def down_frame_interior(self):
        _button_open = ttk.Button(self.down_frame, text='Open',
                                  command=self.down_frame_button_open_press)
        _button_open.pack(side=tk.RIGHT, expand=False)

    def down_frame_button_open_press(self):
        if not self.file_name_list_listbox.curselection():
            tk.messagebox.showwarning("Warning",
                                      "No file selected. Sorry.")
        # take all selected lines;
        self.selected_file_name_list = \
            [self.file_name_list_listbox.get(i) for i in self.file_name_list_listbox.curselection()]

        store_result = self.ftp.retrive_files(self.selected_file_name_list)
        if store_result[0]:
            tk.messagebox.showwarning("Warning",
                                      "All files saved successfully.")
        else:
            tk.messagebox.showwarning("Warning",
                                      "Error to get file " + store_result[1])
            return

        self.middle_frame.update()

        self.file_works = fw.FileWorks()

        for f in self.selected_file_name_list:
            file_name = os.path.join(gconfig.get_temp_folder(), f)
            result = self.file_works.untar(file_name)
            if not result[0]:
                tk.messagebox.showwarning("Warning",
                                          "Error to unzip file.")
                continue

        r = self.file_works.data_type_selector_run_view(result[1])

