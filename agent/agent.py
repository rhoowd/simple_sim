#!/usr/bin/env python
# coding=utf8

"""
===========================================
 :mod:`naive` Naive algorithm for tracking
===========================================
.. moduleauthor:: Daewoo Kim
.. note:: note...

설명
=====

Choose action based on deterministic policy
"""
import logging
import envs
import abc
logger = logging.getLogger("Agent")


class AgentBase(object):

    def __init__(self, env):
        self._env = env
        self._n_drone = env.n_drone

        self._obs_dim = self._env.get_obs_dim()
        self._action_dim = self._env.get_action_dim()
        self._action_max = self._env.get_action_max()
        self._action_min = self._env.get_action_min()

    def _act_n(self, obs_n, step):
        action_n = dict()
        for drone_id in range(self._n_drone):
            action_n[drone_id] = self._act(obs_n[drone_id], step)

        logger.debug("Action: " + str(action_n))

        return action_n

    @abc.abstractmethod
    def _act(self, obs, step):
        pass

    @abc.abstractmethod
    def learn(self, train=True):
        """
        Learn

        :param train: True for training and False for test
        :return:
        """
        pass
