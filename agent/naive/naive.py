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
import numpy as np
logger = logging.getLogger("Agent.naive")


class Agent(object):

    def __init__(self, env):
        logger.info("Naive agent is created")
        self._env = env
        self._n_drone = env.n_drone

        self._obs_dim = self._env.get_obs_dim()
        self._action_dim = self._env.get_action_dim()
        self._action_max = self._env.get_action_max()
        self._action_min = self._env.get_action_min()

    def act_n(self, obs_n, step):
        action_n = dict()
        for drone_id in range(self._n_drone):
            action_n[drone_id] = self.act(obs_n[drone_id], step)

        logger.debug("Action: " + str(action_n))

        return action_n

    def act(self, obs, step):

        x_pos = obs[0]
        y_pos = obs[1]
        z_pos = obs[2]

        if x_pos < 24:
            v_lr = -0.6
        elif x_pos < 16:
            v_lr = -1.2
        elif x_pos > 40:
            v_lr = 0.6
        elif x_pos > 48:
            v_lr = -1.2
        else:
            v_lr = 0

        if y_pos < 24:
            v_fb = 0.6
        elif y_pos < 16:
            v_fb = 1.2
        elif y_pos > 40:
            v_fb = -0.6
        elif y_pos > 48:
            v_fb = -1.2
        else:
            v_fb = 0

        if z_pos < 3.5:
            v_ud = 0.2
        else:
            v_ud = 0

        return v_fb, v_lr, v_ud, 0


    def learn(self, train=True):
        """
        Learn

        :param train: True for training and False for test
        :return:
        """
        logger.debug('Start running (train: {})'.format(train))

        # == Initialize == #
        step = 0
        obs_n = self._env.get_obs()

        while True:
            step += 1

            # == Get action == #
            action_n = self.act_n(obs_n, step)

            # == Take on step == #
            obs_n, reward_n, done_n, info_n = self._env.step(action_n)

            logger.debug("Result: "+str(obs_n) + " " + str(reward_n) + " " + str(done_n) + " " + str(info_n))

            if sum(done_n) == self._n_drone:
                self._env.reset()

            if step % 10 == 0:
                s = raw_input('press enter to continue, (q) for quit > ')
                if s == 'q':
                    break
