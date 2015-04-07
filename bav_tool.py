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
import sys

from PyQt4 import QtGui, QtCore

from conf import bav_conf




HOST_PATH = r'C:\Windows\System32\drivers\etc\hosts'
HOST_DIR = os.path.dirname(HOST_PATH)
HOST_BASE_NAME = os.path.basename(HOST_PATH)


def backup_hosts():
    backup_name = '_backup'
    backup_num = 0
    copy_fail = True
    while copy_fail:
        backup_num = backup_num + 1
        des_path = ''.join([HOST_PATH, backup_name, str(backup_num)])
        if os.path.exists(des_path):
            continue
        try:
            des_path = ''.join([HOST_PATH, backup_name, str(backup_num)])
            shutil.copy(HOST_PATH, des_path)

        except Exception as e:
            print e
        else:
            copy_fail = False

def cat(path):
    with open(path, 'r') as f:
        for i in f:
            print i


def update_hosts():
    backup_hosts()
    with open(HOST_PATH, 'w') as f:
        f.write(bav_conf.BAV_HOST['update_hosts'])
    cat(HOST_PATH)

class Icon(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(300, 300, 275, 550)
        self.setWindowTitle('Bav_tools')
        self.setWindowIcon(QtGui.QIcon('icon/logo.png'))

        '''
        quit = QtGui.QPushButton('backup_hosts', self)
        quit.setGeometry(10, 10, 150, 35)
        self.connect(quit, QtCore.SIGNAL('clicked()'), backup_hosts)
        '''

        '''
        self.connect(quit, QtCore.SIGNAL('clicked()'), QtGui.qApp,
                    QtCore.SLOT('quit()'))
        '''

        '''
        start = QtGui.QPushButton('update_hosts', self)
        start.setGeometry(10, 50, 150, 80)
        self.connect(start, QtCore.SIGNAL('clicked()'), update_hosts)
        '''

        '''
        fresh = QtGui.QPushButton('Fresh', self)
        fresh.setGeometry(130, 10, 60, 35)
        self.connect(fresh, QtCore.SIGNAL('clicked()'), fresh_explorer)
        self.center()
        '''

        self.item_width = 250
        self.item_hight = 35
        lis = [
        {
            'button_name': u'备份hosts',
            'function': backup_hosts
        },
        {
            'button_name': u'升级hosts',
            'function': update_hosts
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
