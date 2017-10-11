#!/usr/bin/env python3

from data_process import data_storage
from data_process import data_plot

file_name = 'ft_data.txt'
data_ins = data_storage.DataStorage(file_name)
data_plt = data_plot.DataPlot(data_ins)
p1 = data_plt.plot_var('var10', ratio=100)
p2 = data_plt.plot_var_multi(('var1', 'var3', 'var1',), ratio=10)
head_title = data_ins.get_head_title()
print(head_title)
