# -*- coding: utf-8 -*-

'''
默认读取md5.txt文件 创建download文件夹，启用多线程下载，我很懒不写命令行
'''

'''
Last modified time: 2014-11-04 16:08:49
Edit time: 2014-11-04 16:10:41
File name: download.py
Edit by caimaoy
'''
import argparse
import os
import threading

import st_log as log

log = log.init_log('log/download')


# 下载命令行 你需要wget 或者也可以换成pytho库自己下载
#command =r'wget -O %s -c store.bav.baidu.com/cgi-bin/download_av_sample.cgi?hash=%s'

# 写明md5的文件
file_name = 'md5.txt'

line = 0
finish_num = 0

# 同步锁 可以不使用
mutex = threading.Lock()

base_path = os.path.dirname(os.path.abspath(__file__))
download_dir = 'download'
download_abs_dir = os.path.join(base_path, download_dir)
abs_filename = os.path.join(base_path, file_name)

wget_path = os.path.join(base_path, 'bin/wget.exe')
wget_argv = '-O %s'
download_url = 'store.bav.baidu.com/cgi-bin/download_av_sample.cgi?hash=%s'

command = ' '.join([wget_path, wget_argv, download_url])


def _create_dir(download_abs_dir):
    if os.path.exists(download_abs_dir):
        pass
    else:
        try:
            os.mkdir(download_abs_dir)
        except Exception as e:
            log.error(e)
            import sys
            sys.exit(0)


def _total_line(file_name):
    global line
    with open(file_name) as f:
        for i in f:
            line = line + 1


def _readline_and_download(md5):
    md5 = md5.split('\n')[0]
    cmd = command % (md5, md5)
    log.debug('cmd is %s...' % cmd)
    os.system(cmd)
    mutex.acquire()
    global finish_num
    finish_num += 1
    log.debug('completed %.2f%%.' % (float(finish_num) / line * 100))
    mutex.release()


def file_download(abs_filename):
    """默认读取md5.txt文件 创建download文件夹，启用多线程下载，我很懒不写命令行
    参数了

    :returns: None

    """

    log.debug('download_dir is %s'% download_abs_dir)
    log.debug('file_name is %s'% os.path.abspath(file_name))

    _create_dir(download_abs_dir)
    _total_line(file_name)
    from multiprocessing.dummy import Pool as ThreadPool

    # 线程池数目，一般来说和cpu的线程数一样就ok了
    threading_num = 9
    pool = ThreadPool(threading_num)

    os.chdir(download_abs_dir)
    log.debug('md5_file is %s'% abs_filename)
    with open(abs_filename) as f:
        pool.map(_readline_and_download, f)

    pool.close()
    pool.join()

def singlenton(cls, *args, **kw):
    '''
    单例类装饰器
    '''
    instances = {}
    def _singlenton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singlenton


@singlenton
class ToolInfo(object):

    def __init__(self):
        self.file_path = __file__
        self.file_dir = os.path.dirname(os.path.abspath(self.file_path))
        self.version = 'v0.0.0.1.20150608'


def download_single_file(md5):
    _create_dir(download_abs_dir)
    os.chdir(download_abs_dir)
    cmd = command % (md5, md5)
    log.debug(cmd)
    os.system(cmd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='bav_download')
    # parser.add_argument('md5_file', help=u'包含MD5的文件', default='md5.txt')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--md5_file', default='md5.txt', help=u'包含md5的文件')
    group.add_argument('-m', '--md5', type=str, help=u'单一的md5')
    group.add_argument('-v', '--version', action='store_true')
    # parser.add_argument('-v', '--verbose', help=u'increse output verbosity', action='store_true')
    args = parser.parse_args()
    version_file = 'version'
    if args.md5:
        download_single_file(args.md5)
    elif args.version:
        print ToolInfo().version
    elif args.md5_file:
        file_download(os.path.abspath(args.md5_file))
    else:
        log.error('args Error')

