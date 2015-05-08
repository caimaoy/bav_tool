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

ACTIONS = {
    1 : "Created",
    2 : "Deleted",
    3 : "Updated",
    4 : "Renamed from something",
    5 : "Renamed to something"
}
# Thanks to Claudio Grondi for the correct set of numbers
FILE_LIST_DIRECTORY = 0x0001
# path_to_watch = "."
des_dir = os.path.dirname(__file__)
path_to_watch = r'C:\Program Files\Baidu Security\Baidu Antivirus\5.4.3.124800.0\dump'
hDir = win32file.CreateFile (
    path_to_watch,
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
        full_filename = os.path.join(path_to_watch, file)

        # print full_filename, ACTIONS.get (action, "Unknown")
        end_list = ['dmp', 'txt', 'zip']
        if ACTIONS.get(action, 'Unknown') == 'Updated':
            for e in end_list:
                if full_filename.endswith(e):
                    print 'my: ' + full_filename
                    shutil.copyfile(full_filename, os.path.join(des_dir, file))



if __name__ == '__main__':
    pass
