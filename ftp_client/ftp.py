import tkinter as tk
import ftplib
import ftp_client.Config as cfg
from ftp_client.Config import gconfig
import os


class Ftp(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Ftp, cls).__new__(cls)
        return cls.instance

    def __init__(self, *args, **kwargs) -> object:

        self.ftp_descriptor=None
        self.is_connected=False
        self._ftp=None

        super().__init__(*args, **kwargs)

    def connect(self):
        self.ftp_descriptor = gconfig.get_server_descriptor()

        if not self.ftp_descriptor:
            tk.messagebox.showwarning("Warning",
                                   "The ftp descriptor was not selected")
            self.interior_left_pane.button_connect.configure(state=tk.NORMAL)
            return

        if self.ftp_descriptor[gconfig.key_activity] != gconfig.value_yes:
            tk.messagebox.showwarning("Warning",
                                   "The ftp server is not active. Sorry.")
            self.interior_left_pane.button_connect.configure(state=tk.NORMAL)
            return

        self._ftp=ftplib.FTP()
        try:
            self._ftp.connect(host=self.ftp_descriptor[gconfig.key_ip])
            self._ftp.login(user=self.ftp_descriptor[gconfig.key_login],
                            passwd=self.ftp_descriptor[gconfig.key_psw])

            if self.ftp_descriptor[gconfig.key_mode] == gconfig.value_passive:
                self._ftp.set_pasv(True)

            self._ftp.cwd(self.ftp_descriptor[gconfig.key_folder])
            self.interior_right_pane.redraw_middle_frame_interior( file_name_list=self._ftp.nlst() )

        except:
            tk.messagebox.showwarning("Warning",
                                   "Could not connect to " + self.ftp_descriptor[gconfig.key_ip])
            self.interior_left_pane.button_connect.configure(state=tk.NORMAL)

    def disconnect(self):
        if not self.ftp_descriptor:
            tk.messagebox.showwarning("Warning",
                                   "the connection was not established")
            return
        try:
            self._ftp.quit()
        except:
            tk.messagebox.showwarning("Warning",
                                   "the connection was lost")
        self.ftp_descriptor = None
        # clear listbox at right pane;
        self.interior_right_pane.file_name_list_listbox.delete(0, self.interior_right_pane.file_name_list_listbox.size())

    def retrive_files(self, file_name_list):
        '''
        store files into temp folder;
        :param file_name_list: list of file name;
        :return:    True    - success
                    False   - otherwise
        '''
        global gconfig
        if not file_name_list:
            return (False, gconfig.message_no_files)

        for f in file_name_list:
            try:
                out_file_name = os.path.join(gconfig.get_temp_folder(), f)
                self._ftp.retrbinary("RETR " + f, open(out_file_name, 'wb').write)

            except ftplib.all_errors as e:
                print("ftplib error: "+str(e) )
                return (False, f)

        return (True, "")


    def set_interior_left_pane(self, obj):
        self.interior_left_pane=obj

    def set_interior_right_pane(self, obj):
        self.interior_right_pane = obj


'''
            self.ftp_server=FTP(host=self.ftp_descriptor[cfg.Config.key_ip],
                                user=self.ftp_descriptor[cfg.Config.key_login],
                                passwd=self.ftp_descriptor[cfg.Config.key_psw],
                                acct=self.ftp_descriptor[cfg.Config.key_ip],
                                timeout=None)
'''

the_ftp=Ftp()

