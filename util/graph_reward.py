#!/usr/bin/env python
# coding=utf8
import sys
import re
import matplotlib.pyplot as plt
import logging


if __name__ == '__main__':
    num_file = len(sys.argv)-1
    for i in range(1, num_file+1):
        print sys.argv[i]

    filename = sys.argv[1]

    x = []
    y = []

    f = open(filename)

    short_fn = "g-"+str(filename).split("/")[-1].replace(".txt", "")

    result = logging.getLogger('Result')
    result.setLevel(logging.INFO)
    result_fh = logging.FileHandler(short_fn+".txt")
    result_fm = logging.Formatter('%(message)s')
    result_fh.setFormatter(result_fm)
    result.addHandler(result_fh)

    result.info("# "+short_fn)
    for line in f:
        if line.split("\t")[1].split(" ")[0] == "reward":
            step = line.split("\t")[2]
            r_str = line.split("\t")[3]
            reward = float(re.sub('[\[\]]', '', r_str))
            # print step, reward
            result.info(str(step) + "\t" + str(reward))
            x.append(step)
            y.append(reward)

    # print x, y
    fig = plt.figure()
    plt.plot(x, y, 'r-')
    plt.xlabel('Training steps', fontsize=16)
    plt.ylabel('Reward', fontsize=16)
    plt.grid(True)
    # plt.show()

    # Save to pdf file
    fig.tight_layout()
    plt.savefig(short_fn+".pdf")
