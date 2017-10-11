#!/usr/bin/env python3

from builtins import object
import time
from functools import wraps
from multiprocessing import Process
import matplotlib.pyplot as plt


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

# the class for handling the plot for the data
class DataPlot(object):
    def __init__(self, data_storage):
        # get the variable name and data
        self.data_ins = data_storage

    @timethis
    def plot_var_no_process(self, var_name, ratio=1):
        # get the data from pool or database
        time = self.data_ins.extract_data('time')
        var = self.data_ins.extract_data(var_name)
        # slim the data according to the ratio
        time = self.data_ins.slim_data(time, ratio)
        var = self.data_ins.slim_data(var, ratio)
        # plot the variable data
        plt.plot(time, var)
        plt.xlabel('t/s')
        plt.ylabel(var_name)
        plt.show()
        print("Plot var {} succeed!".format(var_name))

    # Create a new process for handling the plot action
    def plot_var(self, var_name_list, ratio=1):
        p = Process(target=self.plot_var_no_process, args=(var_name_list, ratio))
        p.start()
        return p    # return the process handle

    @timethis
    def plot_var_multi_no_process(self, var_name_list, ratio=1):
        var_len = len(var_name_list)
        time = self.data_ins.extract_data('time')
        time = self.data_ins.slim_data(time, ratio)
        for index, var_name in enumerate(var_name_list):
            var = self.data_ins.extract_data(var_name)
            var = self.data_ins.slim_data(var, ratio)
            plt.subplot(var_len, 1, index+1)
            plt.plot(time, var)
            plt.xlabel('t/s')
            plt.ylabel(var_name)
        plt.show()

    # Create a new process for handling the plot action
    def plot_var_multi(self, var_name_list, ratio=1):
        p = Process(target=self.plot_var_multi_no_process, args=(var_name_list, ratio))
        p.start()
        return p    # return the process handle

