import tkinter as tk
from tkinter import ttk
import ftp_client.ScrolledWindow as scr_win


class Interior(object):
    '''
    structure of descriptor:
    (<root>             -- mandatory field;
    <item type>,        -- mandatory field;
    <content string>,   -- mandatory field;
    <press_function>    -- arbitrary field;
    )
    '''

    label_type='Label'
    button_type='Button'
    def __init__(self, root, *args, **kwargs):
        self.root=root
        self.the_app=None
        super().__init__()
        self.initContainer(*args, **kwargs)

    def initContainer(self):
        pass

    def set_application_reference(self, app):
        self.the_app=app

    def get_application_reference(self):
        return self.the_app

    def add_widgets(self):
        pass

