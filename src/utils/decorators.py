import time


def excute_time(func):
    """ Show the time ogf excuting func """

    def excuting():
        start = time.time()
        func()
        print("Calling {}: {}".format(func.__name__, format(time.time() - start, '.5f')))

    return excuting
