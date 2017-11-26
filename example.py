#!/usr/bin/env python3

from data_process import data_storage
from data_process import dbhub
from data_process import data_plot
import matplotlib.pyplot as plt

file_path = 'caowen/'
file_name = ['FTPD-C919-10101-YL-171124-F-01-CAOWEN-664002-16.txt',
             'FTPD-C919-10101-YL-171124-F-01-CAOWEN-429002-16.txt',
             'FTPD-C919-10101-YL-171124-F-01-CAOWEN-429003-16.txt',
             'FTPD-C919-10101-YL-171124-F-01-CAOWEN-664003-16.txt',
             'FTPD-C919-10101-YL-171124-F-01-CAOWEN-664004-16.txt']
data_ins = dbhub.DBHub('ftdata')
# for file in file_name:
#     data_ins.store_data(file_path, file)
time = data_ins.get_var('Time_added')
data = data_ins.get_var('DS663')
var_name = data_ins.get_var_names()
plt.plot(time, data)
plt.show()

# var_title = data_ins.get_head_title()
# # data_ins.cr_db_tb()
# # data_ins.insert_data_db()
# data_plt = data_plot.DataPlot(data_ins)
# p1 = data_plt.plot_var(var_title[32], ratio=1)
# # p2 = data_plt.plot_var_multi(('var1', 'var3', 'var1',), ratio=10)
# # head_title = data_ins.get_head_title()
# # print(head_title)
