#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random


head = ["var{}".format(x) for x in range(100)]
head.insert(0, 'time')
data = range(1000000)

def time_generator():
    # time generator, sample time 0.01
    t = 0
    while True:
        t = t + 0.01
        yield t

def gen_random_line_str(column_size, time):
    # generate the random var value except time column
    random_line = list(map(lambda x:"%.3f"%(x*random.random()), list(range(column_size-1))))
    random_line.insert(0, "%.3f"%time)
    random_line = ' '.join(random_line)
    return random_line


def write2file(scale):
    with open('ft_data.txt', 'w') as f:
        # write the var titles
        for title in head[0:-1]:
            f.write(title)
            f.write(' ')
        f.write(head[-1])
        f.write('\n')
        # write the data
        ge = time_generator()
        for _ in range(scale):
            time = next(ge)
            random_line = gen_random_line_str(len(head), time)
            f.write(random_line)
            f.write('\n')


if __name__ == "__main__":
    print('1')
    scale = 400000
    write2file(scale)
