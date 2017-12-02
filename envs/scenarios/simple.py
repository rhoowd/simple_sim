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
from envs.core import World
from envs.scenario import BaseScenario
import logging
logger = logging.getLogger('Simsim.scenario')


class Scenario(BaseScenario):
    def make_world(self, n_drone):
        logger.debug("make world")
        world = World(n_drone)
        return world

    def reset_world(self, world):
        return 0
        # # random properties for agents
        # for i, agent in enumerate(world.agents):
        #     agent.color = np.array([0.25,0.25,0.25])
        # # random properties for landmarks
        # for i, landmark in enumerate(world.landmarks):
        #     landmark.color = np.array([0.75,0.75,0.75])
        # world.landmarks[0].color = np.array([0.75,0.25,0.25])
        # # set random initial states
        # for agent in world.agents:
        #     agent.state.p_pos = np.random.uniform(-1,+1, world.dim_p)
        #     agent.state.p_vel = np.zeros(world.dim_p)
        #     agent.state.c = np.zeros(world.dim_c)
        # for i, landmark in enumerate(world.landmarks):
        #     landmark.state.p_pos = np.random.uniform(-1,+1, world.dim_p)
        #     landmark.state.p_vel = np.zeros(world.dim_p)

    def reward(self, drone, world):
        return 0
        # dist2 = np.sum(np.square(agent.state.p_pos - world.landmarks[0].state.p_pos))
        # return -dist2 #np.exp(-dist2)

    def observation(self, drone, world):
        """
        Drone's observation has 7 elements:
          - obs['t_x']: x coordinate of the center of the target
          - obs['t_x']: y coordinate of the center of the target
          - obs['t_w']: width of the target in the camera
          - obs['t_h']: height of the target in the camera
          - obs['size']: size of target (number of pixels of the target)
          - obs['v_h']: resolution height
          - obs['v_w']: resolution width

        :param drone: drone object
        :param world: world object
        :return: array with t_x, t_y, and size
        """
        logger.debug(str(drone.obs))

        obs = drone.obs
        ret = list()
        ret.append(obs['t_x'])
        ret.append(obs['t_y'])
        ret.append(obs['size'])

        return ret

    def target_move(self, target, world):
        return 0
