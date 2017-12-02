#!/usr/bin/env python
# coding=utf8

"""
======================================
 :mod:`view` Camera view from drone
======================================
.. moduleauthor:: Daewoo Kim
.. note:: note...

설명
=====

Camera view from drone

참고: http://blog.naver.com/PostView.nhn?blogId=samsjang&logNo=220717571305&categoryNo=81&parentCategoryNo=0&viewDate=&currentPage=1&postListTopCurrentPage=1&from=postView&userTopListOpen=true&userTopListCount=10&userTopListManageOpen=false&userTopListCurrentPage=1
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np
from envs.config_env import Flags_e
import logging
logger = logging.getLogger('Simsim.view')


class View(object):
    def __init__(self):
        self._width = Flags_e.view_width
        self._height = Flags_e.view_height
        self._display = (self._width, self._height)
        # phi: camera angle (front: 0, downward: 90, Bug for 90 -> recommend 89 for example)
        self._phi = 45

        # == init pygame to get image view == #
        pygame.init()
        pygame.display.set_mode(self._display, DOUBLEBUF | OPENGL)

        # == View rendering flag:
        # This module does not work when this flag is True for rendering image
        self._view_render_flag = Flags_e.view_render_flag

    def get_view(self, dx, dy, dz, da, tx, ty):
        """
        Get the position of drone and target, and return result
        (result: target's coordinate and size in the view)
        The output coordination (0, 0) means target is located at left up in the view

        :param dx: drone's position x
        :param dy: drone's position y
        :param dz: drone's position z
        :param da: drone's position a
        :param tx: target's position x
        :param ty: target's position y

        :return obs is dict
          - obs['t_x']: x coordinate of the center of the target
          - obs['t_x']: y coordinate of the center of the target
          - obs['t_w']: width of the target in the camera
          - obs['t_h']: height of the target in the camera
          - obs['size']: size of target (number of pixels of the target)
          - obs['v_h']: resolution height
          - obs['v_w']: resolution width
        """

        # == Init opengl view == #
        glLoadIdentity()

        # == Set camera setting and position == #
        gluPerspective(45, (self._display[0] / self._display[1]), 0.1, 50.0)
        c_pos = [dx, dy, dz]
        v_dir = [0]*3
        v_dir[0] = math.sin(math.radians(da)) * math.cos(math.radians(self._phi))
        v_dir[1] = math.cos(math.radians(da)) * math.cos(math.radians(self._phi))
        v_dir[2] = -math.sin(math.radians(self._phi))
        gluLookAt(c_pos[0], c_pos[1], c_pos[2], c_pos[0] + v_dir[0], c_pos[1] + v_dir[1], c_pos[2] + v_dir[2], 0, 0, 1)

        # == Set target position == #
        glTranslatef(tx, ty, 0.0)

        # == Make image view for get result == #
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.draw_target()
        if self._view_render_flag:
            pygame.display.flip()

        # == Get image result from opengl view == #
        view = (GLubyte * (self._width * self._height))(0)
        glReadPixels(0, 0, self._width, self._height, GL_RED, GL_UNSIGNED_BYTE, view)

        # == Derive result (Target's coordinate and size in the view) ==#
        image = np.asarray(view)
        image = image.reshape([-1, self._width])
        y, x = np.nonzero(image)

        obs = dict()
        obs['v_h'] = self._height
        obs['v_w'] = self._width

        if len(x) < 1:  # object not detected
            logger.debug("object not detected")
            obs['t_x'] = -1
            obs['t_y'] = -1
            obs['t_h'] = 0
            obs['t_w'] = 0
            obs['size'] = 0
        else:
            obs['t_x'] = (min(x) + max(x) + 1) / 2
            obs['t_y'] = self._height - ((min(y) + max(y) + 1) / 2)
            obs['t_h'] = max(x) - min(x) + 1
            obs['t_w'] = max(y) - min(y) + 1
            obs['size'] = np.count_nonzero(image)

        return obs

    def draw_target(self):
        """
        Drawing target as red cube with size (1*1*1)
        :return:
        """
        color_red = (1, 0, 0)
        surfaces = ((0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4), (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6))
        vertices = ((1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1), (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1))
        edges = ((0, 1), (0, 3), (0, 4), (2, 1), (2, 3), (2, 7), (6, 3), (6, 4), (6, 7), (5, 1), (5, 4), (5, 7))

        glBegin(GL_QUADS)
        for surface in surfaces:
            for vertex in surface:
                glColor3fv(color_red)
                glVertex3fv(vertices[vertex])
        glEnd()

        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()
