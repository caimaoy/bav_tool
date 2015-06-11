# -*- coding: UTF-8 -*-

'''
Last modified time: 2015-04-03 09:39:39
Edit time: 2015-04-03 09:39:52
File name: bav_tool.py
Edit by caimaoy
'''

__author__ = 'caimaoy'
__version__ = 'v0.0.1.20150611'
__uuid_name__ = 'bav_test_tool'

import ctypes
import json
import shutil
import os
import re
import subprocess
import sys
import socket
import threading
import time
import urllib
import urllib2
import _winreg

import images_rc

from PyQt4 import QtGui, QtCore
from conf.bav_conf import const
# import requests 我也想用requests啊， 但是32位打包exe后在64有Runtime Error


STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

USER_TOKEN = '33E61AC5272DEE05F75A47818E2BDE98'
# 线下
# USER_TOKEN = 'ca133c2a6566b10e1119699feba3167d'

print_lock = threading.RLock()

import functools

def upload(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # bav_conf.UPLOAD_URL
        # BavLog.info(func.__name__)
        post_context = {}
        post_context['function_name'] = func.__name__
        try:
            f = urllib2.urlopen(
                url=const.UPLOAD_URL,
                data=urllib.urlencode(post_context),
                timeout=2
            )
            a = json.loads(f.read())
            # BavLog.debug(repr(a))
            if a['status'] is not True:
                BavLog.error(repr(a))
        # except Exception as e:
            # BavLog.debug(e)
            # URLError
        except socket.error:
            errno, errstr = sys.exc_info()[:2]
            if errno == socket.timeout:
                BavLog.error(u'网络有点问题...')
        except Exception as e:
            BavLog.error(repr(e))
        return func(*args, **kwargs)
    return wrapper

# 字体颜色定义 ,关键在于颜色编码，由2位十六进制组成，分别取0~f，前一位指的是背景色，后一位指的是字体色
# 由于该函数的限制，应该是只有这16种，可以前景色与背景色组合。也可以几种颜色通过或运算组合，组合后还是在这16种颜色中

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


# reset white
def resetColor():
    # set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)
    set_cmd_text_color(FOREGROUND_GREEN)

###############################################################

# 暗蓝色
# dark blue
def printDarkBlue(mess):
    set_cmd_text_color(FOREGROUND_DARKBLUE)
    sys.stdout.write(mess)
    resetColor()

# 暗绿色
# dark green
def printDarkGreen(mess):
    set_cmd_text_color(FOREGROUND_DARKGREEN)
    sys.stdout.write(mess)
    resetColor()

# 暗天蓝色
# dark sky blue
def printDarkSkyBlue(mess):
    set_cmd_text_color(FOREGROUND_DARKSKYBLUE)
    sys.stdout.write(mess)
    resetColor()

# 暗红色
# dark red
def printDarkRed(mess):
    set_cmd_text_color(FOREGROUND_DARKRED)
    sys.stdout.write(mess)
    resetColor()

# 暗粉红色
# dark pink
def printDarkPink(mess):
    set_cmd_text_color(FOREGROUND_DARKPINK)
    sys.stdout.write(mess)
    resetColor()

# 暗黄色
# dark yellow
def printDarkYellow(mess):
    set_cmd_text_color(FOREGROUND_DARKYELLOW)
    sys.stdout.write(mess)
    resetColor()

# 暗白色
# dark white
def printDarkWhite(mess):
    set_cmd_text_color(FOREGROUND_DARKWHITE)
    sys.stdout.write(mess)
    resetColor()

# 暗灰色
# dark gray
def printDarkGray(mess):
    print_lock.acquire()
    set_cmd_text_color(FOREGROUND_DARKGRAY)
    sys.stdout.write(mess)
    resetColor()
    print_lock.release()

# 蓝色
# blue
def printBlue(mess):
    set_cmd_text_color(FOREGROUND_BLUE)
    sys.stdout.write(mess)
    resetColor()

# 绿色
# green
def printGreen(mess):
    print_lock.acquire()
    set_cmd_text_color(FOREGROUND_GREEN)
    sys.stdout.write(mess)
    resetColor()
    print_lock.release()

# 天蓝色
# sky blue
def printSkyBlue(mess):
    set_cmd_text_color(FOREGROUND_SKYBLUE)
    sys.stdout.write(mess)
    resetColor()

# 红色
# red
def printRed(mess):
    print_lock.acquire()
    set_cmd_text_color(FOREGROUND_RED)
    sys.stdout.write(mess)
    resetColor()
    print_lock.release()

# 粉红色
# pink
def printPink(mess):
    set_cmd_text_color(FOREGROUND_PINK)
    sys.stdout.write(mess)
    resetColor()

# 黄色
# yellow
def printYellow(mess):
    set_cmd_text_color(FOREGROUND_YELLOW)
    sys.stdout.write(mess)
    resetColor()

# 白色
# white
def printWhite(mess):
    set_cmd_text_color(FOREGROUND_WHITE)
    sys.stdout.write(mess)
    resetColor()

##################################################

# 白底黑字
# white bkground and black text
def printWhiteBlack(mess):
    set_cmd_text_color(FOREGROUND_BLACK | BACKGROUND_WHITE)
    sys.stdout.write(mess)
    resetColor()

# 白底黑字
# white bkground and black text
def printWhiteBlack_2(mess):
    set_cmd_text_color(0xf0)
    sys.stdout.write(mess)
    resetColor()


# 黄底蓝字
# white bkground and black text
def printYellowRed(mess):
    set_cmd_text_color(BACKGROUND_YELLOW | FOREGROUND_RED)
    sys.stdout.write(mess)
    resetColor()


def get_current_format_time():
    return time.strftime('[%H:%M:%S] ')


class BavLog(object):
    @staticmethod
    def base_print(func, mess):
        mess = [get_current_format_time(), mess, '\n']
        func(''.join(mess))

    @staticmethod
    def info(mess):
        BavLog.base_print(printGreen, mess)

    @staticmethod
    def debug(mess):
        BavLog.base_print(printDarkGray, mess)

    @staticmethod
    def error(mess):
        BavLog.base_print(printRed, mess)


HOST_PATH = r'C:\Windows\System32\drivers\etc\hosts'
HOST_DIR = os.path.dirname(HOST_PATH)
HOST_BASE_NAME = os.path.basename(HOST_PATH)
BAV_CHECKLIST_URL = r'start chrome http://bav-checklist.readthedocs.org/zh_CN/latest/'
BLACK_SAMPLE_URL = r'start chrome http://172.17.194.10:8088/Share/dujuan02/sample/Virus/Sality.ae/4DF99AE59D4DAB46D5F44E6BC8E80920'
WHITE_SAMPLE_URL = r'start chrome http://172.17.194.10:8088/Share/uTorrent.exe'
BAV_DISPOSE_UPDATE_URL = r'start chrome http://hkg02-sys-web51.hkg02.baidu.com:8080/autoUpdate/auto_deploy_rebuild/index.php?m=Op&a=onlineRules&'
BAV_UPDATE_DOC_URL = r'start chrome http://caimaoy.gitbooks.io/doc_bav/content/'
BAV_ENGINE_SCAN_RESULT = r'start chrome http://wiki.baidu.com/pages/viewpage.action?pageId=96210979'
BAV_ENGINE_TYPE = r'start chrome http://wiki.baidu.com/pages/viewpage.action?pageId=96210921'
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

        print retCode
        print stdout
        print stderr
    return


@upload
def bav_checklist():
    call(BAV_CHECKLIST_URL, False)


@upload
def download_black_sample():
    call(BLACK_SAMPLE_URL, False)


@upload
def download_white_sample():
    call(WHITE_SAMPLE_URL, False)


@upload
def bav_dispose_update_url():
    call(BAV_DISPOSE_UPDATE_URL, False)


@upload
def bav_engine_type_url():
    call(BAV_ENGINE_TYPE, False)


@upload
def bav_engine_scan_result_url():
    call(BAV_ENGINE_SCAN_RESULT, False)


@upload
def bav_update_doc_url():
    call(BAV_UPDATE_DOC_URL, False)


def kill_process(name):
    os.system(r'taskkill /f /im %s' % name)


def start_process(cmd):
    os.system(r'%s' % cmd)


@upload
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
            BavLog.error(repr(e))
        else:
            copy_fail = False

@upload
def backup_hosts():
    backup(HOST_PATH, HOST_PATH)


def cat(path):
    with open(path, 'r') as f:
        for i in f:
            if re.match('^\s*\n$', i):
                continue
            BavLog.info(i.replace('\n', ''))


@upload
def update_hosts():
    return hosts('update_hosts')


@upload
def md5_hosts():
    return hosts('md5_hosts')


@upload
def clean_hosts():
    return hosts('clean')


def hosts(k):
    backup_hosts()
    with open(HOST_PATH, 'w') as f:
        f.write(const.BAV_HOST[k])
    show_hosts()


def is_64_windows():
    return 'PROGRAMFILES(X86)' in os.environ

@upload
def show_hosts():
    BavLog.info('------hosts------- ')
    cat(HOST_PATH)


def open_dir(path):
    cmd = 'explorer.exe /e, /root, "%s\\"' % path
    BavLog.info('open %s' % path)
    call(cmd, shell=False, wait=False)


@upload
def open_hosts_dir():
    open_dir(HOST_DIR)

def get_bav_install_path():
    # TODO add try if not install BAV
    k = _winreg.HKEY_LOCAL_MACHINE
    if is_64_windows():
        sub_k = 'SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Baidu Antivirus'
    else:
        sub_k = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Baidu Antivirus'
    key = _winreg.OpenKey(k, sub_k, 0, _winreg.KEY_READ)
    name = 'InstallDir'
    (bav_install_path, valuetype) = _winreg.QueryValueEx(key, name)
    return bav_install_path


class HostWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(300, 300, 275, 550)
        self.setWindowTitle(u'hosts助手')
        # self.setWindowIcon(QtGui.QIcon('icon/:/images/logo.png'))
        self.setWindowIcon(QtGui.QIcon(':/images/logo.png'))

        self.item_width = 250
        self.item_hight = 30
        lis = [
        {
            'button_name': u'clean_hosts',
            'function': clean_hosts
        },
        {
            'button_name': u'打开hosts目录',
            'function': open_hosts_dir
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
        ]

        self.window_width = self.item_width + 20
        self.window_hight = len(lis) * self.item_hight
        self.setGeometry(300, 300, self.window_width, self.window_hight)

        grid = QtGui.QGridLayout()
        grid.setSpacing(1)

        for index, i in enumerate(lis):
            item = QtGui.QPushButton(i['button_name'])
            self.connect(item, QtCore.SIGNAL('clicked()'), i['function'])
            grid.addWidget(item, index, 0)
        self.setLayout(grid)


class ChecklistWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(300, 300, 275, 550)
        self.setWindowTitle(u'checklist助手')
        self.setWindowIcon(QtGui.QIcon(':/images/logo.png'))

        self.item_width = 250
        self.item_hight = 30
        lis = [
        {
            'button_name': u'Bav_checklist指南',
            'function': bav_checklist
        },
        {
            'button_name': u'chrome下载黑文件',
            'function': download_black_sample
        },
        {
            'button_name': u'chrome下载白文件',
            'function': download_white_sample
        },
        ]

        self.window_width = self.item_width + 20
        self.window_hight = len(lis) * self.item_hight
        self.setGeometry(300, 300, self.window_width, self.window_hight)

        grid = QtGui.QGridLayout()
        grid.setSpacing(1)

        for index, i in enumerate(lis):
            item = QtGui.QPushButton(i['button_name'])
            self.connect(item, QtCore.SIGNAL('clicked()'), i['function'])
            grid.addWidget(item, index, 0)
        self.setLayout(grid)


class Icon(QtGui.QWidget):
    @upload
    def __init__(self, parent=None):
        self.is_64_windows = is_64_windows()

        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(300, 300, 275, 550)
        self.setWindowTitle('Bav_tools %s' % __version__)
        # self.setWindowIcon(QtGui.QIcon('icon/:/images/logo.png'))
        self.setWindowIcon(QtGui.QIcon(':/images/logo.png'))

        '''
        self.connect(quit, QtCore.SIGNAL('clicked()'), QtGui.qApp,
                    QtCore.SLOT('quit()'))
        '''

        self.item_width = 300
        self.item_hight = 30

        self.hosts_widget = HostWidget()
        self.checklist_widget = ChecklistWidget()
        lis = [
        {
            'button_name': u'hosts助手',
            'function': self.hosts_widget.show
        },
        {
            'button_name': u'Bav_checklist助手',
            'function': self.checklist_widget.show
        },
        {
            'button_name': u'打开BAV安装目录',
            'function': self.open_insatll_dir
        },
        {
            'button_name': u'刷新explorer(解决右键，64无效)',
            'function': fresh_explorer
        },
        {
            'button_name': u'备份dump文件夹',
            'function': self.backup_dump
        },
        {
            'button_name': u'下载样本(文件夹自动打开)',
            'function': self.show_download_dialog
        },
        {
            'button_name': u'合并csv文件，得到MD5文件',
            'function': self.show_merge_csv_file
        },
        {
            'button_name': u'通过md5文件下载样本',
            'function': self.download_sample_from_file
        },
        {
            'button_name': u'升级各种文档',
            'function': bav_update_doc_url
        },
        {
            'button_name': u'升级部署URL',
            'function': bav_dispose_update_url
        },
        {
            'button_name': u'引擎掩码',
            'function': bav_engine_type_url
        },
        {
            'button_name': u'引擎扫描结果掩码',
            'function': bav_engine_scan_result_url
        },
        {
            'button_name': u'工具升级',
            'function': tooluploader
        },
        {
            'button_name': u'关于',
            'function': self.show_about
        },
        ]

        self.window_width = self.item_width + 20
        self.window_hight = len(lis) * self.item_hight
        self.setGeometry(300, 300, self.window_width, self.window_hight)

        grid = QtGui.QGridLayout()
        grid.setSpacing(1)

        for index, i in enumerate(lis):
            item = QtGui.QPushButton(i['button_name'])
            item.setGeometry(10, 10 + index*self.item_hight,
                             300, self.item_hight)
            self.connect(item, QtCore.SIGNAL('clicked()'), i['function'])
            grid.addWidget(item, index, 0)
            '''
            quit = QtGui.QPushButton('backup_hosts', self)
            quit.setGeometry(10, 10, 150, 35)
            self.connect(quit, QtCore.SIGNAL('clicked()'), backup_hosts)
            '''
        self.setLayout(grid)
        self.center()

    @upload
    def backup_dump(self):
        bav_install_path = get_bav_install_path()
        BavLog.debug('BAV install dir: %s' % bav_install_path)
        bav_dump_path = os.path.join(bav_install_path, 'dump')
        BavLog.debug('BAV dump dir: %s' % bav_dump_path)
        des_dir = os.path.join(LOCAL_DIR, 'dump')
        backup(bav_dump_path, des_dir)
        cmd = 'explorer.exe /e, /root, "%s\\"' % LOCAL_DIR
        BavLog.info('open %s' % LOCAL_DIR)
        call(cmd, shell=False, wait=False)

    @upload
    def open_insatll_dir(self):
        bav_install_path = get_bav_install_path()
        self.open_dir(bav_install_path)

    @upload
    def open_hosts_dir(self):
        self.open_dir(HOST_DIR)

    def open_dir(self, path):
        open_dir(path)

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) / 2,
            (screen.height() - size.height()) / 2
        )

    def show_download_dialog(self):
        text, ok = QtGui.QInputDialog.getText(
            self,
            u'下载样本',
            u'输入样本MD5:'
        )
        if ok:
            text = str(text)
            try:
                md5 = text.strip().upper()
                # BavLog.debug('md5 is %s'% md5)
            except Exception as e:
                BavLog.error(e)

            import re
            reg_ma5 = r'^[\dABCDEF]{32}$'
            if re.match(reg_ma5, md5):
                download_url = 'http://store.bav.baidu.com/cgi-bin/download_av_sample.cgi?hash=%s' % md5
                c = Downloader(md5, download_url)
                c.start()
                BavLog.debug('download %s' % md5)
            else:
                BavLog.error('md5: %s is wrong' % md5)

    def show_about(self):
        # QMessageBox.about (QWidget parent, QString caption, QString text)
        text_about = u'version: %s.<br />\
                联系我: <a href="mailto:chenyue03@baidu.com">\
                chenyue03@baidu.com</a>'% __version__
        QtGui.QMessageBox.about(self, u'关于',text_about)

        '''About Box.<br />
        This accepts HTML formatting <b> bold</b>'''

    @upload
    def show_merge_csv_file(self):
        def get_csv_data(file_name, row_name):
            import csv
            with open(file_name) as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    yield row[row_name]

        def find_all_hash_in_csv_of_dir(csv_dir):
            md5_list = []
            row_name = 'hash'
            for f in [os.path.join(csv_dir, i) for i in os.listdir(csv_dir)]:
                if f.endswith('.csv'):
                    md5_list = md5_list + list(get_csv_data(f, row_name))
            md5_list = list(set(md5_list))
            with open(os.path.join(csv_dir, 'md5.txt'), 'w') as out_file:
                for i in md5_list:
                    out_file.write(i + '\n')
            open_dir(csv_dir.encode('gbk'))

        dir_path = QtGui.QFileDialog.getExistingDirectory(
            self,
            u'需要合并的cvs文件夹目录',
            './'
        )
        csv_dir = unicode(dir_path)
        if csv_dir:
            BavLog.debug('csv_dir is %s' % csv_dir)
            try:
                find_all_hash_in_csv_of_dir(csv_dir)
            except Exception as e:
                BavLog.error(repr(e))
        else:
            return


    def download_sample_from_file(self):
        md5_file = QtGui.QFileDialog.getOpenFileName(
            self,
            u'请输入md5文件',
            './'
        )
        md5_file = unicode(md5_file)
        if md5_file:
            BavLog.debug('md5_file is %s' % md5_file)
            try:
                d = DownloaderFromFile(md5_file)
                d.start()
            except Exception as e:
                BavLog.error(repr(e))
        else:
            return


