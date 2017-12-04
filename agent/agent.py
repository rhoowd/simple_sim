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

        self.obs_dim = self._env.get_obs_dim()
        self.action_dim = self._env.get_action_dim()
        self.action_max = self._env.get_action_max()
        self.action_min = self._env.get_action_min()

    def act_n(self, obs_n, step):
        action_n = []
        for drone_id in range(self._n_drone):
            action_n.append(self.act(obs_n[drone_id], step, drone_id))

        return action_n

    @abc.abstractmethod
    def act(self, obs, step, drone_id):
        pass

    @abc.abstractmethod
    def learn(self, train=True):
        """
        Learn

        :param train: True for training and False for test
        :return:
        """
        pass
