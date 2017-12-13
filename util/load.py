#!/usr/bin/env python
# coding=utf8

"""
The format of input file should be same as below.
We can get this by "tail -n 5 *" in result/eval folder of simsim
_______________________________________________________________________________________

==> r-1-s-simple_history-pw-1.0-h-8-oa-True-ft-30-a-ddpg-1210133604.txt <==
[evaluation.py:80] 2017-12-10 21:44:00,192	reset   	400000	1
[evaluation.py:81] 2017-12-10 21:44:00,192	trk_error	400000	[31.818353430246127]
[evaluation.py:82] 2017-12-10 21:44:00,192	trk_size	400000	[38.499]
[evaluation.py:83] 2017-12-10 21:44:00,192	distance	400000	[16.168120757908071]
[evaluation.py:84] 2017-12-10 21:44:00,192	reward  	400000	[0.72849999999999848]
_______________________________________________________________________________________

"""
import sys
import re
import collections


def get_data(w, h, o, f, data, type='reward'):
    ret = dict()
    print "# w:", w, " h:", h, " o:", o, " f:", f
    if w is None:
        for k, v in data.iteritems():
            ret[k] = (v[h][o][f]['reward'], v[h][o][f]['trk_error'], v[h][o][f]['trk_size'], v[h][o][f]['distance'],
                      v[h][o][f]['reset'])
    elif h is None:
        for k, v in data[w].iteritems():
            # ret[k] = v[o][f][type]
            ret[k] = (v[o][f]['reward'], v[o][f]['trk_error'], v[o][f]['trk_size'], v[o][f]['distance'],
                      v[o][f]['reset'])
    elif o is None:
        ret['True'] = (data[w][h]['True'][f]['reward'], data[w][h]['True'][f]['trk_error'],
                       data[w][h]['True'][f]['trk_size'], data[w][h]['True'][f]['distance'], data[w][h]['True'][f]['reset'])
        ret['False'] = (data[w][h]['False'][f]['reward'], data[w][h]['False'][f]['trk_error'],
                      data[w][h]['False'][f]['trk_size'],data[w][h]['False'][f]['distance'], data[w][h]['False'][f]['reset'])
    elif f is None:
        for k, v in data[w][h][o].iteritems():
            ret[k] = (v['reward'], v['trk_error'], v['trk_size'], v['distance'], v['reset'])

    ret = collections.OrderedDict(sorted(ret.items()))
    print "Key\tReward\t\tTracking Error\tSize\tDistance\tReset"
    for k, v in ret.iteritems():
        print k,
        if v[0] is None:
            print "\tNone"
        else:
            print "\t%.10f\t%s\t%s\t%s\t%s" % v
    print ""

if __name__ == '__main__':
    if len(sys.argv) == 1:
        filename = "temp1.txt"
    else:
        filename = sys.argv[1]

    n_drone = 0
    scenario = None
    p_w = 0.0
    s_w = 0.0
    history = 0
    oa = True
    ft = 0

    i_data = dict()
    i_data['reset'] = None
    i_data['trk_error'] = None
    i_data['trk_size'] = None
    i_data['distance'] = None
    i_data['reward'] = None
    data = dict()
    for _w in range(0, 11):
        w = _w / 10.
        data[w] = dict()
        for h in range(1, 11, 2):
            data[w][h] = dict()
            for o in ['True', 'False']:
                data[w][h][o] = dict()
                for f in [0, 1, 2, 5, 10, 30, 50]:
                    data[w][h][o][f] = i_data.copy()

    f = open(filename)
    for line in f:
        if line.split(" ")[0] == "==>":
            # print line
            params = line.split(" ")[1]
            n_drone = int(params.split('-')[1])
            scenario = params.split('-')[3]
            p_w = float(params.split('-')[5])
            s_w = 1.0 - p_w
            history = int(params.split('-')[7])
            oa = params.split('-')[9]
            ft = int(params.split('-')[11])
            # print "==>", n_drone, scenario, p_w, s_w, history, oa, ft

        elif line.split(" ")[0][0] == "[":
            # print line
            step = line.split("\t")[2]
            key = line.split("\t")[1].split(" ")[0]
            value = line.split("\t")[3]
            value1 = float(re.sub('[\[\]]', '', value))

            if int(step) == 400000:
                data[p_w][history][oa][ft][key] = value1
                # print step, key, value1, data[p_w][history][oa][ft][key]

    # for i in [1, 3, 5, 7]:
    #     get_data(None, i, 'True', 1, data)

    for i in [1, 3, 5, 7]:
        get_data(0.6, i, 'True', None, data)
    #     get_data(0.6, i, 'False', None, data)
    # get_data(0.6, None, True, 1, data)
    # get_data(0.3, 5, None, 1, data)
    # get_data(0.2, 5, True, None, data)




    # step = line.split("\t")[2]
    #         r_str = line.split("\t")[3]
    #         reward = float(re.sub('[\[\]]', '', r_str))
    #         print step, reward
    #         x.append(step)
    #         y.append(reward)
    #
    # print x, y
    # plt.plot(x, y, 'r-')
    # plt.show()