class DownloaderFromFile(threading.Thread):
    def __init__(self, md5_file):
        super(DownloaderFromFile, self).__init__()
        self.md5_file = md5_file

    def run(self):
        '''@summary: 重写父类run方法，在线程启动后执行该方法内的代码。
        '''

        from multi_threading_download import download_from_file
        download_from_file(self.md5_file)
        # TODO bug
        # dir_name = os.path.dirname(self.md5_file)
        # open_dir(dir_name.encode('gbk'))


class Downloader(threading.Thread):
    def __init__(self, file_name, download_url):
        super(Downloader, self).__init__()
        self.file_name = file_name
        self.download_url = download_url

    def run(self):
        '''@summary: 重写父类run方法，在线程启动后执行该方法内的代码。
        '''
        ret = download_file(self.file_name, str(self.download_url))
        if ret:
            open_dir(os.path.dirname(os.path.abspath(self.file_name)))


@upload
def download_file(file_name, download_url):
    # TODO del file
    ret = False
    try:
        f = urllib2.urlopen(download_url, timeout=10)
        with open(file_name, 'wb') as code:
            BavLog.debug('download_url is %s' % download_url)
            code.write(f.read())
            BavLog.debug('%s completed' % download_url)
    except socket.error:
        errno, errstr = sys.exc_info()[:2]
        if errno == socket.timeout:
            BavLog.error(u'网络有点问题...')
            try:
                os.remove(file_name)
            except Exception:
                pass
    except Exception as e:
        BavLog.error(repr(e))
    else:
        ret = True
    return ret

