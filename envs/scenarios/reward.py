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
import config

FLAGS = config.flags.FLAGS

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
        # You can set the reward function in envs/config_env
        if reward_function_name == "reward":
            return self.reward
        elif reward_function_name == "nfp":
            return self.reward_no_fail_penalty
        return None

    def reward(self, drone, world):
        """
        Basic function for reward with energy and

        :param drone: drone object
        :param world: world object
        :return: array with t_x, t_y, and size
        """
        position_weight = FLAGS.position_weight
        size_weight = FLAGS.size_weight

        obs = drone.get_obs()

        size_penalty = self.get_size_penalty(obs['view']['size'])
        position_penalty = self.get_position_penalty(obs['view']['t_x'], obs['view']['t_y'])
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

        if 50 < size <= 200:
            return (-1./150)*(size - 200)
        elif 200 < size <= 250:
            return 0.
        elif 250 < size < 500:
            return (1./250)*(size-250)
        else:  # size < 30 or size > 500
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

    def reward_no_fail_penalty(self, drone, world):
        """
        Basic function for reward with energy and

        :param drone: drone object
        :param world: world object
        :return: array with t_x, t_y, and size
        """
        position_weight = FLAGS.position_weight
        size_weight = FLAGS.size_weight

        obs = drone.get_obs()

        size_penalty = self.get_size_penalty(obs['view']['size'])
        position_penalty = self.get_position_penalty(obs['view']['t_x'], obs['view']['t_y'])
        lost_target = (obs['view']['t_x'] == -1) * 1

        r = (1 - (position_weight * position_penalty + size_weight * size_penalty)) * (1 - lost_target)

        return r
