#!/usr/bin/env python
# coding=utf8


def config_env(_flags):
    flags = _flags

    flags.DEFINE_string("scenario", "simple", "Scenario")

    # core
    flags.DEFINE_float("height_threshold", 3.0, "Height threshold, drone does not fly below this height")
    flags.DEFINE_float("init_position_radius", 8.0, "Initial distance between drone and target")
    flags.DEFINE_boolean("gui_flag", False, "Flag for enable GUI")
    flags.DEFINE_integer("gui_time_spte", 1, "GUI rendering time step")
    flags.DEFINE_float("action_time_step", 0.1, "Action time step, Default we assume drone takes action every 0.1 sec")

    # render (gui)
    flags.DEFINE_integer("gui_port", 23456, "Port number to connect with GUI")

    # view
    flags.DEFINE_boolean("view_render_flag", False, "Rendering during calculation in opengl")
    flags.DEFINE_integer("view_width", 64, "Width of camera view")
    flags.DEFINE_integer("view_height", 64, "Height of camera view")