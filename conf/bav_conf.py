# -*- coding: UTF-8 -*-

'''
Last modified time: 2015-04-07 09:57:10
Edit time: 2015-04-07 09:57:37
File name: bav_conf.py
Edit by caimaoy
'''

__author__ = 'caimaoy'

import sys
sys.path.append('..')

import const

const.BAV_HOST = {
    'update_hosts':
    '''
10.242.108.23 download.antivirus.baidu.com
10.242.108.23 dl2.bav.baidu.com
10.242.108.23 dl-vip.bav.baidu.com
10.242.108.23 updown.bav.baidu.com

10.242.108.23 update.bav.baidu.com
10.242.108.23 download.bav.baidu.com
10.242.108.23 update.sd.baidu.com
10.242.108.23 download.sd.baidu.com
'''
    ,

    'md5_hosts':
    '''
10.242.108.23 f.sd.baidu.com
10.242.108.23 up.sd.baidu.com
10.242.108.23 f.bav.baidu.com
10.242.108.23 up.bav.baidu.com
10.242.108.23 f.th.bav.baidu.com
10.242.108.23 up.th.bav.baidu.com
'''
    ,
    'clean':''
}

const.UPLOAD_URL = r'http://client.baidu.com:8775/count/chenyue_tool_count.php'



if __name__ == '__main__':
    print const.BAV_HOST['update_hosts']
