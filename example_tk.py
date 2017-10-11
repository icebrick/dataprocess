#!/usr/bin/python3

import tkinter as tk
import matplotlib
from functools import wraps
import time
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from data_process import data_storage
from data_process import data_plot


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

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        file_name = 'ft_data.txt'
        self.data_storage = data_storage.DataStorage(file_name)
        self.data_plt = data_plot.DataPlot(self.data_storage)
        self.var_name_list = self.data_storage.get_head_title()
        self.createWidges()

    def createWidges(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Quit button widget
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(row=0,column=0, sticky=tk.E+tk.W)

        self.var_list()
        #
        self.plt, self.fig= self.plot_init()
        #
        self.button = tk.Button(self, text='Plot', command=self.plot_var)
        self.button.grid(row=2,column=0, sticky=tk.E+tk.W)



    def var_list(self):
        # List widget for show all the variable names

        # Get the variable names
        var_names = tk.StringVar()
        var_names.set(' '.join(self.var_name_list))
        # Create the scroll bar
        self.yScroll = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.yScroll.grid(row=1,column=1, sticky=tk.N+tk.S)
        # Create list widget
        self.list = tk.Listbox(self)
        self.list['selectmode'] = tk.EXTENDED
        self.list['width'] = 15
        self.list['listvariable'] = var_names
        self.list['yscrollcommand'] = self.yScroll.set
        self.list.grid(row=1,column=0, sticky=tk.N+tk.S)
        self.yScroll['command'] = self.list.yview

    @timethis
    def plot_init(self):
        fig = plt.figure(1)

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.show()
        plot_widget = canvas.get_tk_widget()
        fig.canvas.draw()
        plot_widget.grid(row=1,column=2, sticky=tk.N+tk.S+tk.E+tk.W)
        plt.plot()
        fig.canvas.draw()
        return plt, fig

    @timethis
    def plot_var(self):

        self.plt.clf()
        plt.grid(b=True)
        line_handles = list()
        var_names_selected = list()

        var_index = self.list.curselection()
        if not var_index:
            return
        for index in var_index:
            var_name = self.var_name_list[index]
            var_names_selected.append(var_name)


            time = self.data_storage.extract_data('time')
            data = self.data_storage.extract_data(var_name)

            ratio = 1000
            time = self.data_storage.slim_data(time, ratio)
            data = self.data_storage.slim_data(data, ratio)
            # a.plot(time, data)

            h = self.plt.plot(time, data)
            line_handles.append(h)
        self.plt.xlabel('t/s')
        # self.plt.ylabel(var_name)
        self.plt.figlegend(line_handles, var_names_selected, "upper right")
        self.fig.canvas.draw()
        #
        # toolbar = NavigationToolbar2TkAgg(canvas, self)
        # toolbar.update()
        # canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)






app = Application()
app.master.title('Sample Application by Jayden')
app.mainloop()
