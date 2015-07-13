# -*- coding: UTF-8 -*-

'''
Last modified time: 2015-04-03 09:39:39
Edit time: 2015-04-03 09:39:52
File name: bav_tool.py
Edit by caimaoy
'''

__author__ = 'caimaoy'
__version__ = 'v0.0.1.20150713'
__uuid_name__ = 'bav_test_tool'

import codecs
import ctypes
import ConfigParser
import io
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

def upload(function_name=None):
    def _upload(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            f_name = function_name
            if f_name:
                pass
            else:
                f_name = func.__name__
            upload_function_name(f_name)
            return func(*args, **kwargs)
        return wrapper
    return _upload

def upload_function_name(function_name):
    '''
    多线程异步上报函数名调用函数
    '''
    u = UploadFunctionName(function_name)
    u.start()


class UploadFunctionName(threading.Thread):
    '''
    多线程异步上报函数名
    '''
    def __init__(self, upload_function_name):
        super(UploadFunctionName, self).__init__()
        self.upload_function_name = upload_function_name

    def upload(self):
        post_context = {}
        post_context['function_name'] = self.upload_function_name
        try:
            f = urllib2.urlopen(
                url=const.UPLOAD_URL,
                data=urllib.urlencode(post_context),
                timeout=2
            )
            a = json.loads(f.read())
            if a['status'] is not True:
                BavLog.error(repr(a))
        except socket.error:
            errno, errstr = sys.exc_info()[:2]
            if errno == socket.timeout:
                # BavLog.error(u'网络有点问题...')
                pass
        except Exception as e:
            # BavLog.error(repr(e))
            pass

    def run(self):
        self.upload()



def cache(func):
    """缓存装饰器
    """
    caches = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in caches:
            caches[args] = func(*args)
        return caches[args]
    return wrapper


def singleton(cls, *args, **kw):
    '''单例装饰器
    '''
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


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
BAV_CHECKLIST_UPDATE_PACKAGE = r' start chrome ftp://172.17.194.12/bav_tool/BAV_checklist.exe'
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


@upload()
def bav_checklist():
    call(BAV_CHECKLIST_URL, False)


@upload()
def download_black_sample():
    call(BLACK_SAMPLE_URL, False)


@upload()
def download_white_sample():
    call(WHITE_SAMPLE_URL, False)


@upload()
def bav_dispose_update_url():
    call(BAV_DISPOSE_UPDATE_URL, False)


@upload()
def bav_engine_type_url():
    call(BAV_ENGINE_TYPE, False)


@upload()
def bav_engine_scan_result_url():
    call(BAV_ENGINE_SCAN_RESULT, False)


@upload()
def bav_update_doc_url():
    call(BAV_UPDATE_DOC_URL, False)


@upload()
def bav_checklist_update_package():
    call(BAV_CHECKLIST_UPDATE_PACKAGE, False)


@upload()
def del_bavwl_file():
    file_path = get_bav_install_path()
    file_name = 'bavwl.dat'
    file_name = os.path.join(file_path, file_name)
    try:
        os.remove(file_name)
    except WindowsError:
        if os.path.exists(file_name):
            BavLog.error(u'没有安装BAV或者没有停服务')
        else:
            BavLog.info('Success to del bavwl.dat.')
    except Exception as e:
        BavLog.error(repr(e))
    else:
        BavLog.info('Success to del bavwl.dat.')


def kill_process(name):
    os.system(r'taskkill /f /im %s' % name)


def start_process(cmd):
    os.system(r'%s' % cmd)


@upload()
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

@upload()
def backup_hosts():
    backup(HOST_PATH, HOST_PATH)


def cat(path):
    with open(path, 'r') as f:
        for i in f:
            if re.match('^\s*\n$', i):
                continue
            BavLog.info(i.replace('\n', ''))


@upload()
def update_hosts():
    return hosts('update_hosts')


@upload()
def md5_hosts():
    return hosts('md5_hosts')


@upload()
def clean_hosts():
    return hosts('clean')


def hosts(k):
    backup_hosts()
    with open(HOST_PATH, 'w') as f:
        f.write(const.BAV_HOST[k])
    show_hosts()


def is_64_windows():
    return 'PROGRAMFILES(X86)' in os.environ

@upload()
def show_hosts():
    BavLog.info('------hosts------- ')
    cat(HOST_PATH)


def open_dir(path):
    cmd = 'explorer.exe /e, /root, "%s\\"' % path
    BavLog.info('open %s' % path)
    call(cmd, shell=False, wait=False)


@upload()
def open_hosts_dir():
    open_dir(HOST_DIR)

def get_bav_install_path():
    return get_bav_reg_info('InstallDir')

@cache
def get_bav_reg_info(info):
    info_context = ''
    k = _winreg.HKEY_LOCAL_MACHINE
    if is_64_windows():
        sub_k = 'SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Baidu Antivirus'
    else:
        sub_k = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Baidu Antivirus'

    try:
        key = _winreg.OpenKey(k, sub_k, 0, _winreg.KEY_READ)
        (info_context, valuetype) = _winreg.QueryValueEx(key, info)
    except:
        info_context = ''
    return info_context


class ChecklistDownloadProtectHandle(object):
    '''
BLACK_SAMPLE_URL = r'start chrome http://172.17.194.10:8088/Share/dujuan02/sample/Virus/Sality.ae/4DF99AE59D4DAB46D5F44E6BC8E80920'
WHITE_SAMPLE_URL = r'start chrome http://172.17.194.10:8088/Share/uTorrent.exe'
    '''

    def __init__(self, browser, sample_type):

        self.browser = browser.lower()
        self.sample_type = sample_type

        self.browser_name = None
        self.sample_type_name = None
        self.sample_url = None
        self.cmd = r'start %s %s'
        self.cmd_name = u'%s下载%s样本'
        self.upload_name = u'%s_download_%s_sample'
        self.init()

    def init(self):
        if self.browser in ('chrome', 'firefox'):
            self.browser_name = self.browser
        elif self.browser == 'iexplore':
            self.browser_name = 'IE'
        else:
            BavLog.error('BrowserError')


        if self.sample_type == 'black':
            self.sample_type_name = u'黑'
            self.sample_url = r'http://172.17.194.10:8088/Share/dujuan02/sample/Virus/Sality.ae/4DF99AE59D4DAB46D5F44E6BC8E80920'
        elif self.sample_type == 'white':
            self.sample_type_name = u'白'
            self.sample_url = r'http://172.17.194.10:8088/Share/uTorrent.exe'
        else:
            BavLog.error('SampleTypeError')

        self.cmd = self.cmd % (self.browser, self.sample_url)
        self.cmd_name = self.cmd_name % (self.browser_name, self.sample_type_name)
        self.upload_name = self.upload_name % (self.browser, self.sample_type)

    def browser_download(self):
        @upload(self.upload_name)
        def _ret_func():
            call(self.cmd, False)
        return _ret_func



class HostWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(300, 300, 275, 550)
        self.setWindowTitle(u'hosts助手')
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

checcklist_donwload_list = []

def make_browser_download_list():
    browsers = ['chrome', 'firefox', 'iexplore']
    sample_types = ['black', 'white']

    com = [(i, j) for i in browsers for j in sample_types]

    for browser, sample_type in com:
        c = ChecklistDownloadProtectHandle(browser, sample_type)
        dic = {
            'button_name': c.cmd_name,
            'function': c.browser_download()
        }
        checcklist_donwload_list.append(dic)


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
            'button_name': u'Bav_checklist需要覆盖装包下载',
            'function': bav_checklist_update_package
        }
        ]
        make_browser_download_list()
        lis.extend(checcklist_donwload_list)

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
    @upload()
    def __init__(self, parent=None):
        self.is_64_windows = is_64_windows()

        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(300, 300, 275, 550)
        self.setWindowTitle('Bav_tools %s' % __version__)
        self.setWindowIcon(QtGui.QIcon(':/images/logo.png'))

        '''
        self.connect(quit, QtCore.SIGNAL('clicked()'), QtGui.qApp,
                    QtCore.SLOT('quit()'))
        '''

        self.item_width = 300
        self.item_hight = 30

        self.hosts_widget = HostWidget()
        self.checklist_widget = ChecklistWidget()
        self.bav_engine_mask_widget = EngineTypeWeight()
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
            'button_name': u'引擎掩码工具',
            'function': self.bav_engine_mask_widget.show
        },
        {
            'button_name': u'删除二次加速缓存（自行关服务）',
            'function': del_bavwl_file
        },
        {
            'button_name': u'checklist发布版本增量升级（自行关服务）',
            'function': checklist_version_add_update
        },
        {
            'button_name': u'checklist发布版本全量升级（自行关服务）',
            'function': checklist_version_all_update
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
        self.setLayout(grid)
        self.center()

    @upload()
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

    @upload()
    def open_insatll_dir(self):
        bav_install_path = get_bav_install_path()
        self.open_dir(bav_install_path)

    @upload()
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

    @upload()
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


@upload()
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

    @upload()
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


@singleton
class BAVConfig(object):

    def __init__(self):
        self.bav_install_path = get_bav_install_path()
        self.bav_config_file = 'config.ini'
        self.bav_config_file = os.path.join(self.bav_install_path,
                                           self.bav_config_file)

    @property
    def od_engine_type(self):
        return self.get_int_type_in_bav_config_file('EngineOption', 'engineType')

    @property
    def oa_engine_type(self):
        return self.get_int_type_in_bav_config_file('RealTime', 'engineType')

    def get_int_type_in_bav_config_file(self, section, option):
        if os.path.exists(self.bav_config_file):
            cf = ConfigParser.ConfigParser()
            cf.readfp(io.open(self.bav_config_file, 'r', encoding='utf-16'))
            ret = cf.getint(section, option)
            return ret
        else:
            BavLog.info(u'没有安装BAV')
            return 0

    def set(self, section, option, value):
        cfg = ConfigParser.ConfigParser()
        try:
            fp = codecs.open(self.bav_config_file, encoding = 'utf-16le')
            header = fp.read(1)# skip and retrieve the bom header: u'\ufeff'
            cfg.readfp(fp)
            fp.close()

            if not cfg.has_section(section):
                cfg.add_section(section)

            cfg.set(section, option, value)
            fp = codecs.open(self.bav_config_file, mode='wb', encoding='utf-16le')
            fp.write(header) #must accompanying the above header = fp.read(1)
            cfg.write(fp)
            fp.close()
            return 0
        except Exception as e:
            # print sys.exc_info()[0], sys.exc_info()[1]
            BavLog.error(repr(e))
            return -1

    def get(self, section, option):
        cfg = ConfigParser.ConfigParser()
        try:
            fp = codecs.open(self.bav_config_file, encoding='utf-16le')
            fp.read(1)
            cfg.readfp(fp)
            value = cfg.get(section, option)
            fp.close()
            return value
        except Exception as e:
            # print sys.exc_info()[0], sys.exc_info()[1]
            BavLog.error(repr(e))
            return -1


class BAVInfo(object):
    def __init__(self):
        self.bav_install_path = get_bav_install_path()
        self.version_file = 'version.xml'
        self.version_file = os.path.join(
            self.bav_install_path,
            self.version_file
        )
        self.update_dir = 'update'
        self.update_dir = os.path.join(
            self.bav_install_path,
            self.update_dir
        )

        self.program_file_list_file = 'ProgramFileList.xml'
        self.program_file_list_file = os.path.join(
            self.bav_install_path,
            self.program_file_list_file
        )


class BAVChecklistUpdate(BAVInfo):

    def __init__(self):
        super(BAVChecklistUpdate, self).__init__()
        self.bav_config = BAVConfig()
        self.version_pattern = r'\d\.\d\.\d\.\d{1,6}'

    def get_real_version(self):
        '''通过注册表读取真实版本号，注册表被改了咋办，呵呵
        '''
        return get_bav_reg_info('InstallVersion')

    def change_version(self, s, change_type):
        des_version = self._create_version(change_type)
        if re.search(r'ProgramVersion', s):
            s = re.sub(self.version_pattern, des_version, s)
        return s

    def _create_version(self, change_type):
        def repl_add(matched):
            ret = matched.group(1) + '1'
            return ret

        def repl_all(matched):
            ret = [
                matched.group(1),
                '0',
                matched.group(3),
                '1'
            ]
            return ''.join(ret)
        real_version = self.get_real_version()
        replace_funciton = lambda a:a.group(0)
        replace_pattern = r'\d\.\d\.\d\.\d{1,6}'
        if change_type == 'ADD':
            '''增量升级
            '''
            replace_pattern = r'(\d\.\d\.\d\.)(\d{1,6})'
            replace_funciton = repl_add
        elif change_type == 'ALL':
            '''全量升级
            '''
            replace_pattern = r'(\d\.)(\d)(\.\d\.)(\d{1,6})'
            replace_funciton = repl_all
        else:
            BavLog.error('No change_type')
        s = re.sub(replace_pattern, replace_funciton, real_version)
        return s


    upload()
    def change_version_file(self, change_type):
        context = []
        with open(self.version_file) as f:
            for i in f:
                add_context = self.change_version(i, change_type)
                context.append(add_context)
        if context:
            try:
                f = open(self.version_file, 'w')
                f.write(''.join(context))
            except Exception as e:
                BavLog.error(repr(e))
                BavLog.error(u'可能没有关自保')
            else:
                BavLog.info(u'修改version.xml文件成功')
        else:
            BavLog.error(u'修改version.xml文件失败')

    upload()
    def close_bd_engine(self, section, option):
        BD_MASK = 0x00000004L
        bav_config = BAVConfig()
        mask = int(bav_config.get(section, option))

        if mask & BD_MASK:
            mask -= BD_MASK
            bav_config.set(section, option, mask)

    def close_od_bd_engine(self):
        self.close_bd_engine('EngineOption', 'engineType')
        BavLog.info(u'修改od引擎掩码')

    def close_oa_bd_engine(self):
        self.close_bd_engine('RealTime', 'engineType')
        BavLog.info(u'修改oa引擎掩码')


    upload()
    def kill_bav_update_process(self):
        kill_process('bavUpdater.exe')

    def del_update_dir(self):
        try:
            shutil.rmtree(self.update_dir)
        except Exception as e:
            if os.path.exists(self.update_dir):
                BavLog.error(u'可能没有停服务')
                BavLog.error(repr(e))
            else:
                BavLog.info('del update_dir: %s' % self.update_dir)
        else:
            BavLog.info('del update_dir: %s' % self.update_dir)

    upload()
    def modify_program_file_list_file(self):
        # 修改ProgramFileList.xml文件
        context = []
        # <File Name="IEProtect.exe.7z" Size="0x0002ee9a" Time="0x01d0413ecc021465" Md5="0x24777d9e1435f7fd1196d51c2f0d7dc2" DcSize="0x0009a750" DcTime="0x01d0413e9f297085" DcMd5="0x037bafb93c51cf783f9b09c5017efdf1" />
        IE_replace_pattern = r'(.*IEProtect.exe.*Size=")(.{10})(.*DcSize=")(.{10})(.*)'
        version_replace_pattern = r'(.*version.xml.*Size=")(.{10})(.*DcSize=")(.{10})(.*)'
        with open(self.program_file_list_file) as f:
            for i in f:
                add_context = re.sub(IE_replace_pattern, r'\g<1>0x00000001\g<3>0x00000001\g<5>', i)
                add_context = re.sub(version_replace_pattern, r'\g<1>0x00000001\g<3>0x00000001\g<5>', add_context)
                context.append(add_context)
        if context:
            try:
                f = open(self.program_file_list_file, 'w')
                f.write(''.join(context))
            except Exception as e:
                BavLog.error(repr(e))
                BavLog.error(u'可能没有关自保')
            else:
                BavLog.info(u'修改ProgramFileList.xml文件成功')
        else:
            BavLog.error(u'修改ProgramFileList.xml文件失败')

    def set_config_update_connect_time(self):
        '''修改config中update配置
        '''
        bav_config = BAVConfig()
        bav_config.set('update', 'connect_time', 2)
        bav_config.set('update', 'period', 2)
        BavLog.info('set config update connect time')

    upload()
    def open_update_dir(self):
        if os.path.exists(self.update_dir):
            open_dir(self.update_dir)
        else:
            open_dir(get_bav_install_path())

    def self_add_update(self):
        # 修改hosts
        update_hosts()
        # 修改版本号为增量升级版本号
        self.change_version_file('ADD')

        # 关闭小红伞
        self.close_oa_bd_engine()
        self.close_od_bd_engine()

        # kill 升级进程
        self.kill_bav_update_process()

        # del update_dir
        self.del_update_dir()

        # 修改config update connect_time
        self.set_config_update_connect_time()

        # 修改ProgramFileList.xml文件
        self.modify_program_file_list_file()
        kill_process('bav.exe')
        self.open_update_dir()


    def self_all_update(self):
        # 修改hosts
        update_hosts()
        # 修改版本号为增量升级版本号
        self.change_version_file('ALL')

        # 关闭小红伞
        self.close_oa_bd_engine()
        self.close_od_bd_engine()

        # kill 升级进程
        self.kill_bav_update_process()

        # del update_dir
        self.del_update_dir()

        # 修改config update connect_time
        self.set_config_update_connect_time()

        # 修改ProgramFileList.xml文件
        self.modify_program_file_list_file()
        kill_process('bav.exe')
        self.open_update_dir()


class EngineTypeWeight(QtGui.QWidget):
    @upload('engine_type_weight_init')
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle(u'引擎掩码')
        self.setWindowIcon(QtGui.QIcon(':/images/logo.png'))
        self.item_hight = 10

        grid = QtGui.QGridLayout()
        grid.setSpacing(1)
        self.checkboxs = []

        self.engine_mask = QtGui.QLabel(u'引擎掩码(默认OD)：')
        grid.addWidget(self.engine_mask, 0, 0)
        self.engine_mask_edit = QtGui.QLineEdit()
        reg = QtCore.QRegExp(r'\d{0,11}')
        self.engine_mask_edit.setValidator(QtGui.QRegExpValidator(reg,self))
        self.connect(self.engine_mask_edit, QtCore.SIGNAL('textChanged(QString)'), self.set_linetext)
        grid.addWidget(self.engine_mask_edit, 1, 0)
        engine_mask = QtGui.QLabel(u'引擎使用情况：')
        grid.addWidget(engine_mask, 3, 0)

        self.config_mask = BAVConfig().od_engine_type

        for index, i in enumerate(const.ENGINE_TYPE_DICT):

            item = QtGui.QCheckBox(i['note'], self)
            item.setGeometry(10, 10 + index*self.item_hight,
                             300, self.item_hight)
            self.connect(item, QtCore.SIGNAL('stateChanged(int)'),
                        self.totalnum)
            grid.addWidget(item, index + 4, 0) # grid 位置
            self.checkboxs.append((item, i['num']))


        self.reset_od_engine_mask_button = QtGui.QPushButton(u'OD掩码')
        self.connect(self.reset_od_engine_mask_button,
                    QtCore.SIGNAL('clicked()'),
                    self.reset_od)

        # 这里有魔法数字 shit
        grid.addWidget(self.reset_od_engine_mask_button, index + 5, 0)

        self.reset_oa_engine_mask_button = QtGui.QPushButton(u'OA掩码')
        self.connect(self.reset_oa_engine_mask_button,
                    QtCore.SIGNAL('clicked()'),
                    self.reset_oa)

        # 这里有魔法数字 shit
        grid.addWidget(self.reset_oa_engine_mask_button, index + 6, 0)

        self.setLayout(grid)
        self.set_check_box(self.config_mask)


    def set_check_box(self, value):
        for item, num in self.checkboxs:
            if value & num:
                item.setChecked(True)
            else:
                item.setChecked(False)


    def set_linetext(self, value):
        for item, num in self.checkboxs:
            item.stateChanged.disconnect()
        text = str(self.engine_mask_edit.text())
        try:
            value = int(text)
            self.set_check_box(value)
        except ValueError:
            self.set_check_box(0)
        for item, num in self.checkboxs:
            self.connect(item, QtCore.SIGNAL('stateChanged(int)'),
                        self.totalnum)

    def totalnum(self):
        num = 0
        for a, b in self.checkboxs:
            if a.isChecked():
                num += b
        self.engine_mask_edit.setText(str(num))

    def reset_mask(self, value):
        for item, num in self.checkboxs:
            item.stateChanged.disconnect()
        try:
            self.set_check_box(value)
        except ValueError:
            self.set_check_box(0)
        for item, num in self.checkboxs:
            self.connect(item, QtCore.SIGNAL('stateChanged(int)'),
                        self.totalnum)
        self.engine_mask_edit.setText(str(value))

    @upload()
    def reset_oa(self):
        oa = BAVConfig().oa_engine_type
        self.reset_mask(oa)

    @upload()
    def reset_od(self):
        od = BAVConfig().od_engine_type
        self.reset_mask(od)

@upload()
def checklist_version_add_update():
    b = BAVChecklistUpdate()
    b.self_add_update()

@upload()
def checklist_version_all_update():
    b = BAVChecklistUpdate()
    b.self_all_update()


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
