import time
from functools import wraps


def excute_time(func):
    """ Show the time ogf excuting func """

    @wraps(func)
    def excuting(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        print("Calling {}: {}".format(func.__name__, format(time.time() - start, '.5f')))

    return excuting
