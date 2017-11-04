#!/usr/bin/env python3

from data_process import data_storage
from data_process import data_plot

file_name = 'data/FTPD-C919-10101-PD-170928-F-01-CAOWEN-429002-16.txt'
data_ins = data_storage.DataStorage(file_name)
print(data_ins.get_head_title())
var_title = data_ins.get_head_title()
# data_ins.cr_db_tb()
# data_ins.insert_data_db()
data_plt = data_plot.DataPlot(data_ins)
p1 = data_plt.plot_var(var_title[32], ratio=1)
# p2 = data_plt.plot_var_multi(('var1', 'var3', 'var1',), ratio=10)
# head_title = data_ins.get_head_title()
# print(head_title)
