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

from envs.scenarios.reward import BaseScenario
import logging
logger = logging.getLogger('Simsim.scenario')


class Scenario(BaseScenario):

    def __init__(self):
        super(Scenario, self).__init__()

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
