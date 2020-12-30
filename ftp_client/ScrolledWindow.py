import tkinter as tk
from tkinter import ttk

class ScrolledWindow(ttk.Frame):
    def __init__(self, root, *args, inner_frame=None, **kwargs):
        self.root=root
        self.inner_frame=inner_frame

        super().__init__(self.root, *args, **kwargs)

        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.vertical_scroll_bar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.vertical_scroll_bar.pack(fill=tk.Y, side=tk.RIGHT, expand=False)

        self.horizonyal_scroll_bar = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.horizonyal_scroll_bar.pack(fill=tk.X, side=tk.BOTTOM, expand=False)

        self.update()
        self.canvas = tk.Canvas(self, bd=0,
                                highlightthickness=0,
                                relief = 'groove',
                                yscrollcommand=self.vertical_scroll_bar.set,
                                xscrollcommand=self.horizonyal_scroll_bar.set,
                                width=self.winfo_width(),
                                height=self.winfo_height())

        self.canvas.configure(yscrollincrement='6', xscrollincrement='6')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.vertical_scroll_bar.config(command=self.canvas.yview)
        self.horizonyal_scroll_bar.config(command=self.canvas.xview)

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        self.canvas.update()
        # create a frame inside the canvas which will be scrolled with it
        self.inner_frame = tk.Frame(self.canvas,
                                    width=self.winfo_reqwidth(),
                                    height=self.winfo_reqheight())
        self.inner_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.inner_frame.update()

        self.canvas.create_window(0, 0, window=self.inner_frame,
                                  anchor=tk.NW)

        self.vertical_scroll_bar.lift(self.inner_frame)
        self.horizonyal_scroll_bar.lift(self.inner_frame)

        self.inner_frame.bind('<Configure>', self._configure_inner_frame)
        self.inner_frame.bind('<Enter>', self._bound_to_mousewheel)
        self.inner_frame.bind('<Leave>', self._unbound_to_mousewheel)

        self.update()

    def _bound_to_mousewheel(self, event):
        #        self.canvas.bind("<MouseWheel>", self._on_mousewheel_vertical)
        self.canvas.bind_all('<Button-4>', lambda event: self._on_mousewheel_vertical(event))
        self.canvas.bind_all('<Button-5>', lambda event: self._on_mousewheel_vertical(event))
        self.canvas.bind_all('<Control-Button-4>', lambda event: self._on_mousewheel_horizontal(event))
        self.canvas.bind_all('<Control-Button-5>', lambda event: self._on_mousewheel_horizontal(event))

    def _unbound_to_mousewheel(self, event):
        #        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")
        self.canvas.unbind_all("<Control-Button-4>")
        self.canvas.unbind_all("<Control-Button-5>")

    def _on_mousewheel_vertical(self, event):
        direction = 0

        if event.num == 5 or event.delta == -120:
            direction = 1

        if event.num == 4 or event.delta == 120:
            direction = -1

        self.canvas.yview_scroll(direction, tk.UNITS)
    #        event.widget.yview_scroll(direction, tk.UNITS)

    def _on_mousewheel_horizontal(self, event):
        direction = 0

        if event.num == 5 or event.delta == -120:
            direction = 1

        if event.num == 4 or event.delta == 120:
            direction = -1

        self.canvas.xview_scroll(direction, tk.UNITS)
    #        event.widget.xview_scroll(direction, tk.UNITS)

    def _configure_inner_frame(self, event):
        #self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
        #print(self.canvas.bbox(tk.ALL))    #for debug only;
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

        if self.inner_frame.winfo_reqwidth() != self.canvas.winfo_width():
            # update the canvas width to fit the inner frame
            self.canvas.config(width = self.inner_frame.winfo_reqwidth())

        if self.inner_frame.winfo_reqheight() != self.canvas.winfo_height():
            # update the canvas width to fit the inner frame
            self.canvas.config(height = self.inner_frame.winfo_reqheight())

