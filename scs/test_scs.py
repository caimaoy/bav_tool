"""

 Copyright 2012 Baidu.com Inc.
 All rights reserved.

 Authors: Peng chong <pengchong@baidu.com>
 Date: 12/05/2012

 This is test module.

"""


from scs import SCSBox


def test_put():
    scsbox = SCSBox()
    scsbox.put_file("/home/xuzeshui/src/bav-cloud/bcs_sample/scs/54D88381B61A3B2EB28942663A98410A",
                    {"hash" : "54D88381B61A3B2EB28942663A98410A",
                     "hashtype" : 1,
                     "source" : "201",
                     "FileName" : "helloworld.txt",
                     "FilePath" : "/home/xuzeshui/src/bav-cloud/bcs_sample/scs"
                     },
                     "wcollecter",
                     "bavwc1234asdf")

def test_put2():
    scsbox = SCSBox()
    scsbox.put_file("/home/xuzeshui/src/bav-cloud/bcs_sample/scs/FF0D8FD026C1DF74D12E2F1FC40992EF",
                    {"hash" : "FF0D8FD026C1DF74D12E2F1FC40992EF",
                     "hashtype" : 1,
                     "source" : "101",
                     "FileName" : "helloworld.txt",
                     "FilePath" : "/home/xuzeshui/src/bav-cloud/bcs_sample/scs"
                     },
                     "wcollecter",
                     "bavwc1234asdf")

def test_put3():
    scsbox = SCSBox()
    scsbox.put_file("/home/xuzeshui/src/bav-cloud/bcs_sample/scs/C27E59D45E9FD16626E8FEF4684F10EB",
                    {"hash" : "C27E59D45E9FD16626E8FEF4684F10EB",
                     "hashtype" : 1,
                     "source" : "101",
                     "FileName" : "helloworld.txt",
                     "FilePath" : "/home/xuzeshui/src/bav-cloud/bcs_sample/scs"
                     },
                     "wcollecter",
                     "bavwc1234asdf")

def test_get():
    scsbox = SCSBox("clientupload", "bavcup2135sadghkj")
    #scsbox = SCSBox("hk01-sd-sample-cache00.hk01.baidu.com", 8000, "clientupload", "bavcup2135sadghkj")
    #scsbox = SCSBox("127.0.0.1", 8080, "clientupload", "bavcup2135sadghkj")
    #print scsbox.get_to_file("94A0F196A28B3FC9FF3E25BCF0D61A51",
    #                   "/home/xuzeshui/src/bav-cloud/bcs_sample/scs/helloworld.txt", instant_mode=False)
    print scsbox.get_to_file("54D88381B61A3B2EB28942663A98410A", "/home/xuzeshui/src/bav-cloud/bcs_sample/scs/54D88381B61A3B2EB28942663A98410A")
    print scsbox.get_to_file("99C6FF852A115420CA6D2BF26BBF071D", "/home/xuzeshui/src/bav-cloud/bcs_sample/scs/99C6FF852A115420CA6D2BF26BBF071D")
    print scsbox.get_to_file("14D88381B61A3B2EB28942663A98410A", "/home/xuzeshui/src/bav-cloud/bcs_sample/scs/14D88381B61A3B2EB28942663A98410A")

def test_stat():
    scsbox = SCSBox("clientupload", "bavcup2135sadghkj")
    #scsbox = SCSBox("hk01-sd-sample-cache00.hk01.baidu.com", 8080, "clientupload", "bavcup2135sadghkj")
    tableindex = int("54D88381B61A3B2EB28942663A98410A".__hash__()) % 16
    print "tableindex", tableindex
    print scsbox.stat_file("54D88381B61A3B2EB28942663A98410A")


def test_sample_existed():
    scsbox = SCSBox("clientupload", "bavcup2135sadghkj")
    print scsbox.check_sample_existed("54D88381B61A3B2EB28942663A98410A")
    print scsbox.check_sample_existed("00000000000000000000000000000000")
    print scsbox.check_sample_existed("0d595d6bfb471b28acb4ddd8f65b54d1")

def test_all():
    scsbox = SCSBox()
    scsbox.put_file("/home/xuzeshui/src/bav-cloud/bcs_sample/scs/54D88381B61A3B2EB28942663A98410A",
                    {"hash" : "54D88381B61A3B2EB28942663A98410A",
                     "hashtype" : 1,
                     "source" : "201",
                     "FileName" : "helloworld.txt",
                     "FilePath" : "/home/xuzeshui/src/bav-cloud/bcs_sample/scs"
                     },
                     "wcollecter",
                     "bavwc1234asdf")
    print scsbox.stat_file("54D88381B61A3B2EB28942663A98410A")
    print scsbox.stat_file("00000000000000000000000000000000")
    if scsbox.check_sample_existed("54D88381B61A3B2EB28942663A98410A"):
        print "put succeeded"
    if scsbox.check_sample_existed("00000000000000000000000000000000") == False:
        print "it is right!"
    if scsbox.get_to_file("54D88381B61A3B2EB28942663A98410A",
                       "/home/xuzeshui/src/bav-cloud/bcs_sample/scs/hello.txt"):
        print "succeeded to get file"
    if scsbox.get_to_file("00000000000000000000000000000000",
                       "/home/xuzeshui/src/bav-cloud/bcs_sample/scs/hello000.txt") == False:
        print "it is right!"


if __name__=="__main__":
    #test_all()
    #test_put()
    #test_put2()
    #test_put3()
    test_sample_existed()
    test_stat()
    #test_get()

