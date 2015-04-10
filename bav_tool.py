# -*- coding: UTF-8 -*-

'''
Last modified time: 2015-04-03 09:39:39
Edit time: 2015-04-03 09:39:52
File name: bav_tool.py
Edit by caimaoy
'''

__author__ = 'caimaoy'

import ctypes
import shutil
import os
import subprocess
import sys
import _winreg

from PyQt4 import QtGui, QtCore

from conf import bav_conf


STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

# 字体颜色定义 ,关键在于颜色编码，由2位十六进制组成，分别取0~f，前一位指的是背景色，后一位指的是字体色
#由于该函数的限制，应该是只有这16种，可以前景色与背景色组合。也可以几种颜色通过或运算组合，组合后还是在这16种颜色中

# Windows CMD命令行 字体颜色定义 text colors
FOREGROUND_BLACK = 0x00 # black.
FOREGROUND_DARKBLUE = 0x01 # dark blue.
FOREGROUND_DARKGREEN = 0x02 # dark green.
FOREGROUND_DARKSKYBLUE = 0x03 # dark skyblue.
FOREGROUND_DARKRED = 0x04 # dark red.
FOREGROUND_DARKPINK = 0x05 # dark pink.
FOREGROUND_DARKYELLOW = 0x06 # dark yellow.
FOREGROUND_DARKWHITE = 0x07 # dark white.
FOREGROUND_DARKGRAY = 0x08 # dark gray.
FOREGROUND_BLUE = 0x09 # blue.
FOREGROUND_GREEN = 0x0a # green.
FOREGROUND_SKYBLUE = 0x0b # skyblue.
FOREGROUND_RED = 0x0c # red.
FOREGROUND_PINK = 0x0d # pink.
FOREGROUND_YELLOW = 0x0e # yellow.
FOREGROUND_WHITE = 0x0f # white.


# Windows CMD命令行 背景颜色定义 background colors
BACKGROUND_BLUE = 0x10 # dark blue.
BACKGROUND_GREEN = 0x20 # dark green.
BACKGROUND_DARKSKYBLUE = 0x30 # dark skyblue.
BACKGROUND_DARKRED = 0x40 # dark red.
BACKGROUND_DARKPINK = 0x50 # dark pink.
BACKGROUND_DARKYELLOW = 0x60 # dark yellow.
BACKGROUND_DARKWHITE = 0x70 # dark white.
BACKGROUND_DARKGRAY = 0x80 # dark gray.
BACKGROUND_BLUE = 0x90 # blue.
BACKGROUND_GREEN = 0xa0 # green.
BACKGROUND_SKYBLUE = 0xb0 # skyblue.
BACKGROUND_RED = 0xc0 # red.
BACKGROUND_PINK = 0xd0 # pink.
BACKGROUND_YELLOW = 0xe0 # yellow.
BACKGROUND_WHITE = 0xf0 # white.



# get handle
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

def set_cmd_text_color(color, handle=std_out_handle):
    Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return Bool

#reset white
def resetColor():
    set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)

###############################################################

#暗蓝色
#dark blue
def printDarkBlue(mess):
    set_cmd_text_color(FOREGROUND_DARKBLUE)
    sys.stdout.write(mess)
    resetColor()

#暗绿色
#dark green
def printDarkGreen(mess):
    set_cmd_text_color(FOREGROUND_DARKGREEN)
    sys.stdout.write(mess)
    resetColor()

#暗天蓝色
#dark sky blue
def printDarkSkyBlue(mess):
    set_cmd_text_color(FOREGROUND_DARKSKYBLUE)
    sys.stdout.write(mess)
    resetColor()

#暗红色
#dark red
def printDarkRed(mess):
    set_cmd_text_color(FOREGROUND_DARKRED)
    sys.stdout.write(mess)
    resetColor()

#暗粉红色
#dark pink
def printDarkPink(mess):
    set_cmd_text_color(FOREGROUND_DARKPINK)
    sys.stdout.write(mess)
    resetColor()

#暗黄色
#dark yellow
def printDarkYellow(mess):
    set_cmd_text_color(FOREGROUND_DARKYELLOW)
    sys.stdout.write(mess)
    resetColor()

#暗白色
#dark white
def printDarkWhite(mess):
    set_cmd_text_color(FOREGROUND_DARKWHITE)
    sys.stdout.write(mess)
    resetColor()

#暗灰色
#dark gray
def printDarkGray(mess):
    set_cmd_text_color(FOREGROUND_DARKGRAY)
    sys.stdout.write(mess)
    resetColor()

#蓝色
#blue
def printBlue(mess):
    set_cmd_text_color(FOREGROUND_BLUE)
    sys.stdout.write(mess)
    resetColor()

#绿色
#green
def printGreen(mess):
    set_cmd_text_color(FOREGROUND_GREEN)
    sys.stdout.write(mess)
    resetColor()

#天蓝色
#sky blue
def printSkyBlue(mess):
    set_cmd_text_color(FOREGROUND_SKYBLUE)
    sys.stdout.write(mess)
    resetColor()

