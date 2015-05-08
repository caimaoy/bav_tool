#coding:UTF-8
import time
import os
import sys

#-------------------------------------------------------------------------------
#coding:UTF-8
import os,sys
import subprocess
import re
import time
import urllib2
from scs.scs import SCSBox
import Queue, threading
from threading import Thread
from threading import RLock
import hashlib
import processbar.progressbarClass  as progressbarClass
lock    = RLock()
import logging
from bav_tool import BavLog, upload

def initlog():

    """获取日志句柄"""
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

    hdlr  = logging.FileHandler('runlog.log', "ab")
    hdlr.setLevel(logging.INFO)
    hdlr.setFormatter(formatter)

    hds = logging.StreamHandler()
    hds.setLevel(logging.DEBUG)
    hds.setFormatter(formatter)

    logger = logging.getLogger("123")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(hdlr)
    logger.addHandler(hds)
    return logger

logger  = initlog()

class Worker(Thread):
    worker_count = 0
    sample_count = 0
    def __init__(self, workQueue, downpath, timeout, pb):
        Thread.__init__(self)
        self.id = Worker.worker_count
        Worker.worker_count += 1
        self.setDaemon(True)
        self.workQueue = workQueue
        self.timeout = timeout
        self.downpath = downpath
        self.login()
        self.pb = pb
        self.date = time.strftime('%Y%m%d')

    def getmd5(self, sfile):
        myhash = hashlib.md5()
        f = open(sfile,'rb')
        while True:
            b = f.read(8096)
            if not b :
                break
            myhash.update(b)
        f.close()
        return myhash.hexdigest().upper()

    def login(self):
        self.scsbox = SCSBox("bcollecter", "bavbc1234qwer")

    def downfile(self, md5, download_fullpath):
        nTry = 0
        r = ''
        #tmp_name = download_fullpath + '_'
        download_fullpath = os.path.join(download_fullpath, md5)
        while True:
            try:
                self.scsbox.get_to_file(md5, download_fullpath)
                if self.getmd5(download_fullpath) != md5.upper():
                    logger.info('%s:File Checked Failed' % md5)
                #os.rename(tmp_name, tmp_name + 'OK')
                break
            except Exception as e:
                BavLog.error(repr(e))
                nTry += 1
                if 3 == nTry:
                    logger.info('%s:Download Failed' % md5)
                    break
        lock.acquire()
        Worker.sample_count += 1
        self.pb.process(Worker.sample_count)
        lock.release()

    def getsavepath(self, md5):
        lock.acquire()
        count = Worker.sample_count
        lock.release()
        if count % 1000 == 0:
            #
            self.date = os.path.join(self.downpath, time.strftime('%Y%m%d'))
        sdir = os.path.join(self.date, md5[0])
        if not os.path.isdir(sdir):
            os.makedirs(sdir)
        return os.path.join(sdir, md5)


    def run(self):
        '''  '''
        while True:
            try:
                md5 = self.workQueue.get(timeout=self.timeout)
                #spath = self.getsavepath(md5)
                #self.downfile(md5, spath)
                self.downfile(md5, self.downpath)
            except Queue.Empty:
                break
            except Exception, e:
                pass

class WorkerManager(object):

    def __init__(self, workQueue, downpath, num_of_workers=10, timeout = 1):
        """"""

        self.workQueue = workQueue
        self.workers = []
        self.timeout = timeout
        pb = progressbarClass.progressbarClass(workQueue.qsize())
        self._recruitThreads(num_of_workers, downpath, pb)
        #初始化工作队列

    def _recruitThreads(self, num_of_workers, downpath, pb):
        for num in range(num_of_workers ):
            worker = Worker(self.workQueue, downpath, self.timeout, pb)
            self.workers.append(worker)

    def start(self):
        for work in self.workers:
            work.start()

    def wait_for_complete(self):
        # ...then, wait for each of them to terminate:
        while len(self.workers):
            worker = self.workers.pop()
            worker.join()
            if worker.isAlive() and not self.workQueue.empty():
                self.workers.append(worker)
        BavLog.debug("All jobs are are completed.")


@upload
def download_from_file(file_name):
    workQueue = Queue.Queue()
    f = open(file_name, 'r')
    data = f.read()
    f.close()
    for md5 in data.strip().split('\n'):
        workQueue.put(md5[:32])
    BavLog.debug('File Count:%s' % workQueue.qsize())
    spath = os.path.join(os.getcwd(), 'download')
    if not os.path.isdir(spath):
        os.makedirs(spath)
    WM = WorkerManager(workQueue, spath, 10, 0)   #10个线程,队列超时时间为0S
    WM.start()
    WM.wait_for_complete()
    BavLog.debug('download copleted')
    '''
    from bav_tool import open_dir
    open_dir(os.path.dirname(file_name).encode('gbk'))
    '''

if __name__=='__main__':
    # main()
    pass
