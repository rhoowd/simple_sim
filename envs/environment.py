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


class Env(object):

    def __init__(self):
        print "Create Simsim Env"

    def step(self, action):
        """
        Agent-environment interaction

        :param action: action representation
        :return:
         - observation: observation
         - reward: reward
         - done: terminal flag
         - info: reset??
        """
        print "step", action
        # == Update world == #

        # == Get observation == #
        obs = 0

        # == Reward == #
        r = 0

        # == Additional process == #
        done = False  # terminate: update to done
        info = None  # reset / loss case (move back): update to info

        return obs, r, done, info

