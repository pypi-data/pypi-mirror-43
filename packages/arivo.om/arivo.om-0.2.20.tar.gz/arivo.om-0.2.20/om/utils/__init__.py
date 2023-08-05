import logging
import sys

from .healthz import Healthz, HealthzStatus

if sys.version_info < (3, 0):
    from .config import log_level as __log_level


    def setup_logging():
        log_level = __log_level()
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s:%(levelname)s:%(name)s -> %(message)s [%(filename)s:%(lineno)s]"
        )
else:
    print("config env vars are not available in python3, use environs")

__all__ = ['Healthz', 'setup_logging']
