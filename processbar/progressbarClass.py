#coding:UTF-8

#Author: zhouws
#2013-02-20 19:59


import os
import sys
import time
import processbar  as progressbar

class progressbarClass: 
    def __init__(self, finalcount=100, progresschar=None):
        self.__pbar = progressbar.ProgressBar(widgets=[progressbar.Percentage(), progressbar.Bar()], maxval=finalcount).start()

    def process(self,i):
        """´Ó1¿ªÊ¼"""
        self.__pbar.update(i)
        if self.__pbar.currval==self.__pbar.maxval:
            self.__pbar.finish()
        return

def test():

    print progressbar.__file__
    pb=progressbarClass(800)

    for count in range(800):
        count+=1
        pb.process(count)
        time.sleep(0.002)
    os.system("pause")

if __name__ == "__main__":
    test()