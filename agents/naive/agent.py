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
from agents.agent import AgentBase
import logging

logger = logging.getLogger("Agent")


class Agent(AgentBase):

    def __init__(self, env):
        super(Agent, self).__init__(env)
        logger.info("Naive agent is created")

    def act(self, obs, step, drone_id, train=True):

        action = [0] * self.action_dim
        x_pos = obs[0]
        y_pos = obs[1]
        z_pos = obs[2]

        if x_pos < 24:
            v_lr = -1
        elif x_pos < 16:
            v_lr = -2
        elif x_pos > 40:
            v_lr = 1
        elif x_pos > 48:
            v_lr = -2
        else:
            v_lr = 0

        if y_pos < 24:
            v_fb = 1
        elif y_pos < 16:
            v_fb = 2
        elif y_pos > 40:
            v_fb = -1
        elif y_pos > 48:
            v_fb = -2
        else:
            v_fb = 0

        if z_pos < 3.5:
            v_ud = 2
        else:
            v_ud = 0

        action[0] = v_fb
        action[1] = v_lr
        action[2] = v_ud
        action[3] = 0

        return action

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
            logger.debug("Action: " + str(action_n))

            # == Take on step == #
            obs_n, reward_n, done_n, info_n = self._env.step(action_n)

            logger.debug("Result: "+str(obs_n) + " " + str(reward_n) + " " + str(done_n) + " " + str(info_n))

            if sum(done_n) == self._n_drone:
                self._env.reset()

            if step % 10 == 0:
                s = raw_input('press enter to continue, (q) for quit > ')
                if s == 'q':
                    break
