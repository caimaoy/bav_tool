"""

 Copyright 2012 Baidu.com Inc.
 All rights reserved.

 Authors: Peng chong <pengchong@baidu.com>
 Date: 12/05/2012

 This is sample object module.

"""


import os
import urllib
import json
import version
from common_exception import NameException
from http_client import *


class SampleObject:
    def __init__(self, object_name="AV Sample Cloud"):
        self._upload_host = "upload.bav.baidu.com"
        self._store_host = "store.bav.baidu.com"
        self.object_name = object_name
        self.c = select_best_http_client()

        self.default_headers = {
                "Host": self._store_host,
                "Accept" : "text/plain,application/octet-stream",
                "User-Agent": "SCSBox %s" % version.__version__,
                "Authorization" : "Basic "
        }

        self.default_put_headers = {
                "Host": self._upload_host,
                "User-Agent": "SCSBox %s" % version.__version__,
                "Authorization" : "Basic "
        }

        self.put_cgi = "cgi-bin/upload_av_sample.cgi"

        self.get_cgi = "cgi-bin/download_av_sample.cgi"
        self.get_url_pre = "http://%s/%s" % (self._store_host, self.get_cgi)

        self.get_cgi_with_two_get = "cgi-bin/download_av_sample_re.cgi"
        self.get_url_pre_with_two_get = "http://%s/%s" % (self._store_host, self.get_cgi_with_two_get)

        self.stat_cgi = "cgi-bin/stat_av_sample.cgi"
        self.stat_url_pre = "http://%s/%s" % (self._store_host, self.stat_cgi)

        self.feedback_cgi = "cgi-bin/feedback_av_sample.cgi"
        self.feedback_url_pre = "http://%s/%s" % (self._store_host, self.feedback_cgi)

        self.hostname_cgi = "cgi-bin/hostname.cgi"
        self.hostname_url_pre = "http://%s/%s" % (self._store_host, self.hostname_cgi)


    def __str__(self):
        return '%s/%s' % ("", self.object_name)

    def ref_str(self):
        return '%s/%s' % ('av sample cloud:/',self.object_name)

    def assert_file_writeable(self, path):
        if os.path.isdir(path):
            raise FileSystemException(path + ' is not a file')

    def handle_response(self, response, restful_action=None):
        """returns tuple to user. """
        try:
            resp_body = response["body"]
            if restful_action in ["PUT", "GET", "POST"]:
                resp = eval(resp_body)
                return resp
            return True
        except Exception, e:
            print response
            print str(e)

    @network
    def put(self, content, headers={}):
        r = self.c.put(self.put_url, content, headers)
        return self.handle_response(r)

    def _update_headers(self, headers):
        headers_ref = {}
        headers_ref.update(self.default_headers)
        headers_ref.update(headers)
        return headers_ref

    def _update_put_headers(self, headers):
        headers_ref = {}
        headers_ref.update(self.default_put_headers)
        headers_ref.update(headers)
        return headers_ref

    @network
    def get_upload_host(self, headers={}):
        try:
            r = self.c.get(self.hostname_url_pre, headers)
            #print "get_upload_url r:", r
            data = self.handle_response(r, "GET")
            if data and isinstance(data, dict) and "hostname" in data:
                return "%s:%d" % (data["hostname"], data["port"])
        except Exception, e:
            pass
        return self._upload_host

    @network
    def stat_file(self, sample_hash, headers={}):
        headers_ref = self._update_headers(headers)
        url_values = urllib.urlencode({"hash" : sample_hash})
        self.stat_url = "%s?%s" % (self.stat_url_pre, url_values)
        r = self.c.stat_file(self.stat_url, headers_ref)
        return self.handle_response(r, 'GET')

    @network
    def put_file(self, local_file, file_meta={}, headers={}):
        headers_ref = self._update_headers(headers)
        upload_host = self.get_upload_host(headers_ref)
        print "upload_host %s " % upload_host
        put_headers = {}
        put_headers.update(headers)
        put_headers.update({"Content-type" : "application/octet-stream", "Host": upload_host})
        
        headers_ref = self._update_put_headers(put_headers)
        self.assert_file_writeable(local_file)
        url_values = urllib.urlencode(file_meta)
        self.put_url = "http://%s/%s?%s" % (upload_host, self.put_cgi, url_values)
        r = self.c.put_file(self.put_url, local_file, headers_ref)
        return self.handle_response(r, 'PUT')

    def put_file_part(self, local_file, start, length, headers={}):
        self.assert_file_writeable(local_file)
        r = self.c.put_file_part(self.put_url, local_file, start, length, headers)
        return self.handle_response(r)

    def post(self, content, headers={}):
        raise NotImplementException()

    @network
    def post_file(self, local_file, headers={}):
        self.assert_file_writeable(local_file)
        r = self.c.post_multipart(self.post_url, local_file, 'file1', headers)
        return self.handle_response(r)

    @network
    def get_to_file(self, sample_hash, local_file, headers={}, instant_mode=False):
        headers_ref = {}
        headers_ref.update(self.default_headers)
        headers_ref.update(headers)
        try:
            r = self.__get_to_file(sample_hash, local_file, headers_ref, instant_mode)
            #print "status: %d, download_url: %s" % (r["status"], r["download_url"])
            self._post_feedback(sample_hash, r, headers_ref)
            return r
        except HTTPException, e:
            self._post_feedback(sample_hash, e.resp, headers_ref)
            raise e
        except Exception, e:
            raise e

    def __get_to_file(self, sample_hash, local_file, headers={}, instant_mode=False):
        self.assert_file_writeable(local_file)
        url_values = urllib.urlencode({"hash" : sample_hash})
        self.get_url = "%s?%s" % (self.get_url_pre_with_two_get, url_values)
        r = self.c.get_file_with_two_get(self.get_url, local_file, headers)
        return r

    def _post_feedback(self, sample_hash, response, headers={}):
        try:
            self.__post_feedback(sample_hash, response, headers)
        except Exception, e:
            #print "_post_feedback exception ", e
            pass

    def __post_feedback(self, sample_hash, response, headers={}):
        url_values = urllib.urlencode({"hash" : sample_hash})
        url = "%s?%s" % (self.feedback_url_pre, url_values)
        body = {
            "type": "download",
            "status": response.get("status", "0"),
            "download_url": response.get("download_url", "")
        }
        r = self.c.post(url, json.dumps(body), headers)
        #print "post_feedback resp:", r

    @network
    def get(self, headers={}):
        r = self.c.get(self.get_url, headers)
        return self.handle_response(r)

    @network
    def head(self, headers={}):
        r = self.c.head(self.head_url, headers)
        return self.handle_response(r)

    @network
    def delete(self, headers={}):
        return self.c.delete(self.del_url, headers)

    @network
    def setmeta(self, headers={}):
        """ To copy to itself. """
        return self.copy_to(self, headers)

    @network
    def copy_to(self, dst, headers={}):
        headers.update( {
                'x-bs-copy-source': self.ref_str() ,
                'x-bs-copy-source-directive': 'copy', # copy or replace
                })
        return self.c.put(dst.put_url, '', headers)

    @network
    def copy_from(self, dst, headers={}):
        headers.update( {
                'x-bs-copy-source': dst.ref_str() ,
                'x-bs-copy-source-directive': 'copy', # copy or replace
                })
        return self.c.put(self.put_url, '', headers)

"""
class Superfile(Object):
    def __init__(self, bucket, object_name, object_list):
        Object.__init__(self, bucket, object_name)
        self.object_list = object_list

    def assertSubObjectExist(self):
        for o in self.object_list:
            if not o.etag:
                o.head() # get etag

    def put(self, headers={}):
        self.assertSubObjectExist()
        tmp_list = ['"part_%d": {"url": "%s", "etag":"%s"}' % (idx, o.ref_str(), o.etag)
                for idx, o in enumerate(self.object_list)]
        tmp_list = ','.join(tmp_list)
        self.superfile_meta = '{"object_list": {%s}}' % tmp_list
        url = '%s&superfile=1' % self.put_url

        return self.c.put(url, self.superfile_meta, headers)


    @network
    def put_file(self, local_file, headers={}):
        raise NotImplementException()

    @network
    def put_file_retain_versions(self, local_file, headers={}):
        raise NotImplementException()

    @network
    def post_file(self, local_file, headers={}):
        raise NotImplementException()

    @network
    def post_file_retain_versions(self, local_file, headers={}):
        raise NotImplementException()

"""
