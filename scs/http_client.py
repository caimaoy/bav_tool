"""

 Copyright 2012 Baidu.com Inc.
 All rights reserved.

 Authors: Peng chong <pengchong@baidu.com>
 Date: 12/05/2012

 This is http client module.

"""


import base64
import cookielib
import copy
import hmac
import hashlib
import httplib
import mimetypes
import os
import re
import sys
import time
import urllib
import urllib2
from cStringIO import StringIO
from urlparse import urlparse
from common import shorten
import logging
logger = logging.getLogger('pyhttpclient')
try:
    import json
except:
    import simplejson as json

try:
    import pycurl
except:
    pass


# A function decorator
def network(func):
    if not hasattr(func, 'attr') :
        func.attr = []
    func.attr += ['network']
    return func


class HTTPException(Exception):
    def __init__(self, resp, msg=None):
        Exception.__init__(self)
        self.resp = resp

    def __str__(self):
        return str(self.resp) 

class FilePartReader:
    def __init__(self, fp, start, length):
        self.fp = fp
        self.fp.seek(start)
        self.length = length

    def read_callback(self, size):
        if self.length == 0:
            return ''
        if self.length > size:
            self.length -= size
            return self.fp.read(size)
        else :
            size = self.length
            self.length -= size
            return self.fp.read(size)

    def read_all(self):
        return self.read_callback(self.length)

class HttpClient(object):
    """define the http client interface. """
    def __init__(self):
        pass

    def get(self, url, headers={}):
        raise NotImplementException()

    def head(self, url, headers={}):
        raise NotImplementException()

    def put(self, url, body='', headers={}):
        raise NotImplementException()

    def post(self, url, body='', headers={}):
        raise NotImplementException()

    def delete(self, url, headers={}):
        raise NotImplementException()

    def get_file(self, url, local_file, headers={}):
        raise NotImplementException()

    def put_file(self, url, local_file, headers={}):
        raise NotImplementException()

    def stat_file(self, url, headers={}):
        raise NotImplementException()

    def post_multipart(self, url, local_file, filename='file1', fields={}, headers={}):
        raise NotImplementException()

    def put_file_part(self, url, local_file, start, length, headers={}):
        raise NotImplementException()

    def _parse_resp_headers(self, resp_header):
        (status, header) = resp_header.split('\r\n\r\n') [-2] . split('\r\n', 1)
        status = int(status.split(' ')[1])

        header = [i.split(':', 1) for i in header.split('\r\n') ]
        header = [i for i in header if len(i)>1 ]
        header = [[a.strip().lower(), b.strip()]for (a,b) in header ]
        return (status, dict(header) )


