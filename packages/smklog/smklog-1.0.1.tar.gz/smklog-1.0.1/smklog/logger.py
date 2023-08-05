import json
import logging
import sys

__all__ = ["SmkLog"]


class SmkLog(object):

    def __init__(self, platform: str, service: str):
        # e.g. youzan, or 'storefront_wechat' etc. for our own platform
        self.platform = platform

        # e.g. nomad_envoy_order or storefront_auth
        self.service = service

        self._logger = get_log("%s_%s" % (self.platform, self.service))

    """
    All these different log level functions will be overwrote with full
    signature and implementation in the end of current file.
    """

    def info(self, *args, **kw) -> str:
        pass

    def debug(self, *args, **kw) -> str:
        pass

    def error(self, *args, **kw) -> str:
        pass

    def warn(self, *args, **kw) -> str:
        pass

    def critical(self, *args, **kw) -> str:
        pass


def json_dumps_unicode(obj):
    """
    Change Python default json.dumps acting like JavaScript, including allow
    Chinese characters and no space between any keys or values.
    """
    return json.dumps(obj,
                      ensure_ascii=False,
                      separators=(',', ':')
                      )


def get_log(name):
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)

    # ref: https://stackoverflow.com/questions/19561058/duplicate-output-in-simple-python-logging-configuration  # noqa:E501
    log.propagate = False  # stop producing duplicated logs

    if not log.handlers:
        out_handler = logging.StreamHandler(sys.stdout)
        out_handler.setFormatter(logging.Formatter(
            '%(asctime)s.%(msecs)03dZ %(levelname)s %(name)s %(message)s',
            '%Y-%m-%dT%H:%M:%S'))
        out_handler.setLevel(logging.INFO)
        log.addHandler(out_handler)

    return log


for level in ["info", "debug", "error", "warn", "critical"]:
    def closure_log(level):
        def log(self,
                source: str,
                category: str,
                label: str,
                message: str,
                data: object,
                timing: object,
                user: str,
                store_id: str = None,
                request_id: str = None):

            msg = {
                "smklog.platform": self.platform,
                "smklog.service": self.service,
                "smklog.source": source,
                "smklog.category": category,
                "smklog.label": label,
                "smklog.message": message,
                "smklog.data": data,
                "smklog.timing": timing,
                "smklog.user": user
            }

            if store_id:
                msg.update({"smklog.store_id": store_id})
            if request_id:
                msg.update({"smklog.request_id": request_id})

            msg = json_dumps_unicode(msg)
            msg = msg.replace("\n", " - ")

            handler = getattr(self._logger, level)
            handler(msg)  # log current message.

            return msg

        return log

    setattr(SmkLog, level, closure_log(level))  # noqa:E303
