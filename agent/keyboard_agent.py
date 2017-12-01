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
import pygame
from pygame.locals import *


class Agent(object):

    def __init__(self, env):

        print "Create Keyboard Agent"
        self._env = env
        self._step = 0.1

    def learn(self):
        print "learn start"
        while True:
            v = (0,0,0,0)
            s = raw_input('action: ')
            print s
            if s =='a':
                v = (0, -self._step, 0, 0)
            elif s =='s':
                v = (-self._step, 0, 0, 0)
            elif s =='d':
                v = (0, self._step, 0, 0)
            elif s =='w':
                v = (self._step, 0, 0, 0)
            elif s =='q':
                v = (0, 0, 0, -self._step)
            elif s =='e':
                v = (0, 0, 0, self._step)
            elif s =='r':
                v = (0, 0, self._step, 0)
            elif s =='f':
                v = (0, 0, -self._step, 0)
            else:
                print "wrong input"
                continue

            self._env.step(v)



