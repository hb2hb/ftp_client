import tarfile
from ftp_client.Config import gconfig
import os
import gzip
import shutil
import dbf


class FileWorks(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FileWorks, cls).__new__(cls)
        return cls.instance

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)

    def untar(self, file_name):
        tar = tarfile.open(file_name, "r:*")
        gzip_name=None

        for name in tar.getnames():
            if name.endswith(gconfig.value_gz):
                gzip_name=name  # get filename that ends with a ".gz";
                break           # jump out;

        if not gzip_name:
            return (False, "")        #error if not present file name with ".gz";

        member = tar.getmember(gzip_name)   #get member by name;
        f = tar.extract(member, path=gconfig.get_temp_folder()) #extract file into temp folder;

        gz_file_name = os.path.join(gconfig.get_temp_folder(), gzip_name)
        out_file_name=gz_file_name[: -len(gconfig.value_gz)]    #drop extention;

        with gzip.open(gz_file_name, 'rb') as f_in:
            with open(out_file_name, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        return (True, out_file_name)
    
    def data_type_selector_run_view(self, full_file_name):
        data_type=gconfig.get_data_type()

        if data_type == gconfig.value_file_type_dbf:
            return self.data_viewer_dbf(full_file_name)
        elif data_type == gconfig.value_file_type_txt:
            return self.data_viewer_txt(full_file_name)
        elif data_type == gconfig.value_file_type_bin:
            return self.data_viewer_bin(full_file_name)

        return False

    def data_viewer_dbf(self, full_file_name):
        table = dbf.Table(full_file_name)
        table.open()
        field_name_list=gconfig.get_field_name_list()
        print("table structure:\n", table.structure())

        try:
            for header, field in field_name_list:
                print(header,":", table[0][field] )
        except:
            print("field: ", field, "not found in file: ", full_file_name)

        #for item in table:

        table.close()

        return True

    def data_viewer_txt(self, full_file_name):
        pass

    def data_viewer_bin(self, full_file_name):
        pass

