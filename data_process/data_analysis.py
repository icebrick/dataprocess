#!/usr/bin/env python3

from builtins import object
import time
from functools import wraps


def timethis(func):
    # time the function run for performance test
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        r = func(*args, **kwargs)
        end = time.perf_counter()
        print('{}.{} : {}'.format(func.__module__, func.__name__, end - start))
        return r
    return wrapper

class DataProcess(object):
    def __init__(self):
        pass

    def transfer_mat(self):
        '''Transfer the variables data which stored in database to
        Matlab type(.mat) files'''


