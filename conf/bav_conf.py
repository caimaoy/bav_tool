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


# 扫描器类型SCANNER_TYPE
const.ENGINE_TYPE_DICT = [
    {'num': 0x00000001L, 'note':u'超级巡警引擎总开关'},
    {'num': 0x00000002L, 'note':u'特征云引擎'},
    {'num': 0x00000004L, 'note':u'小红伞'},
    {'num': 0x00000008L, 'note':u'二次加速'},
    {'num': 0x00000010L, 'note':u'超级巡警格式识别模块，默认必须加载'},
    {'num': 0x00000020L, 'note':u'本地黑白名单病毒库查询模块'},
    {'num': 0x00000040L, 'note':u'感染式检测模块'},
    {'num': 0x00000080L, 'note':u'恶意木马检测模块'},
    {'num': 0x00000100L, 'note':u'文档启发检测模块'},
    {'num': 0x00000200L, 'note':u'脚本启发检测模块'},
    {'num': 0x00000400L, 'note':u'数字签名检测模块'},
    {'num': 0x00000800L, 'note':u'云引擎检测模块'},
    {'num': 0x00001000L, 'note':u'启发式检测模块'},
    {'num': 0x00002000L, 'note':u'包裹解压模块'},
    {'num': 0x00004000L, 'note':u'升级URL库'},
    {'num': 0x00008000L, 'note':u'主防引擎'},
    {'num': 0x00010000L, 'note':u'云鉴定工具扫描'},
    {'num': 0x00020000L, 'note':u'adware过滤'},
    {'num': 0x00040000L, 'note':u'微特征引擎'},
    {'num': 0x00080000L, 'note':u'急救箱'},
    {'num': 0x00100000L, 'note':u'adware微特征云过滤'},
    {'num': 0x00200000L, 'note':u'应急处理引擎'},
    {'num': 0x00400000L, 'note':u'病毒免疫引擎'},
    {'num': 0x00800000L, 'note':u'硬链接识别'},
    {'num': 0x01000000L, 'note':u'OA防重复扫描识别'},
    {'num': 0x02000000L, 'note':u'脱壳引擎'},
    {'num': 0x04000000L, 'note':u'慧眼引擎'},
]


if __name__ == '__main__':
    print const.BAV_HOST['update_hosts']