from progressbar import *

def tooluploader():
    t = ToolUploader()
    t.start()

# class ToolUploader():
class ToolUploader(threading.Thread):
    def __init__(self, status='buttom'):
        super(ToolUploader, self).__init__()
        self.current_version = __version__
        self.get_last_tool_url = 'http://client.baidu.com:8811/webapi/toolupdate/getLastTool'
        self.last_version_response = None
        # self.last_version_response = self.get_the_last_version_response()
        self.status = status

    def cbk(self, a, b, c):

        '''
        回调函数

        @a: 已经下载的数据块

        @b: 数据块的大小

        @c: 远程文件的大小
        '''

        w=['Progress: ', Percentage(), ' ', Bar(marker=RotatingMarker('>-=')),' ',
        ETA(), ' ', FileTransferSpeed()]
        pbar=ProgressBar(widgets=w, maxval=100).start()

        per = 100.0 * a * b / c
        if per < 100:
            pbar.update(int(per))
        else:
            pbar.update(int(per))
            pbar.finish()

    def update(self, url_file):
        BavLog.info(u'马上下载最新版本工具，请手动替换')
        cmd = 'start %s' % url_file
        call(cmd, False)

    def run(self):
        if self.status == 'buttom':
            self.get_the_last_version()
        elif self.status == 'watch':
            self.watch()

    def get_the_last_version_response(self):
        a = None
        try:
            response = urllib2.urlopen(
                url=self.get_last_tool_url,
                data=urllib.urlencode({'user_token':USER_TOKEN})
            )
            a = json.load(response)
        except Exception as e:
            BavLog.error(repr(e))
        return a

    def need_update(self):
        self.last_version_response = self.get_the_last_version_response()
        ret = False
        reg_success = r'success'
        if (self.last_version_response and
            re.search(reg_success,
                      self.last_version_response.get('msg', None))):
            last_version = self.last_version_response.get('version')
            if last_version == self.current_version:
                ret = False
            else:
                ret = True
        return ret

    @upload
    def get_the_last_version(self):
        if self.need_update():
            BavLog.info(u'您现在不是最新版本')
            self.update(self.last_version_response.get('path'))
        else:
            BavLog.info(u'您已经是最新版本')

    def watch(self):
        if self.need_update():
            BavLog.info(u'您现在不是最新版本, 请点击工具升级进行升级')
        else:
            BavLog.info(u'您已经是最新版本')


if __name__ == '__main__':
    from watch_dir import WatchBAVDumpDir
    w = WatchBAVDumpDir()
    w.start()
    t = ToolUploader('watch')
    t.start()
    app = QtGui.QApplication(sys.argv)
    icon = Icon()
    icon.show()
    sys.exit(app.exec_())
    # http://store.bav.baidu.com/cgi-bin/download_av_sample.cgi?hash=AC7123250F7DEBF509D1EB299CB593F1
