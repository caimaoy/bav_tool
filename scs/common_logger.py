"""

 Copyright (c) 2012 Baidu.com Inc.
 All rights reserved.

 Author: Peng chong <pengchong@baidu.com>
 Date: 12/05/2012

 This is the logger module which provides logger function.

"""


import logging


LEVELS={'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'critical':logging.CRITICAL}

class CommonLogger(object):
    def __init__(self, log_file, log_level):
        """log_level should be the ones in LEVELS. """
        self.logger = logging.getLogger()
        self.log_file = log_file
        handler = logging.FileHandler(log_file)
        self.logger.addHandler(handler)
        self.logger.setLevel(LEVELS.get(log_level, logging.INFO))

    def get_logger(self):
        return self.logger
