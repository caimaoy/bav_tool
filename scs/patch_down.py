"""

 Copyright 2012 Baidu.com Inc.
 All rights reserved.

 Authors: Peng chong <pengchong@baidu.com>
 Date: 12/05/2012

 This is test module.

"""


from scs import SCSBox


def test_put():
    scsbox = SCSBox("store.bav.baidu.com", 8080)
    scsbox.put_file("/home/pengchong/src/ws/server/sample_cloud_sdk/scs/A02EEEB7601FEDD4EE6323A02087919B",
                    {"hash" : "A02EEEB7601FEDD4EE6323A02087919B",
                     "hashtype" : 1,
                     "source" : "0",
                     "FileName" : "",
                     "FilePath" : ""
                     },
                     "wcollecter",
                     "bavwc1234asdf")

def test_get():
    scsbox = SCSBox("store.bav.baidu.com", 8080, "clientupload", "bavcup2135sadghkj")

    for md5 in open("md5_list_existed", "r"):
        md5_name = md5.strip()
        try:
            scsbox.get_to_file(md5_name,
                               "/home/pengchong/src/ws/server/sample_cloud_sdk/scs/vault/%s" % md5_name)
            print "%s fin" % md5_name
        except Exception, e:
            print "%s------> not ok" % md5_name
            print str(e)


def test_stat():
    scsbox = SCSBox("store.bav.baidu.com", 8080, "clientupload", "bavcup2135sadghkj")

    for md5 in open("md5_list", "r"):
        md5_name = md5.strip()
        try:
            print scsbox.stat_file(md5_name)
            print "%s fin" % md5_name
        except Exception, e:
            print "%s------> not ok" % md5_name
            print str(e)
    print scsbox.stat_file("A02EEEB7601FEDD4EE6323A02087919B")

def test_sample_existed():
    scsbox = SCSBox("store.bav.baidu.com", 8080)
    print scsbox.check_sample_existed("00000072E6E3C20F4D10F68DEEFA6BFB")
    print scsbox.check_sample_existed("00000000000000000000000000000000")

def test_all():
    scsbox = SCSBox("store.bav.baidu.com", 8080)
    scsbox.put_file("/home/pengchong/src/ws/server/sample_cloud_sdk/scs/00000072E6E3C20F4D10F68DEEFA6BFB",
                    {"hash" : "00000072E6E3C20F4D10F68DEEFA6BFB",
                      "hashtype" : 1,
                     "source" : "101",
                     "FileName" : "sample.exe",
                     "FilePath" : "c:\sample.exe"
                     })
    print scsbox.stat_file("00000072E6E3C20F4D10F68DEEFA6BFB")
    print scsbox.stat_file("00000000000000000000000000000000")
    if scsbox.check_sample_existed("00000072E6E3C20F4D10F68DEEFA6BFB"):
        print "put succeeded"
    if scsbox.check_sample_existed("00000000000000000000000000000000") == False:
        print "it is right!"
    if scsbox.get_to_file("00000072E6E3C20F4D10F68DEEFA6BFB",
                       "/home/pengchong/src/ws/server/sample_cloud_sdk/scs/local_sample"):
        print "succeeded to get file"
    if scsbox.get_to_file("00000000000000000000000000000000",
                       "/home/pengchong/src/ws/server/sample_cloud_sdk/scs/local_sample_000") == False:
        print "it is right!"

    status = scsbox.put_file("/home/pengchong/src/ws/server/sample_cloud_sdk/scs/00000072E6E3C20F4D10F68DEEFA6BFB",
                    {"hash" : "00000072E6E3C20F4D10F68DEEFA6BFB",
                      "hashtype" : 1,
                     "source" : "101",
                     "FileName" : "sample.exe",
                     "FilePath" : "c:\sample.exe"
                     })
    if status == 2:
        print "it is right!"

if __name__=="__main__":
    test_get()

