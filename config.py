#!/usr/bin/env python
# coding=utf8

import tensorflow as tf
import logging
import time
import envs.config_env as config_env
import agents.config_agents as config_agent

flags = tf.flags

# flags for setting
flags.DEFINE_integer("n_drone", 3, "Number of drones")

config_env.config_env(flags)
config_agent.config_agent(flags)


# Make result file with given filename
now = time.localtime()
s_time = "%02d%02d%02d%02d%02d" % (now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
file_name = str(flags.FLAGS.n_drone) + "-"
file_name += config_env.get_filename() + "-" + config_agent.get_filename()
file_name += "-" + s_time
result = logging.getLogger('Result')
result.setLevel(logging.INFO)
result_fh = logging.FileHandler("./result/eval/r-" + file_name + ".txt")
result_fm = logging.Formatter('[%(filename)s:%(lineno)s] %(asctime)s\t%(message)s')
result_fh.setFormatter(result_fm)
result.addHandler(result_fh)
