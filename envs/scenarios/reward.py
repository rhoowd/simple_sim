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
from envs.scenarios.base_scenario import BaseScenario as BS
import logging
import numpy as np

logger = logging.getLogger('Simsim.scenario')


# defines scenario upon which the world is built
class BaseScenario(BS):
    """
    This is the class for make reward function.
    The observations given by drone are as follows.

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

    """

    def __init__(self):
        super(BaseScenario, self).__init__()

    def get_reward_function(self, reward_function_name=None):
        if reward_function_name == None:
            return self.reward

        return None

    def reward(self, drone, world):
        """
        Basic function for reward with energy and

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

        r = 1 - (position_weight * position_penalty + size_weight * size_penalty) - lost_target

        return r

    def get_position_penalty(self, cx, cy, radius=16.):
        pos_max = np.sqrt(2*32**2)*1.5

        if cx == -1 or cy == -1:
            return 1.

        distance = np.sqrt((cx - 32)**2 + (cy - 32)**2)  # [0, 45.25)

        if distance > np.sqrt(2*radius**2):  # 22.62
            distance *= 1.5

        return distance/pos_max

    def get_size_penalty(self, size):

        if 10 < size < 21:
            return (-1./10)*size + 2
        elif 20 < size < 41:
            return 0.
        elif 40 < size < 401:
            return (1./360)*(size-40)
        else:  # size < 11 or size > 400
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

        obs = drone.get_obs()
        ret = list()
        ret.append(obs['view']['t_x'])
        ret.append(obs['view']['t_y'])
        ret.append(obs['view']['size'])

        return ret
