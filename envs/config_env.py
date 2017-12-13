#!/usr/bin/env python
# coding=utf8

def config_env(_flags):
    flags = _flags

    # Scenario
    flags.DEFINE_string("scenario", "simple", "Scenario")

    # Reward
    flags.DEFINE_string("reward", "reward", "Reward")
    flags.DEFINE_float("position_weight", 0.5, "The position for size in reward function")
    flags.DEFINE_float("size_weight", 0.5, "The weight for size in reward function")

    # Reset and failure
    flags.DEFINE_integer("fail_threshold", 30, "When terminate episode")

    # Observation
    flags.DEFINE_integer("history_len", 8, "How many previous steps we look back")
    flags.DEFINE_boolean("obs_with_action", True, "Observation includes action or only image result")

    # core
    flags.DEFINE_float("height_threshold", 3.0, "Height threshold, drone does not fly below this height")
    flags.DEFINE_float("init_position_radius", 8.0, "Initial distance between drone and target")
    flags.DEFINE_boolean("gui_flag", False, "Flag for enable GUI")
    flags.DEFINE_integer("gui_time_step", 1, "GUI rendering time step")
    flags.DEFINE_float("action_time_step", 0.1, "Action time step, Default we assume drone takes action every 0.1 sec")

    # render (gui)
    flags.DEFINE_integer("gui_port", 23456, "Port number to connect with GUI")

    # view
    flags.DEFINE_boolean("view_render_flag", False, "Rendering during calculation in opengl")
    flags.DEFINE_integer("view_width", 64, "Width of camera view")
    flags.DEFINE_integer("view_height", 64, "Height of camera view")


def get_filename():
    import config
    FLAGS = config.flags.FLAGS

    return "s-"+FLAGS.scenario+"-pw-"+str(FLAGS.position_weight)+"-h-"+str(FLAGS.history_len)+\
           "-oa-"+str(FLAGS.obs_with_action)+"-ft-"+str(FLAGS.fail_threshold)+"-rw-"+str(FLAGS.reward)
