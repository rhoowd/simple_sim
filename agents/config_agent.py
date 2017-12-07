#!/usr/bin/env python
# coding=utf8
import agents


def config_agent(_flags):
    flags = _flags

    flags.DEFINE_string("agent", "naive", "Agent")
    agents.load("naive/config.py").config(flags)


def get_filename():
    import config
    FLAGS = config.flags.FLAGS

    return "a-"+FLAGS.agent + agents.load("naive/config.py").get_filename()