import logging
from logging import Logger
from sys import argv
from os.path import basename, splitext
from re import sub as replace
import sys


# formats dictionary that gives the logging format words
FORMATS = {'time': '%(asctime)s',  # Human-readable time, By default yyyy-mm-dd hh:mm:ss,ms
           'filename': '%(filename)s',  # Filename portion of pathname.
           'level': '%(levelname)s',    # text logging level for the message.
           'levelno': '%(levelno)s',    # Numeric logging level for the message
           # Source line number where the logging call was issued.
           'line': '%(lineno)d',
           'msg': '%(message)s',    # The logged message
           'logger': '%(name)s',    # Name of the logger used to log the call.
           # Name of function containing the logging call.
           'function': '%(funcName)s',
           'module': '%(module)s',  # Module (name portion of filename).
           'process': '%(process)d',  # Process ID (if available).
           'processname': '%(processName)s',  # Process name (if available).
           'thread': '%(thread)d',  # Thread ID (if available).
           'threadname': '%(threadName)s'  # Thread name (if available).
           }

LEVELS = {'critical': logging.CRITICAL,  # 50
          'error': logging.ERROR,  # 40
          'warning': logging.WARNING,  # 30
          'info': logging.INFO,  # 20
          'debug': logging.DEBUG  # 10
          }


class MyLogger(Logger):
    """a custome logger that inherets from the logging Logger class, to give quick configurations to the logger.
    also provide ready made loggers with the class methods"""

    def __init__(self, name=None, level='debug', form=None, file=None, filelevel=None, stream=True, streamlevel=None):
        """
        Create a logger and configure it according to the arguments passed.
        retrurns the Looger.

        if no kwargs are given, returns a logger that will log to the stream with the lowest logging level

        kwargs:
            level: can be debug, error, warning, info, critical

            format: defaults to a spacific format if none was passed, have to be according to the logging module formatting.

            file: log to a file if one was specified

            filelevel: sets a different logging level to the file, defaults to the logger level

            stream: pring the log to the stream, defaults to True, if False will only log to the file

            streamlevel: sets a different logging level to the stream, defaults to the logger level
            """

        # get the name of the module that will run the logger

        name = name or splitext(basename(argv[0]))[0]
        super().__init__(name)

        # set the level of the logger, passed as a string to the function and matched from the LEVELS dicitonary,
        # sets an instance variable of level to be used elsewhere without the need of the dictionary
        self.level = LEVELS[level]
        self.setLevel(self.level)
        self.filename = file

        # creat the format of the messege if passed in form kwarg, defaults to the else statment
        # words in the form kwarg need to match the FORMAT dictionary keys
        if form:
            self.formatter = self.make_formater(form)
        else:
            self.formatter = logging.Formatter(
                '%(name)s: %(levelname)s: %(message)s')

        # creat a default file handler if a file was passed in and adds the format to it, saves the file handler as an instance variable to give the ability to change it latter by the config_handler method.
        # default file handler form and level are the logger's, unless a filelevel was provided in the kwargs
        if file:
            self.default_fh = self.make_Handler(form, filelevel, file)
            self.addHandler(self.default_fh)

        # on by default, creat a stream handler and save it as an instance variable to give ability to change
        # default stream handler form and level are the logger's, unless a stream level was provided in the kwargs
        if stream:
            self.default_sh = self.make_Handler(form, streamlevel)

            self.addHandler(self.default_sh)

    @staticmethod
    def make_formater(form):
        '''replaces the words in the form to the appropriate logging syntax and return the formmatter to be added'''

        for word in replace(r'[^\w]', ' ', form).split():
            if word in FORMATS.keys():
                form = form.replace(word, FORMATS[word])
        return logging.Formatter(form)

    def make_Handler(self, form=None, level=None, file=None):
        '''makes a handler (file or stream) and sets its level and format and return it to be added to the logger'''
        if file:
            handler = logging.FileHandler(file)
        else:
            handler = logging.StreamHandler()

        # sets a level to the handler if provided, defaults to the logger level
        if not level:
            level = self.level
        else:
            level = LEVELS[level]
        handler.setLevel(level)

        # sets a format to the handler if provided, defaults to the logger format
        if form:
            handler.setFormatter(self.make_formater(form))
        else:
            handler.setFormatter(self.formatter)

        return handler

    def config_handler(self, handler, form=None, level=None):
        '''configure an already excisting handler, including the default handlers.
        can configure the level and format of the handler'''
        if form:
            handler.setFormatter(self.make_formater(form))
        if level:
            handler.setLevel(LEVELS[level])

    def disable(self, level=None):
        '''disable logging of a certian level, defaults to highest level'''
        if not level:
            level = LEVELS['critical']
        else:
            level = LEVELS[level]
        logging.disable(level)

    def set_handler(self, form=None, level=None, file=None):
        '''automaticaly adds the handler to the logger'''
        self.addHandler(self.make_Handler(form, level, file))

    def log_errors(self):
        if self.filename:
            sys.stderr = open(self.filename, 'a')

    def __call__(self, msg):
        self.info(msg)

    @classmethod
    def FunctionLogger(cls):
        '''return a basic funtions logger'''
        return cls(name='FunctionLog', form='name: function: msg')

    @classmethod
    def BasicFileLogger(cls):
        '''return a basic logger that will log to a file with the module name'''
        filename = splitext(basename(argv[0]))[0] + 'Log.log'
        return cls(file=filename, stream=False, form='time- module: level: line: msg')

    # TODO: add rotating file handler and timed rotating file handler functionality


# use case
if __name__ == '__main__':
    log = MyLogger(file='logClass_test.log')
    log.debug('test')

    log.config_handler(
        log.default_fh, form='time: logger: line: msg', level='info')
    log.debug('only stream with different format')
    log.info('stream and file different format')
    log.set_handler(file='2ndtest.log', level='info')
    log.info('test second handler')
    log.debug('only stream')
    func = MyLogger.FunctionLogger()
    func.info('test')
