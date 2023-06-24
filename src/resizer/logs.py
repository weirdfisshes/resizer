import sys
import datetime
import textwrap
import traceback as traceback_module


def write(line):
    sys.stderr.write(f'''{line['timestamp']} {line['level']}\n''')
    sys.stderr.write(f'''   service: {line['service']}\n''')
    sys.stderr.write(f'''   module: {line['module']}\n''')
    sys.stderr.write(f'''   line: {line['line']}\n''')
    sys.stderr.write(f'''   message: {line['message']}\n''')
    sys.stderr.write(f'''   arguments: {line['arguments']}\n''')
    if 'exception' in line:
        sys.stderr.write(f'''    exception: {line['exception']}\n''')

        if 'traceback' in line:
            sys.stderr.write('\n')
            sys.stderr.write(textwrap.indent(line['traceback'], '    '))

    sys.stderr.write('\n')
    sys.stderr.flush()


def get_log(level, frame, message, *, exception = None, traceback = None, **kwargs):
    line = {
        'service': 'AAA',
        'timestamp': str(datetime.datetime.now()),
        'module': frame.f_globals['__name__'],
        'line': frame.f_lineno,
        'level': level,
        'message': message,
        'arguments': kwargs
    }

    if exception is not None:
        line['exception'] = repr(exception)
        line['traceback'] = ''.join(traceback_module.format_exception(None, exception, traceback))

    write(line)


def debug(message, **kwargs):
    get_log('DEBUG', sys._getframe().f_back, message, **kwargs)


def info(message, **kwargs):
    get_log('INFO', sys._getframe().f_back, message, **kwargs)


def warning(message, **kwargs):
    get_log('WARNING', sys._getframe().f_back, message, **kwargs)


def error(message, **kwargs):
    get_log('ERROR', sys._getframe().f_back, message, **kwargs)


def exception_caught(message, **kwargs):
    exception_type, exception, traceback = sys.exc_info()
    get_log('ERROR', sys._getframe().f_back, message, exception = exception, traceback = traceback, **kwargs)
