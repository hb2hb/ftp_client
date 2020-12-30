'''
    created: 2020/10/21
    author: H.B.
'''
from argparse import ArgumentParser
import ftp_client.Application as app
import ftp_client.Config as cfg
from ftp_client.Config import gconfig
import ftp_client.ftp as ftp
from ftp_client.ftp import the_ftp


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", dest="config_file",
                        help="config file name")

    args = parser.parse_args()

    gconfig.read_config_file(config_file=args.config_file)
    the_app = app.Application()
    the_app.run()