class PyCurlHttpClient(HttpClient):
    def __init__(self, proxy = None, limit_rate = 0):
        pass

    def get(self, url, headers={}):
        logger.info('pycurl -X GET "%s" ', url)
        self._init_curl('GET', url, headers)
        return self._do_request()

    def head(self, url, headers={}):
        logger.info('pycurl -X HEAD "%s" ', url)
        self._init_curl('HEAD', url, headers)
        return self._do_request()

    def delete(self, url, headers={}):
        logger.info('pycurl -X DELETE "%s" ', url)
        self._init_curl('DELETE', url, headers)
        return self._do_request()

    def stat_file(self, url, headers={}):
        logger.info('pycurl -X GET "%s"', url)
        self._init_curl('GET', url, headers)
        return self._do_request()

    def get_file(self, url, local_file, headers={}):
        logger.info('pycurl -X GET "%s" > %s', url, local_file)
        self._init_curl('GET', url, headers, local_file)
        return self._do_request()

    def put(self, url, body='', headers={}):
        headers = copy.deepcopy(headers)
        logger.info('pycurl -X PUT -d "%s" "%s" ', shorten(body, 100), url)
        self._init_curl('PUT', url, headers)
        req_buf =  StringIO(body)
        self.c.setopt(pycurl.INFILESIZE, len(body))
        self.c.setopt(pycurl.READFUNCTION, req_buf.read)
        return self._do_request()

    def post(self, url, body='', headers={}, log=True):
        headers = copy.deepcopy(headers)
        if log:
            logger.info('pycurl -X POST "%s" ', url)
        headersnew = { 'Content-Length': str(len(body))}
        headers.update(headersnew)
        self._init_curl('POST', url, headers)
        req_buf =  StringIO(body)
        self.c.setopt(pycurl.READFUNCTION, req_buf.read)
        return self._do_request()

    def put_file(self, url, local_file, headers={}):
        logger.info('pycurl -X PUT -T"%s" "%s" ', local_file, url)
        filesize = os.path.getsize(local_file)
        if 'Content-Length' not in headers:
            headers.update({'Content-Length': str(filesize+2) })
        if 'Expect' not in headers:
            headers.update({'Expect': '' })
        self._init_curl('PUT', url, headers)
        self.c.setopt(pycurl.INFILESIZE, filesize)
        self.c.setopt(pycurl.INFILE, open(local_file, 'rb'))
        return self._do_request()

    def put_file_part(self, url, local_file, start, length, headers={}):
        """just for pycurl. """
        logger.info('pycurl -X PUT -T"%s[%d->%d]" "%s" ', local_file, start, length, url)
        self._init_curl('PUT', url, headers)
        filesize = os.path.getsize(local_file)

        self.c.setopt(pycurl.INFILESIZE, length)
        self.c.setopt(pycurl.READFUNCTION, FilePartReader(open(local_file, 'rb'), start, length).read_callback)

        return self._do_request()

    def post_multipart(self, url, local_file, filename='file1', fields={}, headers={}):
        post_info = ' '.join( ['-F "%s=%s"' % (k,urllib.quote(v)) for (k,v) in fields.items()])
        if local_file:
            post_info += ' -F "%s=@%s" ' % (filename, local_file)
        logger.info('pycurl -X POST %s "%s" ', post_info, url)
        self._init_curl('POST', url, headers)
        values = fields.items()
        if filename:
            values.append( (filename, (pycurl.FORM_FILE, local_file)) )
        self.c.setopt(pycurl.HTTPPOST, values)
        return self._do_request()

    def _do_request(self):
        #add by guochuqin 2013.06.27
        self.c.setopt(pycurl.CONNECTTIMEOUT, 60)
        self.c.setopt(pycurl.TIMEOUT, 300)
        
        self.c.perform()
        resp_header = self.c.resp_header_buf.getvalue()
        resp_body = self.c.resp_body_buf.getvalue()
        status = self.c.getinfo(pycurl.HTTP_CODE)

        status, headers = self._parse_resp_headers(resp_header)
        self.c.close()

        rst = { 'status': status,
                'header' : headers,
                'body': resp_body,
                'body_file': self.c.resp_body_file,
                }
        if (status in [200, 206]):
            return rst
        else:
            raise HTTPException(rst)

    def _init_curl(self, verb, url, headers, resp_body_file=None):
        self.c = pycurl.Curl()
        self.c.resp_header_buf = None
        self.c.resp_body_buf = None
        self.c.resp_body_file = None

        self.c.setopt(pycurl.DEBUGFUNCTION, self._curl_log)
        self.c.setopt(pycurl.VERBOSE, 1)
        self.c.setopt(pycurl.FOLLOWLOCATION, 1)
        self.c.setopt(pycurl.MAXREDIRS, 10)

        self.c.setopt(pycurl.SSL_VERIFYHOST, 0)
        self.c.setopt(pycurl.SSL_VERIFYPEER, 0)

        #self.c.setopt(pycurl.CONNECTTIMEOUT, 100)
        #self.c.setopt(pycurl.TIMEOUT, 60*60*3)

        self.c.unsetopt(pycurl.CUSTOMREQUEST)

        if verb == 'GET' : self.c.setopt(pycurl.HTTPGET, True)
        elif verb == 'PUT' : self.c.setopt(pycurl.UPLOAD , True)
        elif verb == 'POST' : self.c.setopt(pycurl.POST  , True)
        elif verb == 'HEAD' : self.c.setopt(pycurl.NOBODY, True)
        elif verb == 'DELETE' : self.c.setopt(pycurl.CUSTOMREQUEST, 'DELETE')
        else: raise KeyError('unknown verb ' + verb)

        self.c.setopt(pycurl.URL, url)

        if headers:
            headers = ['%s: %s'%(k, v) for (k,v) in headers.items()]
            self.c.setopt(pycurl.HTTPHEADER, headers)

        self.c.resp_header_buf = StringIO()
        self.c.resp_body_buf = StringIO()
        self.c.setopt(pycurl.HEADERFUNCTION,    self.c.resp_header_buf.write)

        if resp_body_file:
            self.c.resp_body_file = resp_body_file
            f = open(resp_body_file, "wb")
            self.c.setopt(pycurl.WRITEDATA, f)
        else:
            self.c.setopt(pycurl.WRITEFUNCTION,     self.c.resp_body_buf.write)

    def _curl_log(self, debug_type, debug_msg):
        curl_out = [    pycurl.INFOTYPE_HEADER_OUT,         #2  find this out from pycurl.c
                        pycurl.INFOTYPE_DATA_OUT,           #4
                        pycurl.INFOTYPE_SSL_DATA_OUT]       #6
        curl_in  =  [   pycurl.INFOTYPE_HEADER_IN,          #1
                        pycurl.INFOTYPE_DATA_IN,            #3
                        pycurl.INFOTYPE_SSL_DATA_IN]        #5
        curl_info = [   pycurl.INFOTYPE_TEXT]               #0

        if debug_type in curl_out:
            logger.debug("> %s" % debug_msg.strip())
        elif debug_type in curl_in:
            logger.debug("< %s" % debug_msg.strip())
        else:
            logger.debug("I %s" % (debug_msg.strip()) )


