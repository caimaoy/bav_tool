"""

 Copyright 2012 Baidu.com Inc.
 All rights reserved.

 Authors: Peng chong <pengchong@baidu.com>
 Date: 12/05/2012

 This is exception module.

"""


class DbException(Exception):
    def __init__(self, sql_statement):
        Exception.__init__(self, sql_statement)
        self.sql_statement = sql_statement

    def __str__(self):
        count = 20
        print '='*count
        return str(self.sql_statement)

class NameException(Exception):
    def __init__(self, msg=None):
        Exception.__init__(self)
        self.msg = msg
    def __str__(self):
        return 'NameExecption: ' + str(self.msg)

