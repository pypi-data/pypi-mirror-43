import inspect
import logging as real_logging
import unicodedata
import logging.handlers as real_handlers
import os


class RelativePathRotatingFileHandler(real_handlers.RotatingFileHandler):
    def __init__(self, relative_path, file_name, max_bytes=2000, backup_count=100):
        local_path = os.path.dirname(os.path.abspath(__file__))
        log_path = os.path.join(local_path, relative_path)
        if not os.path.isdir(log_path):
            os.mkdir(log_path)
        log_file_name = os.path.join(log_path, file_name)
        super(RelativePathRotatingFileHandler, self).__init__(log_file_name, max_bytes, backup_count)


def get_logger():
    stack = inspect.stack()
    if len(stack) == 2:
        file_name = os.path.basename(stack[1][1]).split(".")[0]
    else:
        file_name = os.path.basename(stack[2][1]).split(".")[0]
    the_function = stack[1][3]
    # noinspection PyBroadException
    try:
        if len(stack[1][0].f_locals) > 0:
            the_class = str(stack[1][0].f_locals["self"].__class__.__name__) + "."
        else:
            the_class = ""
    except Exception:
        the_class = ""
    logger_name = "{}.{}{}".format(file_name, the_class, the_function)
    return real_logging.getLogger(logger_name)


def _get_arg_list(kwargs):
    string = ""
    count = 0
    for key in kwargs:
        if isinstance(kwargs[key], int):
            val = 'u' + str(kwargs[key])
        else:
            val = kwargs[key]
        # noinspection PyBroadException
        try:
            string += u'' + str(key) + u"=" + val
        except Exception:
            pass
        if count < len(kwargs) - 1:
            string += ","
            count += 1
    if string != "":
        string = "{}".format(unicodedata.normalize('NFKD', string).encode('ascii', 'ignore'))
    return string


def start_function(logger, **kwargs):
    stack = inspect.stack()
    the_function = stack[1][3]
    logger.debug("Starting {}({})".format(the_function, _get_arg_list(kwargs)))


def end_function(logger, **kwargs):
    stack = inspect.stack()
    the_function = stack[1][3]
    logger.debug("Ending {}({})".format(the_function, _get_arg_list(kwargs)))
