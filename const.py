# -*- coding: UTF-8 -*-

'''
Last modified time: 2015-06-09 09:49:29
Edit time: 2015-06-09 09:55:07
File name: constant.py
Edit by caimaoy
'''

__author__ = 'caimaoy'


class _const(object):
    class ConstError(TypeError): pass
    class ConstCaseError(TypeError): pass

    def __setattr__(self, name, value):
        if self.__dict__.has_key(name):
            raise self.ConstError, "Can't change const. %s" % name
        if not name.isupper():
            raise self.ConstCaseError, \
                    'const name "%s" is not all uppercase' % name
        self.__dict__[name] = value


import sys
sys.modules[__name__] = _const()
