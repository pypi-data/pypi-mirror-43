import logging
import sys
import errno
import os
import time

from .log_setting import LogSetting


class Logger(object):
    def __init__(self):
        self.start_time = time.time()
        self.setting = LogSetting().load()
        self.logger = logging.getLogger('podder.task')
        self.logger.setLevel(self.setting["task_log_level"])
        if self.logger.hasHandlers() is False:
            format = self.setting["task_log_format"]
            self._add_default_handler(format)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, extra=self._create_extra())

    def warn(self, msg, *args, **kwargs):
        self.logger.warning(msg, extra=self._create_extra())

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, extra=self._create_extra())

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, extra=self._create_extra())

    def log(self, msg, *args, **kwargs):
        self.logger.log(msg, extra=self._create_extra())

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, extra=self._create_extra())

    # private
    def _create_extra(self):
        ex = {}
        ex['progresstime'] = str(round((time.time() - self.start_time), 3))
        ex['taskname'] = self.setting["task_name"]
        return ex

    def _add_default_handler(self, format):
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(self.setting["task_log_level"])
        handler.setFormatter(
            logging.Formatter(format)
        )
        self.logger.addHandler(handler)


def class_logger(cls):
    global _is_logged
    if _is_logged is False:
        _is_logged = Logger()

    cls.logger = _is_logged
    return cls

_is_logged = False
