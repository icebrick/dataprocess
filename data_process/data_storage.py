#!/usr/bin/python3
# -*- coding: utf-8 -*-

from builtins import object
from functools import wraps
import re
import time
import collections
import MySQLdb as mysql
from MySQLdb.constants import FIELD_TYPE
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

class DataStorage(object):
    def __init__(self, file_name):
        self.file_name = file_name
        with open(self.file_name, 'r') as f:
            head_str = f.readline()
            self.head_list = head_str.replace("-", "_").split()
            self.head_str = ','.join(self.head_list)
            self.table_name = self.file_name.replace("-", "_").split(".")[0]
            self.data_pool = collections.OrderedDict()

    # set the data pool cache to aviod extract from database frequency
    def data_pool_set(self, var_name, data):
        # just keep 15 variable in cache
        def check_data_pool_len(*args, **kwargs):
            if len(self.data_pool) >= 15:
                self.data_pool.popitem(last=False)    # Delete the first inserted data
                self.data_pool_set(*args, **kwargs)

        check_data_pool_len(var_name, data)
        self.data_pool[var_name] = data

    def data_pool_get(self, var_name):
        if var_name in self.data_pool:
            return self.data_pool[var_name]
        return "The variable {} is not in the data pool".format(var_name)

    @timethis
    def connect_db(self, db_name):
        # perform the connection to database
        db = mysql.connect(host='localhost', user='root', passwd='jiandan313', db=db_name)
        cursor = db.cursor()
        print("Connect to database: {}".format(db_name))
        return db, cursor

    # create the empty table for holding the data from datafile
    @timethis
    def cr_db_tb(self):
        # connect to the database
        db, cursor = self.connect_db('DBTest')
        self.check_time_type()
        # create db table with variable name as column name
        # cmd_str_part = ','.join(["{} float".format(i_head) for i_head in self.head_list])
        cmd_list_part = ["{} float".format(i_head) for i_head in self.head_list]
        if self.time_type == 'time_string':
            cmd_list_part[0] = cmd_list_part[0].replace('float', 'TIME(3)')
        cmd_str_part = ','.join(cmd_list_part)
        cmd_str = "CREATE TABLE IF NOT EXISTS {} ({});".format(self.table_name, cmd_str_part)
        # execute the command
        cursor.execute(cmd_str)
        # close the connection
        cursor.close()
        db.close()
        print("succeed to create db table: ".format(self.table_name))

    def check_time_type(self):
        with open(self.file_name, 'r') as f:
            f.readline()    # skip the head line
            first_line_data = f.readline()
            if ':' in first_line_data.split()[0]:
                self.time_type = 'time_string'
            else:
                self.time_type = 'second'

    @timethis
    def insert_data_db(self):
        db, cursor = self.connect_db('DBTest')

        with open(self.file_name, 'r') as f:
            # skip the head line
            f.readline()
            while True:
                data_line = f.readline()
                if data_line:
                    data_line = data_line.split()
                    # transfer the time HH:MM:SS:sss to HH:MM:SS.sss for mysql time column requirement
                    if self.time_type == 'time_string':
                        data_line[0] = re.sub(':', '.', data_line[0][::-1], count=1)[::-1]
                        # make the time str to str when it is in sql cmd
                        data_line[0] = '"'+data_line[0]+'"'
                    data_line = ','.join(data_line)
                    cmd_str = "INSERT INTO {} ({}) VALUES ({})".format(self.table_name, self.head_str, data_line)
                    cursor.execute(cmd_str)
                else:
                    break
            db.commit()
            cursor.close()
            db.close()
            print('Insert data to db succeed')

    def get_head_title(self):
        db, cursor = self.connect_db('DBTest')
        cmd_str = "SELECT * FROM {} LIMIT 1".format(self.table_name)
        cursor.execute(cmd_str)
        # get the column head info
        head_title = [x[0] for x in cursor.description]
        return head_title

    @timethis
    def tuple_process(self, data_tuple):
        # transfer double layer tuple to one layer
        # ((1,),(2,),)  ->   (1, 2,)
        return tuple(map(lambda x: x[0], data_tuple))

    @timethis
    def extract_data(self, var_name):
        # If the data is in the pool
        if var_name in self.data_pool:
            data = self.data_pool_get(var_name)
            print("Extract data {} succeed!".format(var_name))
            return data
        # Else, we need to get it from the database
        db, cursor = self.connect_db('DBTest')
        cmd_str = "SELECT {} FROM {};".format(var_name, self.table_name)
        cursor.execute(cmd_str)
        data = cursor.fetchall()
        data = self.tuple_process(data)
        self.data_pool_set(var_name, data)
        print("Extract data {} succeed!".format(var_name))
        return data

    @timethis
    def slim_data(self, data, ratio):
        # decrease the data frequency
        return data[::ratio]

    @timethis
    def plot_var(self, var_name, ratio=1):
        # get the data from pool or database
        time = self.extract_data('time')
        var = self.extract_data(var_name)
        # slim the data according to the ratio
        time = self.slim_data(time, ratio)
        var = self.slim_data(var, ratio)
        # plot the variable data
        plt.plot(time, var)
        plt.xlabel('t/s')
        plt.ylabel(var_name)
        plt.show()
        print("Plot var {} succeed!".format(var_name))

    def plot_var_multi(self, var_name_list, ratio = 1):
        var_len = len(var_name_list)
        time = self.extract_data('time')
        time = self.slim_data(time, ratio)
        for index, var_name in enumerate(var_name_list):
            var = self.extract_data(var_name)
            var = self.slim_data(var, ratio)
            plt.subplot(var_len, 1, index+1)
            plt.plot(time, var)
            plt.xlabel('t/s')
            plt.ylabel(var_name)
        plt.show()



# file_name = 'ft_data.txt'
# file = FileRead(file_name)
# file.cr_db_tb()
# file.insert_data_db()
# file.plot_var('var5', 1000)
# file.plot_var('var10', 1000)
# file.plot_var('var5', 1000)
# file.plot_var_multi(('var1', 'var2', 'var3'), 1000)
