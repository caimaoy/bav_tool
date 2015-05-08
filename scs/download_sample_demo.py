#coding:utf-8
import os, sys
from scs import SCSBox
import logging
import time

def initlog():

    """获取日志句柄"""
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

    hdlr  = logging.FileHandler("Failed.log", "ab")
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

logger = initlog()

class clsGetSample(object):
    
    def __init__(self, sfile, sdown):
        self.filepath = sfile
        self.downpath = sdown
        self.login()
        
    def login(self):
        self.scsbox = SCSBox("store.bav.baidu.com", 80, "bcollecter", "bavbc1234qwer")
        
    def filestat(self, md5):
        #dict = self.scsbox.stat_file(md5)
        #print dict["file_size"]
        #return dict["existed"]
        return True
        
    def getfile(self, md5):
        savepath = os.path.join(self.downpath, md5)
        if self.filestat(md5):
            if self.scsbox.get_to_file(md5, savepath):
                logger.debug("%s-->下载成功." % md5)
            else:
                logger.info("%s-->下载失败." % md5)
        else:
            logger.info("%s-->文件不存在." % md5)

    def DownSample(self):
        f = open(self.filepath, "r")
        data = f.read()
        f.close()
    
        md5lst = data.split("\n")
        nCnt = len(md5lst)
        print "一共%d个文件." % nCnt
        index = 0
        for md5 in md5lst:
            md5 = md5.strip()
            if 32 != len(md5):
                continue
            nTry = 0
            index += 1
            print "%d/%d. MD5:%s" % (index, nCnt, md5)
            while True:
                try:
                    self.getfile(md5)
                    break
                except Exception, e:
                    #print e        #出错信息
                    nTry += 1
                    print "%s:下载出错,重试第%d次." % (md5, nTry)
                    #os.system('pause')
                    #self.login()
                    if 3 == nTry:
                        logger.info("%s-->下载发生错误." % md5)
                        break
            print ""


        
if __name__ == "__main__":
    t1 = time.time();
    if 3 != len(sys.argv):
        print "参数不正确,传递一个需要MD5列表文件 和 样本保存目录\n------------------------------------------------"
        print "默认MD5文件: MD5.txt"
        print "默认下载目录: Down\n------------------------------------------------"
        #Query = raw_input("是否使用默认设置?(Y/N)")
        #if Query.upper() == "Y":
        md5lst = os.path.join(os.getcwd(), "MD5.txt")
        downpath = os.path.join(os.getcwd(), "Down")
    else:
        md5lst = sys.argv[1]
        downpath = sys.argv[2]
        
    if not os.path.exists(md5lst):
        print "MD5.txt文件不存在"
        os.system("pause")
        exit(0)
        
    if not os.path.exists(downpath):
        os.makedirs(downpath)
        
    print "ws"
    for fname in os.listdir(downpath):
        sfile = os.path.join(downpath, fname)
        if os.path.isfile(sfile):
            os.remove(sfile)    #清空目录
    GS = clsGetSample(md5lst, downpath)
    GS.DownSample()
    t2 = time.time();
    print "use time: %f" % (t2-t1)
    os.system("pause");
