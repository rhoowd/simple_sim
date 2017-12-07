#!/usr/bin/env python
# coding=utf8

"""
====================================
 :mod:`envorinment` Environment
====================================
.. moduleauthor:: Daewoo Kim
.. note:: note...

설명
=====

Environment Simsim
"""
import numpy as np
import logging

logger = logging.getLogger('Simsim.env')


class Env(object):

    def __init__(self, world, reset_callback=None, reward_callback=None,
                 observation_callback=None, info_callback=None,
                 done_callback=None):

        logger.debug("Simsim Env")

        self._world = world
        self._drones = world.get_drones()
        self._n_drone = world.n_drone

        # scenario callbacks
        self.reset_callback = reset_callback
        self.reward_callback = reward_callback
        self.observation_callback = observation_callback
        self.info_callback = info_callback
        self.done_callback = done_callback

        self._action_dim = 4
        self._obs_dim = np.reshape(self.get_obs(), -1).shape[0] / self._n_drone
        self._action_max = np.array([20, 20, 0.2, np.pi/5])      # environment configuration4
        self._action_min = np.array([-20, -20, -0.2, -np.pi/5])  # environment configuration5


    def step(self, action_n):
        """
        Agent-environment interaction

        :param action_n: action representation
        :return:
         - observation: Observation
         - reward: Reward
         - done: Terminal flag
         - info: Additional information
        """
        logger.debug("Get action from agent")

        obs_n = []
        reward_n = []
        done_n = []
        info_n = {'n': []}

        # == Advance world state  == #
        self._world.step(action_n)

        # == Get observation == #
        for drone in self._drones:
            obs_n.append(self._get_obs(drone))
            reward_n.append(self._get_reward(drone))
            done_n.append(self._get_done(drone))
            info_n['n'].append(self._get_info(drone))

        return obs_n, reward_n, done_n, info_n

    def reset(self):
        self.reset_callback(self._world)

    def stop(self):
        self._world.stop()

    @property
    def n_drone(self):
        return self._n_drone

    def get_obs(self):
        obs_n = []
        for drone in self._drones:
            obs_n.append(self._get_obs(drone))
        return obs_n

    def get_obs_dim(self):
        return self._obs_dim

    def get_action_dim(self):
        return self._action_dim

    def get_action_max(self):
        return self._action_max

    def get_action_min(self):
        return self._action_min

    # get info used for benchmarking
    def _get_info(self, drone):
        return self.info_callback(drone, self._world)

    # get observation for a particular agent
    def _get_obs(self, drone):
        return self.observation_callback(drone, self._world)

    # get done for a particular agent
    def _get_done(self, drone):
        return self.done_callback(drone, self._world)

    # get reward for a particular agent
    def _get_reward(self, drone):
        return self.reward_callback(drone, self._world)

