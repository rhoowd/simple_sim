#!/usr/bin/env python
# coding=utf8

"""
====================================
 :mod:`scenario` Scenario
====================================
.. moduleauthor:: Daewoo Kim
.. note:: note...

설명
=====

Environment Simsim
"""


# defines scenario upon which the world is built
class BaseScenario(object):
    # create elements of the world
    def make_world(self, n_drone):
        raise NotImplementedError()

    # create initial conditions of the world
    def reset_world(self, world):
        raise NotImplementedError()

    def reward(self, drone, world):
        raise NotImplementedError()

    def observation(self, drone, world):
        raise NotImplementedError()

    def target_move(self, target, world):
        raise NotImplementedError()
