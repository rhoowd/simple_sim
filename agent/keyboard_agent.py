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

    def learn(self):
        print "learn start"
        pygame.init()
        width = 80
        height = 60
        display = (width, height)
        pygame.display.set_mode(display)
        quit_flag = False
        key_flag = False
        while True:
            if quit_flag:
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit_flag = True

                if event.type == KEYDOWN:
                    key_flag = True
                    if event.key == K_LEFT:
                        action = "left"
                    if event.key == K_RIGHT:
                        action = "right"
                    if event.key == K_UP:
                        action = "up"
                    if event.key == K_DOWN:
                        action = "down"
                    if event.key == ord('a'):
                        action = "a"
                    if event.key == ord('d'):
                        action = "d"
                    if event.key == ord('w'):
                        action = "w"
                    if event.key == ord('s'):
                        action = "s"
                    print action

            if key_flag:
                key_flag = False
                obs_n, reward, done, info = self._env.step(action)
                print obs_n, reward, done





