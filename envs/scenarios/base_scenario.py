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
from envs.core import World
import random
import numpy as np
import logging

logger = logging.getLogger('Simsim.scenario')


# defines scenario upon which the world is built
class BaseScenario(object):
    # create elements of the world
    def __init__(self):
        self._n_drone = 0
        self._fail_cnt = None
        self._fail_threshold = 30

    def make_world(self, n_drone, target_move_callback):
        logger.debug("make world")
        world = World(n_drone, target_move_callback)

        self._n_drone = n_drone
        self._fail_cnt = [0] * self._n_drone

        return world

    def reset_world(self, world):
        self._fail_cnt = [0] * self._n_drone
        world.reset()
        return 0

    def get_reward_function(self, reward_function_name):
        raise NotImplementedError()

    def observation(self, drone, world):
        raise NotImplementedError()

    def info(self, drone, world):
        return 0

    def done(self, drone, world):
        if drone.get_obs()['view']['t_x'] == -1:
            self._fail_cnt[drone.id] += 1
        else:
            self._fail_cnt[drone.id] = 0

        if self._fail_cnt[drone.id] > self._fail_threshold:
            return True

        return False

    def target_move(self, target, world):
        """
        How to move the target for one step
        :param target: target object
        :param world:
        :return: dx, dy - movement in x and y axis
        """
        max_speed = 3

        dx = 2 * max_speed * (random.random() - 0.5)
        dy = 2 * max_speed * (random.random() - 0.5)

        return dx, dy


