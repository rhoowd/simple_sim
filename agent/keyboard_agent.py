#!/usr/bin/env python
# coding=utf8

"""
======================================
 :mod:`keyboard_agent` Keyboard Agent
======================================
.. moduleauthor:: Daewoo Kim
.. note:: note...

설명
=====

Keyboard Agent
"""


class Agent(object):

    def __init__(self, env):

        print "Create Keyboard Agent"
        self._env = env
        self._step = 0.5
        self._drone_id = 0

    def learn(self):
        print "learn start"
        action = dict()
        while True:
            s = raw_input('action: ')
            if s == 'a':
                v = (0, -self._step, 0, 0)
            elif s == 's':
                v = (-self._step, 0, 0, 0)
            elif s == 'd':
                v = (0, self._step, 0, 0)
            elif s == 'w':
                v = (self._step, 0, 0, 0)
            elif s == 'q':
                v = (0, 0, 0, -self._step)
            elif s == 'e':
                v = (0, 0, 0, self._step)
            elif s == 'r':
                v = (0, 0, self._step, 0)
            elif s == 'f':
                v = (0, 0, -self._step, 0)
            else:
                print "wrong input"
                continue
            action[self._drone_id] = v
            obs_n, reward_n, done_n, info_n = self._env.step(action)
            print obs_n