#红色
#red
def printRed(mess):
    set_cmd_text_color(FOREGROUND_RED)
    sys.stdout.write(mess)
    resetColor()

#粉红色
#pink
def printPink(mess):
    set_cmd_text_color(FOREGROUND_PINK)
    sys.stdout.write(mess)
    resetColor()

#黄色
#yellow
def printYellow(mess):
    set_cmd_text_color(FOREGROUND_YELLOW)
    sys.stdout.write(mess)
    resetColor()

#白色
#white
def printWhite(mess):
    set_cmd_text_color(FOREGROUND_WHITE)
    sys.stdout.write(mess)
    resetColor()

##################################################

#白底黑字
#white bkground and black text
def printWhiteBlack(mess):
    set_cmd_text_color(FOREGROUND_BLACK | BACKGROUND_WHITE)
    sys.stdout.write(mess)
    resetColor()

#白底黑字
#white bkground and black text
def printWhiteBlack_2(mess):
    set_cmd_text_color(0xf0)
    sys.stdout.write(mess)
    resetColor()


#黄底蓝字
#white bkground and black text
def printYellowRed(mess):
    set_cmd_text_color(BACKGROUND_YELLOW | FOREGROUND_RED)
    sys.stdout.write(mess)
    resetColor()


class BavLog(object):
    @staticmethod
    def info(mess):
        printGreen(mess)

    @staticmethod
    def debug(mess):
        printDarkWhite(mess)

    @staticmethod
    def error(mess):
        printRed(mess)


HOST_PATH = r'C:\Windows\System32\drivers\etc\hosts'
HOST_DIR = os.path.dirname(HOST_PATH)
HOST_BASE_NAME = os.path.basename(HOST_PATH)
BAV_CHECKLIST_URL = r'start chrome http://bav-checklist.readthedocs.org/zh_CN/latest/'
LOCAL_DIR = os.path.dirname(os.path.abspath(__file__))

def call(args, wait=True, shell=True):
    p = subprocess.Popen(args,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=shell
                         )
    if wait:
        retCode = p.wait()
        stdout = p.stdout.read()
        stderr = p.stderr.read()

        '''
        BavLog.debug(retCode)
        BavLog.info(stdout)
        BavLog.error(stderr)
        '''
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
            BavLog.error(e)
        else:
            copy_fail = False


def backup_hosts():
    backup(HOST_PATH, HOST_PATH)


def cat(path):
    with open(path, 'r') as f:
        for i in f:
            BavLog.info(i)


def update_hosts():
    return hosts('update_hosts')


def md5_hosts():
    return hosts('md5_hosts')


def hosts(k):
    backup_hosts()
    with open(HOST_PATH, 'w') as f:
        f.write(bav_conf.BAV_HOST[k])
    show_hosts()


def is_64_windows():
    return 'PROGRAMFILES(X86)' in os.environ

def show_hosts():
    BavLog.info('\nhosts:\n')
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
            'button_name': u'打开BAV安装目录',
            'function': self.open_insatll_dir
        },
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
            'function': self.backup_dump
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
        self.center()

    def get_bav_install_path(self):
        k = _winreg.HKEY_LOCAL_MACHINE
        if self.is_64_windows:
            sub_k = 'SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Baidu Antivirus'
        else:
            sub_k = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Baidu Antivirus'
        key = _winreg.OpenKey(k, sub_k, 0, _winreg.KEY_READ)
        name = 'InstallDir'
        (bav_install_path, valuetype) = _winreg.QueryValueEx(key, name)
        return bav_install_path

        '''
        BavLog.debug('\nBAV install dir:\n%s\n' % bav_install_path)
        bav_dump_path = os.path.join(bav_install_path, 'dump')
        BavLog.debug('\nBAV dump dir:\n%s\n' % bav_dump_path)
        des_dir = os.path.join(LOCAL_DIR, 'dump')
        backup(bav_dump_path, des_dir)
        cmd = 'explorer.exe /e, /root, "%s\\"' % LOCAL_DIR
        BavLog.info('open %s\n'% LOCAL_DIR)
        call(cmd , shell=False, wait=False)
        '''

    def backup_dump(self):
        bav_install_path = self.get_bav_install_path()
        BavLog.debug('\nBAV install dir:\n%s\n' % bav_install_path)
        bav_dump_path = os.path.join(bav_install_path, 'dump')
        BavLog.debug('\nBAV dump dir:\n%s\n' % bav_dump_path)
        des_dir = os.path.join(LOCAL_DIR, 'dump')
        backup(bav_dump_path, des_dir)
        cmd = 'explorer.exe /e, /root, "%s\\"' % LOCAL_DIR
        BavLog.info('open %s\n'% LOCAL_DIR)
        call(cmd , shell=False, wait=False)


    def open_insatll_dir(self):
        bav_install_path = self.get_bav_install_path()
        cmd = 'explorer.exe /e, /root, "%s\\"' % bav_install_path
        BavLog.info('open %s\n'% bav_install_path)
        call(cmd , shell=False, wait=False)

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                 (screen.height() - size.height()) / 2)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    icon = Icon()
    icon.show()
    sys.exit(app.exec_())
