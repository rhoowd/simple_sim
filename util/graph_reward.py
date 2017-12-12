#!/usr/bin/env python
# coding=utf8
import sys
import re
import matplotlib.pyplot as plt


if __name__ == '__main__':
    num_file = len(sys.argv)-1
    for i in range(1, num_file+1):
        print sys.argv[i]

    filename = sys.argv[1]

    x = []
    y = []

    f = open(filename)

    for line in f:
        if line.split("\t")[1].split(" ")[0] == "reward":
            step = line.split("\t")[2]
            r_str = line.split("\t")[3]
            reward = float(re.sub('[\[\]]', '', r_str))
            print step, reward
            x.append(step)
            y.append(reward)

    # print x, y
    plt.plot(x, y, 'r-')
    plt.show()
