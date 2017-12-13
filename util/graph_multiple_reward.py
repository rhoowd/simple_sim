#!/usr/bin/env python
# coding=utf8
import sys
import re
import matplotlib.pyplot as plt
import logging


if __name__ == '__main__':
    num_file = len(sys.argv)-1
    filename = []
    for i in range(1, num_file+1):
        filename.append(sys.argv[i])
        print sys.argv[i]
    print num_file

    fig = plt.figure()
    for i in range(num_file):
        x = []
        y = []

        f = open(filename[i])

        for line in f:
            if line.split("\t")[1].split(" ")[0] == "reward":
                step = line.split("\t")[2]
                r_str = line.split("\t")[3]
                reward = float(re.sub('[\[\]]', '', r_str))
                print step, reward
                x.append(step)
                y.append(reward)
        plt.plot(x, y)

    plt.xlabel('Training steps', fontsize=16)
    plt.ylabel('Reward', fontsize=16)
    plt.grid(True)
    fig.tight_layout()
    # plt.show()

    # Save to pdf file
    plt.savefig("plot.pdf")
