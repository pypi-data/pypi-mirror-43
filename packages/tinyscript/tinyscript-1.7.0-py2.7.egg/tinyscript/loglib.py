#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Module for defining logging-related constants and objects.

"""
import coloredlogs
import logging

from .__info__ import __author__, __copyright__, __version__


__features__ = ["LOG_FORMAT", "DATE_FORMAT", "TIME_MILLISECONDS",
                "logger", "logging"]
__all__ = ["coloredlogs", "configure_logger"] + __features__


DATE_FORMAT = '%H:%M:%S'
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
TIME_MILLISECONDS = False


# add a custom log level for stepping
STEP_COLOR = "cyan"
logging.STEP = 100
logging.addLevelName(logging.STEP, "STEP")
def step(self, message, *args, **kwargs):
    if self.isEnabledFor(logging.STEP):
        self._log(logging.STEP, message, args, **kwargs) 
logging.Logger.step = step
coloredlogs.DEFAULT_LEVEL_STYLES['step'] = dict(color=STEP_COLOR,
                                           bold=coloredlogs.CAN_USE_BOLD_FONT)


# add a custom log level for timing
TIME_COLOR = "magenta"
logging.TIME = 100
logging.addLevelName(logging.TIME, "TIME")
def time(self, message, *args, **kwargs):
    if self.isEnabledFor(logging.TIME):
        self._log(logging.TIME, message, args, **kwargs) 
logging.Logger.time = time
coloredlogs.DEFAULT_LEVEL_STYLES['time'] = dict(color=TIME_COLOR,
                                           bold=coloredlogs.CAN_USE_BOLD_FONT)


# setup a default logger for allowing logging before initialize() is called
logger = logging.getLogger("main")
coloredlogs.DEFAULT_LOG_FORMAT = LOG_FORMAT
coloredlogs.DEFAULT_DATE_FORMAT = DATE_FORMAT
coloredlogs.install(logger=logger)


def configure_logger(glob, multi_level):
    """
    Logger configuration function for setting either a simple debug mode or a
     multi-level one.
    
    :param glob:        globals dictionary
    :param multi_level: boolean telling if multi-level debug is to be considered
    """
    levels = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG] \
             if multi_level else [logging.INFO, logging.DEBUG]
    try:
        verbose = min(int(glob['args'].verbose), 3)
    except AttributeError:
        verbose = 0
    glob['args']._debug_level = dl = levels[verbose]
    logger.handlers = []
    glob['logger'] = logger
    handler = logging.StreamHandler()
    formatter = logging.Formatter(glob['LOG_FORMAT'], glob['DATE_FORMAT'])
    handler.setFormatter(formatter)
    glob['logger'].addHandler(handler)
    glob['logger'].setLevel(dl)
    coloredlogs.DEFAULT_LOG_FORMAT = glob['LOG_FORMAT']
    coloredlogs.DEFAULT_DATE_FORMAT = glob['DATE_FORMAT']
    coloredlogs.install(dl, logger=glob['logger'],
                        milliseconds=TIME_MILLISECONDS)
