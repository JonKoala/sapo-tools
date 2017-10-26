import logging
from inspect import getframeinfo, stack

from appconfig import settings
import inout

LOG_TYPES = ['info', 'exception']
__LOG_REFS = {
    'info': logging.info,
    'exception': logging.exception
}

def log(message, logtype='info'):

    print(message)

    #getting caller data
    caller = getframeinfo(stack()[1][0])
    data = '[{}:{}] {}'.format(caller.filename, caller.lineno, message)

    log_ref = __LOG_REFS[logtype]
    log_ref(data)


##
#INITIALIZATION


filename = inout._enforce_file_extension(settings['logger']['filename'], '.txt')
filename = '{}/{}'.format(settings['logger']['filepath'], settings['logger']['filename'])
inout._enforce_path(filename)

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG,
    filename=filename)
