# -*- coding: UTF-8 -*-

'''
Last modified time: 2015-05-07 16:54:30
Edit time: 2015-05-07 16:54:40
File name: watch.py
Edit by caimaoy
'''

__author__ = 'caimaoy'


import os
import win32file
import win32con
import shutil
import threading
import time

from bav_tool import get_bav_install_path, BavLog, upload

class WatchBAVDumpDir(threading.Thread):
    def __init__(self):
        super(WatchBAVDumpDir, self).__init__()
        self.bav_install_path = get_bav_install_path()
        self.bav_dump = os.path.join(self.bav_install_path, 'dump')
        self.des_dir = r'c:\bav_dump'
        info = u'此应用会自动监控BAV dump文件夹，帮您捕捉dump, 包括卸载dump'
        BavLog.info(info)

    def run(self):
        u = Upload()
        u.start()
        try:
            os.mkdir(self.des_dir)
        except:
            pass
        ACTIONS = {
            1 : "Created",
            2 : "Deleted",
            3 : "Updated",
            4 : "Renamed from something",
            5 : "Renamed to something"
        }
        # Thanks to Claudio Grondi for the correct set of numbers
        FILE_LIST_DIRECTORY = 0x0001
        hDir = win32file.CreateFile (
            self.bav_dump,
            FILE_LIST_DIRECTORY,
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
            None,
            win32con.OPEN_EXISTING,
            win32con.FILE_FLAG_BACKUP_SEMANTICS,
            None
        )
        while 1:
        #
        # ReadDirectoryChangesW takes a previously-created
        #  handle to a directory, a buffer size for results,
        #  a flag to indicate whether to watch subtrees and
        #  a filter of what changes to notify.
        #
        # NB Tim Juchcinski reports that he needed to up
        #  the buffer size to be sure of picking up all
        #  events when a large number of files were
        #  deleted at once.
        #
            results = win32file.ReadDirectoryChangesW (
                hDir,
                1024,
                True,
                win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                win32con.FILE_NOTIFY_CHANGE_SIZE |
                win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                win32con.FILE_NOTIFY_CHANGE_SECURITY,
                None,
                None
            )
            for action, file in results:
                full_filename = os.path.join(self.bav_dump, file)
                # print full_filename, ACTIONS.get (action, "Unknown")
                end_list = ['dmp', 'txt', 'zip']
                a = ACTIONS.get(action, 'Unknown')
                if a == 'Updated':
                    for e in end_list:
                        if full_filename.endswith(e):
                            BavLog.debug('%s %s' % (full_filename, a))
                            shutil.copyfile(full_filename,
                                            os.path.join(self.des_dir , file))
                            BavLog.error('Please open dir, %s' % self.des_dir)

class Upload(threading.Thread):
    def __init__(self):
        super(Upload, self).__init__()
        self.upload_period = 30*60
        self.start_time = time.time()

    @upload
    def watch_bav_dump_dir(self):
        pass

    def check_upload_time(self):
        delta_time = time.time() - self.start_time
        if delta_time > self.upload_period:
            self.watch_bav_dump_dir()
            self.start_time = time.time()

    def run(self):
        self.watch_bav_dump_dir()
        while True:
            self.check_upload_time()
            time.sleep(1)


if __name__ == '__main__':
    pass
