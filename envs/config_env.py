#!/usr/bin/env python
# coding=utf8


class Flags_e(object):

    # main
    n_drone = 1
    scenario = "simple"

    # core
    height_threshold = 3
    init_position_radius = 8
    gui_flag = True
    gui_time_step = 1
    action_time_step = 0.1

    # render (gui)
    port = 23456

    # view
    view_render_flag = False
    view_width = 64
    view_height = 64
