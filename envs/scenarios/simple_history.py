#!/usr/bin/env python
# coding=utf8

"""
====================================
 :mod:`simple_history` Simple Scenario
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
from envs.scenarios.simple import Scenario as BaseScenario
import logging
logger = logging.getLogger('Simsim.scenario')


class Scenario(BaseScenario):

    def __init__(self):
        self._n_drone = 0
        self._fail_cnt = None
        self._fail_threshold = 30
        self._history_len = 8
        self._obs = -2 * np.ones((7, self._history_len))
        self.pos_max = np.sqrt(2*32**2)*1.5

    def make_world(self, n_drone, target_move_callback):
        logger.debug("make world")
        world = World(n_drone, target_move_callback)

        self._n_drone = n_drone
        self._fail_cnt = [0] * self._n_drone

        return world

    def reset_world(self, world):
        self._fail_cnt = [0] * self._n_drone
        world.reset()
        self._obs = -2 * np.ones((7, self._history_len))
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

    def reward_d(self, drone, world):
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
        position_weight = 0.5
        size_weight = 0.5

        obs = drone.get_obs()

        size_penalty = self.get_size_penalty(obs['view']['size'])
        position_penalty = self.get_position_penalty(obs['view']['t_x'], obs['view']['t_x'])
        lost_target = (obs['view']['t_x'] == -1) * 1

        r = 1 - (position_weight*position_penalty + size_weight*size_penalty) - lost_target

        return r

    def get_position_penalty(self, cx, cy, radius=16.):
        if cx == -1 or cy == -1:
            return 1.

        distance = np.sqrt((cx - 32)**2 + (cy - 32)**2)  # [0, 45.25)

        if distance > np.sqrt(2*radius**2):  # 22.62
            distance *= 1.5

        return distance/self.pos_max

    def get_size_penalty(self, size):

        if 10 < size < 21:
            return (-1./10)*size + 2
        elif 20 < size < 41:
            return 0.
        elif 40 < size < 401:
            return (1./360)*(size-40)
        else:  #size < 11 or size > 400
            return 1.

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

        self._obs = np.roll(self._obs, -1, axis=1)

        obs = drone.get_obs()

        if self._obs[0][0] == -2:
            for i in range(self._history_len):
                self._obs[0, i] = obs['view']['t_x']
                self._obs[1, i] = obs['view']['t_y']
                self._obs[2, i] = obs['view']['size']
                self._obs[3, i] = obs['drone']['v_fb']
                self._obs[4, i] = obs['drone']['v_lr']
                self._obs[5, i] = obs['drone']['v_ud']
                self._obs[6, i] = obs['drone']['v_a']

        else:
            self._obs[0, -1] = obs['view']['t_x']
            self._obs[1, -1] = obs['view']['t_y']
            self._obs[2, -1] = obs['view']['size']
            self._obs[3, -1] = obs['drone']['v_fb']
            self._obs[4, -1] = obs['drone']['v_lr']
            self._obs[5, -1] = obs['drone']['v_ud']
            self._obs[6, -1] = obs['drone']['v_a']

        ret = np.reshape(self._obs, (self._history_len * 7))  # 7 is the number of obs element

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
        max_speed = 0

        dx = 2 * max_speed * (random.random() - 0.5)
        dy = 2 * max_speed * (random.random() - 0.5)

        return dx, dy
