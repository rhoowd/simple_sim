#!/usr/bin/env python
# coding=utf8

"""
====================================
 :mod:`simple` Simple Scenario
====================================
.. moduleauthor:: Daewoo Kim
.. note:: note...

설명
=====

Simple scenario
"""

import numpy as np
import math
import random
from envs.core import World
from envs.scenario import BaseScenario
import logging
logger = logging.getLogger('Simsim.scenario')


class Scenario(BaseScenario):

    def __init__(self):
        self._n_drone = 0
        self._fail_cnt = None
        self._fail_threshold = 10

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

    def reward(self, drone, world):
        """
        Drone's observation has 11 elements:
          - obs['drone']['v_fb']: velocity for forward/backward
          - obs['drone']['v_lr']: velocity for left/right
          - obs['drone']['v_ud']: velocity for up/down
          - obs['drone']['v_a']: Angular rate

          - obs['view']['t_x']: x coordinate of the center of the target
          - obs['view']['t_x']: y coordinate of the center of the target
          - obs['view']['t_w']: width of the target in the camera
          - obs['view']['t_h']: height of the target in the camera
          - obs['view']['size']: size of target (number of pixels of the target)
          - obs['view']['v_h']: resolution height
          - obs['view']['v_w']: resolution width

        :param drone: drone object
        :param world: world object
        :return: array with t_x, t_y, and size
        """
        obs = drone.get_obs()
        if obs['view']['t_x'] == -1:  # There is no target in the view
            return 0

        view_area = obs['view']['v_w'] * obs['view']['v_h']
        distance_from_center = math.sqrt(math.pow(obs['view']['t_x']-obs['view']['v_w']/2, 2) + math.pow(obs['view']['t_y']-obs['view']['v_h']/2, 2))

        ret = 0
        if distance_from_center < obs['view']['v_w'] * 0.15:
            if view_area * 0.05 < obs['view']['size'] < view_area * 0.2:
                ret = 1
        else:
            ret = 0.1

        return ret

    def observation(self, drone, world):
        """
        Drone's observation has 11 elements:
          - obs['drone']['v_fb']: velocity for forward/backward
          - obs['drone']['v_lr']: velocity for left/right
          - obs['drone']['v_ud']: velocity for up/down
          - obs['drone']['v_a']: Angular rate

          - obs['view']['t_x']: x coordinate of the center of the target
          - obs['view']['t_x']: y coordinate of the center of the target
          - obs['view']['t_w']: width of the target in the camera
          - obs['view']['t_h']: height of the target in the camera
          - obs['view']['size']: size of target (number of pixels of the target)
          - obs['view']['v_h']: resolution height
          - obs['view']['v_w']: resolution width

        :param drone: drone object
        :param world: world object
        :return: array with t_x, t_y, and size
        """
        # logger.debug(str(drone.get_obs()))

        obs = drone.get_obs()
        ret = list()
        ret.append(obs['view']['t_x'])
        ret.append(obs['view']['t_y'])
        ret.append(obs['view']['size'])

        return ret

    def done(self, drone, world):

        if drone.get_obs()['view']['t_x'] == -1:
            self._fail_cnt[drone.id] += 1
        else:
            self._fail_cnt[drone.id] = 0

        if self._fail_cnt[drone.id] > self._fail_threshold:
            return True

        return False

    def info(self, drone, world):
        return 0

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