class HttplibHttpClient(HttpClient):
    def __init__(self):
        self.connection_buffer = {}
        self.get_redirect = False

    def request(self, verb, url, data, headers={}):
        """used by small response (get/put), not get_file. """
        response, conn = self.send_request(verb, url, data, headers)
        if verb == 'HEAD':
            response.close()
            conn.close()
            resp_body = ''
        else:
            resp_body = response.read()
            response.close()
            conn.close()
        for (k, v) in response.getheaders():
            logger.debug('< %s: %s' % (k, v))
        logger.debug('< ' + shorten(data, 1024))
        rst = { 'status': response.status,
                'header' : dict(response.getheaders()),
                'body': resp_body,
                'body_file': None
        }
        if (response.status in [200, 206]):
            return rst
        else:
            print rst
            raise HTTPException(rst)

    def send_request(self, verb, url, data, headers={}):
        """used by all methods. """
        logger.info('ll httplibcurl -X "%s" "%s" ', verb, url)
        for (k, v) in headers.items():
            logger.debug('> %s: %s' % (k, v))
        logger.debug('\n')
        logger.debug('> ' + shorten(data, 1024))
        o = urlparse(url)
        host = o.netloc
        path = o.path
        if o.query:
            path+='?'
            path+=o.query
        conn = None
        #print "verb,", verb
        #print "url:", url
        #print "host:", host
        #print "path:", path
        #print "headers:", headers
        #print "data:", data
        if o.scheme == 'https':
            if not conn:
                conn = httplib.HTTPSConnection(host, None, False, 300)
        else:
            if not conn:
                conn = httplib.HTTPConnection(host, None, False, 300)
        try:
            conn.request(verb, path, data, headers)
        except:
            #print "exception......"
            conn.close()
            conn = None
            if o.scheme == 'https':
                if not conn:
                    conn = httplib.HTTPSConnection(host, None, False, 300)
            else:
                if not conn:
                    conn = httplib.HTTPConnection(host, None, False, 300)
            conn.request(verb, path, data, headers)

        response = conn.getresponse()
        return response, conn

    def get(self, url, headers={}):
        return self.request('GET', url, '', headers)

    def head(self, url, headers={}):
        return self.request('HEAD', url, '', headers)

    def put(self, url, body='', headers={}):
        headers = copy.deepcopy(headers)
        if 'Content-Length' not in headers:
            headers.update({'Content-Length': str(len(body)) })
        return self.request('PUT', url, body, headers)

    def post(self, url, body='', headers={}):
        headers = copy.deepcopy(headers)
        if 'Content-Type' not in headers:
            headers.update({'Content-Type': 'text/html'})
        if 'Content-Length' not in headers:
            headers.update({'Content-Length': str(len(body)) })
        return self.request('POST', url, body, headers)

    def delete(self, url, headers={}):
        return self.request('DELETE', url, '', headers)

    def get_file_with_two_get(self, url, local_file, headers={}):
        logger.info('httplibcurl -X GET "%s" > %s ', url, local_file)
        response, conn = self.send_request('GET', url, '', headers)

        self.get_redirect = False
        redirect_url = ""
        while True:
            if response.status in [200, 206]:
                if not self.get_redirect:
                    redirect_url = str(response.read())
                    response.close()
                    conn.close()
                    #print redirect_url
                    if redirect_url.startswith("http://"):
                        self.get_redirect = True
                        for i in range(2):
                            response, conn = self.send_request('GET', redirect_url, '', {})
                            if response.status in [200, 206]:
                                break
                            else:
                                response.close()
                                conn.close()
                    else:
                        raise Exception("wrong protocol")
                else:
                    fout = open(local_file, 'wb')
                    try:
                        CHUNK = 1024*512
                        while True:
                            data = response.read(CHUNK)
                            if not data:
                                break
                            fout.write(data)
                    except Exception,e:
                        response.close()
                        conn.close()
                        fout.close();
                        os.remove(local_file);
                        raise Exception(e);
                    fout.close()
                    break
            elif response.status in [302]:
                response.close()
                conn.close()
                resp_headers = dict(response.getheaders())
                new_location = resp_headers["location"]
                response, conn = self.send_request('GET', new_location, '', headers)
            else:
                break
        response.close()
        conn.close()

        rst = { 'status':  response.status,
                'header' : dict(response.getheaders()),
                'body':    None,
                'body_file': local_file,
                'download_url': redirect_url
        }
        #print "rst:", rst
        if (response.status in [200, 206]):
            return rst
        else:
            raise HTTPException(rst)

    def get_file(self, url, local_file, headers={}):
        logger.info('httplibcurl -X GET "%s" > %s ', url, local_file)
        response, conn = self.send_request('GET', url, '', headers)

        while True:
            if response.status in [200, 206]:
                fout = open(local_file, 'wb')
                CHUNK = 1024*512
                while True:
                    data = response.read(CHUNK)
                    if not data:
                        break
                    fout.write(data)
                fout.close()
                break
            elif response.status in [302]:
                response.close()
                conn.close()
                resp_headers = dict(response.getheaders())
                new_location = resp_headers["location"]
                response, conn = self.send_request('GET', new_location, '', headers)
            else:
                break
        response.close()
        conn.close()
        rst = { 'status':  response.status,
                'header' : dict(response.getheaders()),
                'body':    None,
                'body_file': local_file,
        }
        if (response.status in [200, 206]):
            return rst
        else:
            raise HTTPException(rst)

    def stat_file(self, url, headers={}):
        logger.info('httplibcurl -X GET -T %s', url)
        return self.get(url, headers)

    def put_file(self, url, local_file, headers={}):
        logger.info('httplibcurl -X PUT -T "%s" %s ',  local_file, url)
        #return self.put(url, open(local_file, 'rb').read(), headers)
        #newly bfe does not support PUT protocol
        return self.post(url, open(local_file, 'rb').read(), headers)

    def post_multipart(self, url, local_file, filename='file1', fields={}, headers={}):
        logger.info('httplibcurl -X POST -F "%s" %s with fields: %s',  local_file, url, str(fields))
        headers = copy.deepcopy(headers)
        if local_file and filename:
            f = (filename, os.path.basename(local_file), open(local_file, 'rb').read())
            f_list = [f]
        else:
            f_list = []
        content_type, body = encode_multipart_formdata(fields.items(), f_list)
        headersnew = { 'Content-Type' : content_type,
                'Content-Length': str(len(body))}
        headers.update(headersnew)
        #req = urllib2.Request(url, body, headers)
        return self.post(url, body, headers)

    def put_file_part(self, url, local_file, start, length, headers={}):
        logger.warn('it is a tragedy to use `put_file_part` by httplib , YoU NeeD pycurl installed! ')
        data = FilePartReader(open(local_file, 'rb'), start, length).read_all()
        return self.put(url, data, headers)

def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % _get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body


def _get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


def select_best_http_client():
    import platform
    logger.debug('Httplib httpclient')
    return HttplibHttpClient()
    try:
        import pycurl
        logger.debug('PyCurl httpclient')
        return PyCurlHttpClient()
    except :
        logger.debug('Httplib httpclient')
        return HttplibHttpClient()


__all__ = ['network', 'HTTPException', 'PyCurlHttpClient',
           'HttplibHttpClient', 'select_best_http_client'
        ]
