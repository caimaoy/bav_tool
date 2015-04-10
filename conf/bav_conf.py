# -*- coding: UTF-8 -*-

'''
Last modified time: 2015-04-07 09:57:10
Edit time: 2015-04-07 09:57:37
File name: bav_conf.py
Edit by caimaoy
'''

__author__ = 'caimaoy'


BAV_HOST = {
    'update_hosts':
    '''
10.240.36.36 update.sd.baidu.com
10.240.36.36 update.bav.baidu.com
10.240.36.36 update.security.baidu.co.th
10.240.36.36 download.sd.baidu.com
10.240.36.36 download.antivirus.baidu.com
10.240.36.36 download.bav.baidu.com
10.240.36.36 download.security.baidu.co.th
10.240.36.36 updown.bav.baidu.com
'''
    ,

    'md5_hosts':
    '''
10.240.36.42 f.sd.baidu.com
10.240.36.42 up.sd.baidu.com
10.240.36.42 f.bav.baidu.com
10.240.36.42 up.bav.baidu.com
10.240.36.42 f.th.bav.baidu.com
10.240.36.42 up.th.bav.baidu.com
'''
    ,
}



if __name__ == '__main__':
    print BAV_HOST['update_hosts']
