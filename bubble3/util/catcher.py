import traceback
import sys
import time

from pprint import pformat	

def catch(ignore=[],
          was_doing="something important",
          helpfull_tips="you should use a debugger",
          gbc=None):
    """
    Catch, prepare and log error

    :param exc_cls: error class
    :param exc: exception
    :param tb: exception traceback
    """
    exc_cls, exc, tb=sys.exc_info()
    if exc_cls in ignore:
        msg='exception in ignorelist'
        gbc.say('ignoring caught:'+str(exc_cls))
        return 'exception in ignorelist'
        

    ex_message = traceback.format_exception_only(exc_cls, exc)[-1]
    ex_message = ex_message.strip()
    
    # TODO: print(ex_message)

    error_frame = tb
    while error_frame.tb_next is not None:
        error_frame = error_frame.tb_next

    file = error_frame.tb_frame.f_code.co_filename
    line = error_frame.tb_lineno
    stack = traceback.extract_tb(tb)

    formated_stack = []
    for summary in stack:
        formated_stack.append({
            'file': summary[0],
            'line': summary[1],
            'func': summary[2],
            'text': summary[3]
        })

    event = {
        'was_doing':was_doing,
        'message': ex_message,
        'errorLocation': {
            'file': file,
            'line': line,
            'full': file + ' -> ' + str(line)
        },
        'stack': formated_stack
        #,
        #'time': time.time()
    }

    try:
        #logging.info('caught:'+pformat(event))
        gbc.cry('caught:'+pformat(event))
        print('Bubble3: written error to log')
        print('Bubble3: tips for fixing this:')
        print(helpfull_tips)

    except Exception as e:
        print('Bubble3: cant log error cause of %s' % e)

