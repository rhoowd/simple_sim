#!/usr/bin/env python
# coding=utf8
import agents


def config_agent(_flags):
    flags = _flags

    flags.DEFINE_string("agent", "naive", "Agent")


def get_filename():
    import config
    FLAGS = config.flags.FLAGS

    return "a-"+FLAGS.agent