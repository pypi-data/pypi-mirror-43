# encoding: utf-8

import logging
import sys
import os
import time

from colorama import Fore, init
from colorlog import ColoredFormatter

init(autoreset=True)

log_colors_config = {
    'DEBUG':    'cyan',
    'INFO':     'green',
    'WARNING':  'yellow',
    'ERROR':    'red',
    'CRITICAL': 'red',
}
logger = logging.getLogger("zybats")


def setup_logger(log_level, log_file=None, log_file_path=None):
    """setup root logger with ColoredFormatter."""
    if log_file_path:
        if os.path.isdir(log_file_path):
            (log_path, testcase) = os.path.split(log_file_path)
        elif os.path.isfile(log_file_path):
            (dir, file) = os.path.split(log_file_path)
            (log_path, testcase) = os.path.split(dir)
        log_file_path = os.path.join(log_path, 'logs')
        if not os.path.exists(log_file_path):
            os.mkdir(log_file_path)
        log_name = os.path.join(log_file_path,'%s.log'%(time.strftime('%Y_%m_%d_%H-%M-%S')))
    else:
        current_path = os.path.dirname(os.path.realpath(__file__))
        log_file_path = os.path.join(os.path.dirname(current_path), 'logs')
        log_name = os.path.join(log_file_path, '%s.log' % (time.strftime('%Y_%m_%d_%H-%M-%S')))

    level = getattr(logging, log_level.upper(), None)
    if not level:
        color_print("Invalid log level: %s" % log_level, "RED")
        sys.exit(1)

    # hide traceback when log level is INFO/WARNING/ERROR/CRITICAL
    if level >= logging.INFO:
        sys.tracebacklimit = 0

    formatter = ColoredFormatter(
        u"%(log_color)s%(bg_white)s%(levelname)-8s%(reset)s %(message)s",
        datefmt=None,
        reset=True,
        log_colors=log_colors_config
    )

    formatter_file = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
    if log_file:
        handler_file = logging.FileHandler(log_file, 'a', encoding='utf-8')
    else:
        handler_file = logging.FileHandler(log_name, 'a', encoding='utf-8')

    handler_file.setLevel(level)
    handler_file.setFormatter(formatter_file)
    logger.addHandler(handler_file)

    handler_console = logging.StreamHandler()
    handler_console.setFormatter(formatter)
    handler_console.setLevel(level)
    logger.addHandler(handler_console)
    logger.setLevel(level)

def coloring(text, color="WHITE"):
    fore_color = getattr(Fore, color.upper())
    return fore_color + text


def color_print(msg, color="WHITE"):
    fore_color = getattr(Fore, color.upper())
    print(fore_color + msg)


def log_with_color(level):
    """ log with color by different level
    """
    def wrapper(text):
        color = log_colors_config[level.upper()]
        getattr(logger, level.lower())(coloring(text, color))

    return wrapper


log_debug = log_with_color("debug")
log_info = log_with_color("info")
log_warning = log_with_color("warning")
log_error = log_with_color("error")
log_critical = log_with_color("critical")
