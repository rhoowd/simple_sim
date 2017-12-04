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
        self._n_drone = 1

    def learn(self):
        print "learn start"

        while True:
            s = raw_input('action or (exit): ')
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
            elif s == 'exit':
                break
            else:
                print "wrong input"
                continue
            action = [0] * 4

            action[0] = v[0]
            action[1] = v[1]
            action[2] = v[2]
            action[3] = v[3]

            action_n = []
            action_n.append(action)

            obs_n, reward_n, done_n, info_n = self._env.step(action_n)
            print "agent:", obs_n, reward_n, done_n
            if sum(done_n) == self._n_drone:
                self._env.reset()
