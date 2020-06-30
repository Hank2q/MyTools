import logging
from sys import argv
from os.path import basename, splitext
from re import sub as replace

FORMATS = {'time': '%(asctime)s',
               'filename': '%(filename)s',
               'level': '%(levelname)s',
               'line': '%(lineno)d',
               'msg': '%(message)s',
               'logger': '%(name)s',
               'function': '%(funcName)s',
               'module': '%(module)s'}

LEVELS = {'critical': logging.CRITICAL,
          'error': logging.ERROR,
          'warning': logging.WARNING,
          'info': logging.INFO,
          'debug': logging.DEBUG}


def MakeLogger(name=None, level='debug', form=None, file=None, filelevel=None, stream=True):
    '''
    Create a logger and configure it according to the arguments passed.
    retrurns the Looger.

    if no kwargs are given, returns a logger that will log to the stream with the lowest logging level
    
    kwargs:
        level: can be debug, error, warning, info, critical
        
        format: defaults to a spacific format if none was passed, have to be according to the logging module formatting.
        
        file: log to a file if one was specified

        filelevel: sets a different logging level to the file, defaults to the logger level

        stream: pring the log to the stream, defaults to True, if False will only log to the file
        '''

    # get the name of the module that will run the logger
    if not name:
        name = splitext(basename(argv[0]))[0]
    
    # initiate the logger
    logger = logging.getLogger(name)

    # set the level of the logger, based as a string to the function and matched from the LEVELS dicitonary
    logger.setLevel(LEVELS[level])

    # creat the format of the messege if passed in form kwarg, defaults to the else statment
    # words in the form need to match the dictionary or arguments
    
    # replaces the words passed in the form to the appropriate logging syntax
    if form:
        for word in replace(r'[^\w]', ' ', form).split():
            if word in FORMATS.keys():
                form = form.replace(word, FORMATS[word])
        formatter = logging.Formatter(form)
    else:
        formatter = logging.Formatter('%(name)s: %(levelname)s: %(message)s')


    # creat a file handler if a file was passed in and adds the format to it
    if file:
        file_handler = logging.FileHandler(file)

    # specify a level to log to the file if a file level was provided, defaults to the logger level
        if filelevel:
            file_handler.setLevel(LEVELS[filelevel])

    # adds the formatter to the file handler
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    # display the logging messege to the stream if passed as True
    if stream:
        stream_handler = logging.StreamHandler()

    # adds the formatter to the stream handler
        stream_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)
    return logger


# diacles all loggers
def disable(level='critical'):
    logging.disable(LEVELS[level])


if __name__ == '__main__':
    logger = MakeLogger(level='debug', file='make_test.log', filelevel='info', stream=True,
        form='time/ module/ level: "msg"')
    # disable()
    # will print to the stream and file, file level is set to warning
    logger.warning('to file and stream')
    # will only show in stream because level is lower than file level
    logger.info('only on stream')