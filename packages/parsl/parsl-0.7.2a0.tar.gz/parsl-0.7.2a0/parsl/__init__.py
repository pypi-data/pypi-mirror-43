"""Parsl is a Parallel Scripting Library, designed to enable efficient workflow execution.

Importing
---------

To get all the required functionality, we suggest importing the library as follows:

>>> import parsl
>>> from parsl import *

Logging
-------

Following the general logging philosophy of python libraries, by default
`Parsl <https://github.com/swift-lang/swift-e-lab/>`_ doesn't log anything.
However the following helper functions are provided for logging:

1. set_stream_logger
    This sets the logger to the StreamHandler. This is quite useful when working from
    a Jupyter notebook.

2. set_file_logger
    This sets the logging to a file. This is ideal for reporting issues to the dev team.

"""
import logging

from parsl.version import VERSION
from parsl.app.app import App
from parsl.executors import ThreadPoolExecutor
from parsl.executors import IPyParallelExecutor
from parsl.executors import HighThroughputExecutor
from parsl.executors import ExtremeScaleExecutor

from parsl.data_provider.files import File

from parsl.dataflow.dflow import DataFlowKernel, DataFlowKernelLoader

__author__ = 'The Parsl Team'
__version__ = VERSION

__all__ = [
    'App', 'DataFlowKernel', 'File', 'set_stream_logger', 'set_file_logger',
    'ThreadPoolExecutor', 'HighThroughputExecutor', 'ExtremeScaleExecutor', 'IPyParallelExecutor',
]

clear = DataFlowKernelLoader.clear
load = DataFlowKernelLoader.load
dfk = DataFlowKernelLoader.dfk
wait_for_current_tasks = DataFlowKernelLoader.wait_for_current_tasks


def set_stream_logger(name='parsl', level=logging.DEBUG, format_string=None):
    """Add a stream log handler.

    Args:
         - name (string) : Set the logger name.
         - level (logging.LEVEL) : Set to logging.DEBUG by default.
         - format_string (string) : Set to None by default.

    Returns:
         - None
    """
    if format_string is None:
        # format_string = "%(asctime)s %(name)s [%(levelname)s] Thread:%(thread)d %(message)s"
        format_string = "%(asctime)s %(name)s:%(lineno)d [%(levelname)s]  %(message)s"

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter(format_string, datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Concurrent.futures errors are also of interest, as exceptions
    # which propagate out of the top of a callback are logged this way
    # and then discarded. (see #240)
    futures_logger = logging.getLogger("concurrent.futures")
    futures_logger.addHandler(handler)


def set_file_logger(filename, name='parsl', level=logging.DEBUG, format_string=None):
    """Add a stream log handler.

    Args:
        - filename (string): Name of the file to write logs to
        - name (string): Logger name
        - level (logging.LEVEL): Set the logging level.
        - format_string (string): Set the format string

    Returns:
       -  None
    """
    if format_string is None:
        format_string = "%(asctime)s.%(msecs)03d %(name)s:%(lineno)d [%(levelname)s]  %(message)s"

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename)
    handler.setLevel(level)
    formatter = logging.Formatter(format_string, datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # see note in set_stream_logger for notes about logging
    # concurrent.futures
    futures_logger = logging.getLogger("concurrent.futures")
    futures_logger.addHandler(handler)


class NullHandler(logging.Handler):
    """Setup default logging to /dev/null since this is library."""

    def emit(self, record):
        pass


logging.getLogger('parsl').addHandler(NullHandler())
