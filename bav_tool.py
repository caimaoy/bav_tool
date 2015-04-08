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
import subprocess
import sys
import _winreg

from PyQt4 import QtGui, QtCore

from conf import bav_conf

HOST_PATH = r'C:\Windows\System32\drivers\etc\hosts'
HOST_DIR = os.path.dirname(HOST_PATH)
HOST_BASE_NAME = os.path.basename(HOST_PATH)
BAV_CHECKLIST_URL = r'start chrome http://bav-checklist.readthedocs.org/zh_CN/latest/'
LOCAL_DIR = os.path.dirname(os.path.abspath(__file__))

def call(args, wait=True):
    p = subprocess.Popen(args,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True
                         )
    if wait:
        retCode = p.wait()
        stdout = p.stdout.read()
        stderr = p.stderr.read()

        print retCode
        print stdout

    return


def bav_checklist():
    call(BAV_CHECKLIST_URL, False)


def kill_process(name):
    os.system(r'taskkill /f /im %s' % name)


def start_process(cmd):
    os.system(r'%s' % cmd)


def fresh_explorer():
    kill_process('explorer.exe')
    call('start explorer', False)


def backup(src, des, backup_name='_backup'):
    backup_name = '_backup'
    backup_num = 0
    copy_fail = True
    while copy_fail:
        backup_num = backup_num + 1
        des_path = ''.join([des, backup_name, str(backup_num)])
        if os.path.exists(des_path):
            continue
        try:
            if os.path.isfile(src):
                shutil.copy(src, des_path)
            elif os.path.isdir(src):
                shutil.copytree(src, des_path)

        except Exception as e:
            print e
        else:
            copy_fail = False


def backup_hosts():
    backup(HOST_PATH, HOST_PATH)


def cat(path):
    with open(path, 'r') as f:
        for i in f:
            print i


def update_hosts():
    return hosts('update_hosts')


def md5_hosts():
    return hosts('md5_hosts')


def hosts(k):
    backup_hosts()
    with open(HOST_PATH, 'w') as f:
        f.write(bav_conf.BAV_HOST[k])
    cat(HOST_PATH)


def is_64_windows():
    return 'PROGRAMFILES(X86)' in os.environ

def show_hosts():
    cat(HOST_PATH)


class Icon(QtGui.QWidget):
    def __init__(self, parent=None):
        self.is_64_windows = is_64_windows()

        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(300, 300, 275, 550)
        self.setWindowTitle('Bav_tools')
        self.setWindowIcon(QtGui.QIcon('icon/logo.png'))

        '''
        self.connect(quit, QtCore.SIGNAL('clicked()'), QtGui.qApp,
                    QtCore.SLOT('quit()'))
        '''

        self.item_width = 250
        self.item_hight = 35
        lis = [
        {
            'button_name': u'备份hosts',
            'function': backup_hosts
        },
        {
            'button_name': u'show_hosts',
            'function': show_hosts
        },
        {
            'button_name': u'升级hosts',
            'function': update_hosts
        },
        {
            'button_name': u'线下云查hosts',
            'function': md5_hosts
        },
        {
            'button_name': u'Bav_checklist指南',
            'function': bav_checklist
        },
        {
            'button_name': u'刷新explorer(解决右键，64无效)',
            'function': fresh_explorer
        },
        {
            'button_name': u'备份dump文件夹',
            'function': self.get_bav_install_path
        },
        ]
        self.window_width = self.item_width + 20
        self.window_hight = len(lis) * self.item_hight + 20
        self.setGeometry(300, 300, self.window_width, self.window_hight)

        for index, i in enumerate(lis):
            item = QtGui.QPushButton(i['button_name'], self)
            item.setGeometry(10, 10 + index*self.item_hight,
            250, self.item_hight )
            self.connect(item, QtCore.SIGNAL('clicked()'), i['function'])
            '''
            quit = QtGui.QPushButton('backup_hosts', self)
            quit.setGeometry(10, 10, 150, 35)
            self.connect(quit, QtCore.SIGNAL('clicked()'), backup_hosts)
            '''

    def get_bav_install_path(self):
        k = _winreg.HKEY_LOCAL_MACHINE
        if self.is_64_windows:
            sub_k = 'SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Baidu Antivirus'
        else:
            sub_k = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Baidu Antivirus'
        key = _winreg.OpenKey(k, sub_k, 0, _winreg.KEY_READ)
        name = 'InstallDir'
        (bav_install_path, valuetype) = _winreg.QueryValueEx(key, name)
        print bav_install_path
        bav_dump_path = os.path.join(bav_install_path, 'dump')
        print bav_dump_path
        des_dir = os.path.join(LOCAL_DIR, 'dump')
        backup(bav_dump_path, des_dir)

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                 (screen.height() - size.height()) / 2)


if __name__ == '__main__':
    # backup_host()
    # print bav_conf.BAV_HOST
    app = QtGui.QApplication(sys.argv)
    icon = Icon()
    icon.show()
    sys.exit(app.exec_())
