"""

 Copyright 2012 Baidu.com Inc.
 All rights reserved.

 Authors: Peng chong <pengchong@baidu.com>
 Date: 12/05/2012

 This is scs module.

"""

import base64
import urllib
import hashlib
import hmac
import os
import re
import sys
import time
import common
from common_util import error_exit
from common_util import warning
from sample_object import SampleObject
from http_client import *

try:
    import json
except:
    import simplejson as json


class SCSBox:
    def __init__(self, user='', passwd='', httpclient_class=None):
        self.sample_object = SampleObject()
        self.user=user
        self.passwd=passwd

    def _get_auth_header(self, user='', passwd=''):
        if self.user and self.passwd:
            credentials="%s:%s" % (self.user, hashlib.md5(self.passwd).hexdigest())
            auth_header = {"Authorization" : "Basic %s" % base64.encodestring(credentials).strip("\n")}
        else:
            credentials="%s:%s" % (user, hashlib.md5(passwd).hexdigest())
            auth_header = {"Authorization" : "Basic %s" % base64.encodestring(credentials).strip("\n")}
        return auth_header

    def _check_file(self, local_file):
        basename = os.path.basename(local_file)
        if len(basename) != 32:
            error_exit("invalid sample file, sample file should have a md5 name")
        if not os.path.exists(local_file) or os.path.getsize(local_file) == 0:
            error_exit("invalid sample file, not existed or zero size")

    def _check_meta(self, meta):
        if len(str(meta["hash"])) != 32:
            error_exit("invalid hash in meta, hash should have length of 32")
        if str(meta["hashtype"]) not in ["0", "1", "2"]:
            error_exit("invalid hashtype, should be 0/1/2")

    def _check_base_and_meta(self, meta, local_file):
        basename = os.path.basename(local_file)
        file_hash = str(meta["hash"])

        if basename != file_hash:
            warning("base file name %s is not equal to file hash in meta info %s, file is %s" % (
                    basename, file_hash, local_file))
            return 0
        return 1

    @network
    def put_file(self, local_file_path='', file_meta={}, user='', passwd=''):
        """file meta = {
            hash: 'xxx'
            hashtype: 0,1,2
            source: '102',
            FileName: 'sample.exe',
            FilePath : 'c:\sample.exe'
        }
        returns: 0 - failed 1 - succeeded 2 - existed
        """
        self._check_file(local_file_path)
        self._check_meta(file_meta)
        st = self. _check_base_and_meta(file_meta, local_file_path)
        if st == 0:
            return st

        put_status_dict = self.sample_object.put_file(local_file_path,
                                                      file_meta,
                                                      self._get_auth_header(user, passwd))
        status = put_status_dict.get("put_status", 0)
        if status == 0:
            print "%s failed to store" % local_file_path
        elif status == 1:
            print "%s stored to sample cloud" % local_file_path
        elif status == 2:
            print "%s already existed in sample cloud, failed to put" % local_file_path
        elif status == 3:
            print "%s updated to sample cloud" % local_file_path
        return status

    @network
    def stat_file(self, sample_hash, user='', passwd=''):
        """Return status dict.
            stat = {"existed" : 0/1, xxxx, } 0 - not existed 1 -existed
        """
        return self.sample_object.stat_file(sample_hash, self._get_auth_header(user, passwd))

    @network
    def check_sample_existed(self, sample_hash, user='', passwd=''):
        """Return True if sample existed in cloud.
        """
        sample_stat = self.stat_file(sample_hash, user, passwd)
        return True if sample_stat["existed"] == 1 else False

    @network
    def get_to_file(self, sample_hash, local_file, user='', passwd='', instant_mode=False):
        """If the size of local file is zero, it means that
        file is not existed in sample cloud, user should validte
        it with stat_file interface
        False - file size is zero, not existed in sample cloud, check with stat_file
        True - get file from cloud successfully
        """
        r = self.sample_object.get_to_file(sample_hash,
                                       local_file,
                                       self._get_auth_header(user, passwd), instant_mode)
        if os.path.getsize(local_file) != int(r['header']['content-length']):
            return False
        return True

    @network
    def df(self):
        pass
