'''
this module exporting the_app_config - golobal configure object;
'''
import json
import datetime

class Config(object):
    key_project = "project"
    key_servers = "servers"
    key_ip = "ip"
    key_name = "name"
    key_login = "login"
    key_psw = "psw"
    key_mode='mode'
    key_activity="activity"
    key_temp_folder="temp_folder"

    key_data_descriptor="data_descriptor"
    key_data_type="data_type"
    key_separator="separator"
    key_fields="fields"
    key_field_data=u"ДАТА"
    key_field_time=u"ВРЕМЯ"
    key_field_abonent=u"АБОНЕНТ"
    key_field_abonent2=u"АБОНЕНТ2"
    key_field_duration=u"ДЛИТЕЛЬНОСТЬ"
    key_field_trank_in=u"ТРАНК_ВХ"
    key_field_trank_out=u"ТРАНК_ИСХ"
    key_folder='folder'

    key_field_alias='alias'
    key_field_name='name'
    key_field_type='type'
    key_field_size='size'
    key_field_value='value'

    value_field_type_char='C'
    value_field_type_numeric='N'
    value_field_type_date='D'

    value_file_type_dbf='dbf'
    value_file_type_txt = 'txt'
    value_file_type_bin = 'bin'

    value_passive='passive'
    value_yes="yes"
    value_no="no"
    value_servers=u'Серверы'
    value_observer=u'Обозреватель'
    value_gz='.gz'

    value_field_name_dbf_date='DATE'
    value_field_name_dbf_time='TIME'
    value_field_name_dbf_abonent_a='ABONENT'
    value_field_name_dbf_abonent_b = 'ABONENT2'
    value_field_name_dbf_tlk_sec='TALK_SEC'
    value_field_name_dbf_trunk_in='TRUNK_IN'
    value_field_name_dbf_trunk_out = 'TRUNK_OUT'

    msg_empty_folder=u'папка пуста'

    key_file_name_format = "file_name_format"
    key_y4 = 'yyyy'
    key_y2 = 'yy'
    key_mm = 'mm'
    key_dd = 'dd'
    y2mmdd = 'yymmdd'
    y4mmdd = 'yyyymmdd'

    message_no_files="no files."

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance

    def __init__(self, *arg, config_file=None, **kwargs):
        """

        :type config_file: String
        """
        self.config_file = config_file
        self.configure = None
        self.read_config_file()
        self.ftp_descriptor=None
        self.field_descriptor= {
            Config.key_field_alias : None,
            Config.key_field_name : None,
            Config.key_field_type : None,
            Config.key_field_size : None
        }
        self.record_descriptor = None

        super().__init__(*arg, **kwargs)

    def read_config_file(self, config_file=None):
        if config_file:
            self.config_file = config_file
        if self.config_file:
            # read config file;
            with open(self.config_file, 'r') as cf:
                c = cf.read()
                self.configure = json.loads(c)
            self.get_server_name_list()  # build server name list;

    def set_default_value(self):
        pass

    def get_min_size_width(self):
        return 300
        # return self.conf["min_size_width"]

    def get_min_size_height(self):
        return 200
        # return self.conf["min_size_height"]

    def get_date_format(self, pattern):
        pass

    def get_server_name_list(self):
        self.server_name_list = list()
        for s in self.configure[Config.key_servers]:

            #select only for activity is yes:
            if s[Config.key_activity] == Config.value_yes:
                self.server_name_list.append(s[Config.key_name])

    def get_server_by_name(self, name):
        for s in self.configure[Config.key_servers]:
            if s[Config.key_name] == name:
                return s
        return None

    def set_server_descriptor(self, name):
        self.ftp_descriptor=self.get_server_by_name(name)

    def get_server_descriptor(self):
        return self.ftp_descriptor

    def get_filter_pattern(self):
        return "_"+datetime.date.today().strftime('%Y')+datetime.date.today().strftime('%m')

    def get_file_name_pattern(self, file_name_pattern):
        mm = datetime.date.today().strftime('%m')
        result_pattern=file_name_pattern
        result_pattern.replace(Config.key_mm, mm)

        if file_name_pattern.find(Config.key_y4)<0:
            y2=datetime.date.today().strftime('%y')      #year format: yy
            result_pattern.replace(Config.key_y2, y2)
        else:
            y4=datetime.date.today().strftime('%Y')      #year format: yyyy
            result_pattern.replace(Config.key_y4, y4)

        return result_pattern

    def get_filtered_list(self, source_list, file_name_pattern):
        result_list=list()
        for s in source_list:
            if s.find(file_name_pattern) >= 0:
                result_list.append(s)

        return result_list

    def get_project_config(self):
        return self.configure[Config.key_project]

    def get_temp_folder(self):
        return self.get_project_config()[Config.key_temp_folder]

    def get_data_descriptor(self):
        return self.ftp_descriptor[Config.key_data_descriptor]

    def get_data_type(self):
        return self.get_data_descriptor()[Config.key_data_type]

    def get_field_name_list(self):
        field_name_list=list()
        for n in self.get_data_descriptor()[Config.key_fields]:
            if type( n[1] ) is int:
                if n[1] < 0:
                    continue

            field_header_name = n[0], n[1]
            field_name_list.append( field_header_name )

        return field_name_list

    def get_record_descriptor(self):
        return self.record_descriptor

    def is_field_name_valid(self, field_name_list):
        for _alias, _name in self.get_field_name_list():
            for f in field_name_list:
                field_name, field_type = f.split()
                if field_name == _name:
                    return (_alias, _name, field_type)
            return None     #return None if no match found;


    def set_record_descriptor(self, field_name_list, record_value):
        self.field_descriptor_list=list()
        self.field_descriptor= {
            Config.key_field_alias : None,
            Config.key_field_name : None,
            Config.key_field_type : None,
            Config.key_field_size : None
        }


gconfig = Config()

'''
from datetime import date

datetime.date.today().strftime('%Y-%m-%d')
datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# dd/mm/YY
d1 = today.strftime("%d/%m/%Y")
print("d1 =", d1)

# Textual month, day and year	
d2 = today.strftime("%B %d, %Y")
print("d2 =", d2)

# mm/dd/y
d3 = today.strftime("%m/%d/%y")
print("d3 =", d3)

# Month abbreviation, day and year	
d4 = today.strftime("%b-%d-%Y")
print("d4 =", d4)
'''
