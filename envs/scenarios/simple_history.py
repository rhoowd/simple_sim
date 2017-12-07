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
import config

FLAGS = config.flags.FLAGS
logger = logging.getLogger('Simsim.scenario')


class Scenario(BaseScenario):

    def __init__(self):
        super(Scenario, self).__init__()
        self._history_len = FLAGS.history_len
        self._obs = -2 * np.ones((7, self._history_len))
        self.pos_max = np.sqrt(2*32**2)*1.5

    def reset_world(self, world):
        BaseScenario.reset_world(world)

        self._obs = -2 * np.ones((7, self._history_len))
        return 0

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
