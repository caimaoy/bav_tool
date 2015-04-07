# -*- coding: UTF-8 -*-

'''
Last modified time: 2015-04-03 09:39:39
Edit time: 2015-04-03 09:39:52
File name: bav_tool.py
Edit by caimaoy
'''

__author__ = 'caimaoy'

import shutil
import os


HOST_PATH = r'C:\Windows\System32\drivers\etc\hosts'
HOST_DIR = os.path.dirname(HOST_PATH)
HOST_BASE_NAME = os.path.basename(HOST_PATH)


def backup_host():
    backup_name = '_backup'
    backup_num = 0
    copy_fail = True
    while copy_fail:
        backup_num = backup_num + 1
        try:
            des_path = ''.join([HOST_PATH, backup_name, str(backup_num)])
            shutil.copy(HOST_PATH, des_path)

        except Exception as e:
            print e
        else:
            copy_fail = False


if __name__ == '__main__':
    backup_host()
