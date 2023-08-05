import json
import logging
import logging.handlers
import sys
import uuid

from jkutils.time import utc_strftime

CONSOLE_FORMAT = "%(message)s"
# ‘2006-01-02 15:04:05‘
DATEFMT = "%Y-%m-%d %H:%M:%S"
LEVEL = logging.INFO


if hasattr(sys, "_getframe"):
    currentframe = lambda: sys._getframe(3)
else:  # pragma: no cover

    def currentframe():
        """Return the frame object for the caller's stack frame."""
        try:
            raise Exception
        except Exception:
            return sys.exc_info()[2].tb_frame.f_back


class LogJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super().default(obj)
        except Exception:
            return str(obj)


class JKLogger:
    def __init__(self, project_name, level=LEVEL, datefmt=DATEFMT, native=True):
        self._name = project_name
        self._datefmt = datefmt
        self._default_fields = dict()

        if native:
            logging.basicConfig(level=level)
            logging.debug = self.debug
            logging.info = self.info
            logging.warning = self.warning
            logging.warn = self.warn
            logging.error = self.error
            logging.critical = self.critical

        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(logging.Formatter(fmt=CONSOLE_FORMAT))

        self._logger = logging.getLogger("jk")
        self._logger.setLevel(level)
        self._logger.addHandler(console_handler)

        self._logger.propagate = False

    def debug(self, msg, **kw):
        self._log("debug", msg, **kw)

    def info(self, msg, **kw):
        self._log("info", msg, **kw)

    def warning(self, msg, **kw):
        self._log("warn", msg, **kw)

    def warn(self, msg, **kw):
        self._log("warn", msg, **kw)

    def error(self, msg, **kw):
        self._log("error", msg, **kw)

    def critical(self, msg, **kw):
        self._log("critical", msg, **kw)

    def _log(self, level, msg, **kw):
        f = currentframe()
        data = dict()
        data.update(self._default_fields)
        data.update(
            {
                "msg": msg,
                "funcname": f.f_code.co_name,
                "file": "{}:{}".format(f.f_code.co_filename, f.f_lineno),
                "level": level,
                "project": self._name,
                "time": utc_strftime(self._datefmt),
            }
        )
        data.update(kw)
        getattr(self._logger, level)(json.dumps(data, cls=LogJSONEncoder, ensure_ascii=False))

    def __getattr__(self, name):
        """其他方法透传"""
        return getattr(self._logger, name)

    def set_default_fields(self, **kwargs):
        """
        设置默认打印字段
        """
        self._default_fields.update(kwargs)

    def remove_default_field(self, *keys):
        """
        移除指定默认打印字段
        """
        for key in keys:
            if key in self._default_fields:
                self._default_fields.pop(key)

    def remove_default_all_fields(self):
        """
        移除所有默认打印字段
        """
        self._default_fields = dict()

    @property
    def log_id(self):
        return uuid.uuid4().hex
