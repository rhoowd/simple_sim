#!/usr/bin/env python
# coding=utf8
import agents


def config_agent(_flags):
    flags = _flags

    flags.DEFINE_string("agent", "ddpg", "Agent")

    # configuration for ddpg

    flags.DEFINE_integer("training_step", 400000, "Training time step")
    flags.DEFINE_boolean("load_nn", False, "Load nn from file or not")
    flags.DEFINE_string("nn_file", "nn-1-s-simple_history-a-ddpg-1207165607-400000", "The name of file for loading")
    flags.DEFINE_integer("minibatch_size", 128, "Minibatch size")
    flags.DEFINE_boolean("train", True, "Training or testing")

def get_filename():
    import config
    FLAGS = config.flags.FLAGS

    return "a-"+FLAGS.agent