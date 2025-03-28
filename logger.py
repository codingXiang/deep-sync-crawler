import logging
import sys

import env


# 建立 self._core
class Logger:
    def __init__(self):
        self._core = logging.getLogger('DeepSyncCrawler')
        self._core.setLevel(logging.DEBUG)

        # 建立輸出到 stdout 的 handler
        handler = logging.StreamHandler(sys.stdout)
        log_level = env.get("LOG_LEVEL")
        if log_level == "debug":
            handler.setLevel(logging.DEBUG)
        elif log_level == "info":
            handler.setLevel(logging.INFO)
        elif log_level == "warning":
            handler.setLevel(logging.WARNING)
        elif log_level == "error":
            handler.setLevel(logging.ERROR)
        elif log_level == "critical":
            handler.setLevel(logging.CRITICAL)
        else:
            handler.setLevel(logging.INFO)

        # 設定輸出格式
        formatter = logging.Formatter('%(asctime)s - [%(levelname)s][%(name)s] %(message)s')
        handler.setFormatter(formatter)

        # 將 handler 加入到 logger 中
        self._core.addHandler(handler)

    def debug(self, msg):
        self._core.debug(msg)

    def info(self, msg):
        self._core.info(msg)

    def warning(self, msg):
        self._core.warning(msg)

    def error(self, msg):
        self._core.error(msg)

    def critical(self, msg):
        self._core.critical(msg)


logger = Logger()
