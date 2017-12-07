#!/usr/bin/env python
# coding=utf8
import agents


def config_agent(_flags):
    flags = _flags

    flags.DEFINE_string("agent", "ddpg", "Agent")

    # configurateion for ddpg

    flags.DEFINE_integer("training_step", 400000, "Training time step")
    flags.DEFINE_boolean("load_nn", False, "Load nn from file or not")
    flags.DEFINE_integer("minibatch_size", 128, "Minibatch size")


def get_filename():
    import config
    FLAGS = config.flags.FLAGS

    return "a-"+FLAGS.agent