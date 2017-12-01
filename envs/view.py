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
import time


class View(object):
    def __init__(self):
        self._color_red = (1,0,0)
        self._surfaces = ((0,1,2,3), (3,2,7,6), (6,7,5,4),(4,5,1,0),(1,5,7,2),(4,0,3,6))
        self._vertices = ((1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,-1),(1,-1,1),(1,1,1),(-1,-1,1),(-1,1,1))
        self._edges = ((0,1), (0,3), (0,4),(2,1),(2,3),(2,7),(6,3),(6,4),(6,7),(5,1),(5,4),(5,7))
        self._width = 80
        self._height = 60

        pygame.init()
        self._display = (self._width, self._height)
        pygame.display.set_mode(self._display, DOUBLEBUF | OPENGL)

    def get_view(self):

        fb = 0.0
        lr = -2.0
        ud = 10
        print "view step"

        # Camera angle: face upward 20 degree from vertical down
        glLoadIdentity()
        gluPerspective(45, (self._display[0] / self._display[1]), 0.1, 50.0)

        # Camera angle: face upward 20 degree from vertical down
        glRotatef(-20, 1, 0, 0)

        # Drone's yaw
        glRotatef(90, 0, 1, 0)

        # Drone position
        glTranslatef(-lr, -fb, -ud)

        # Target position
        glTranslatef(0.0, 0.0, 0.0)




        # glRotatef(20, 0, 0, 1)
        #


        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.draw_target()
        pygame.display.flip()
        # pygame.display.flip()  # need to call two times to update

        a = (GLubyte * (self._width * self._height))(0)
        glReadPixels(0, 0, self._width, self._height, GL_RED, GL_UNSIGNED_BYTE, a)

        for i in range(self._height):
            for j in range(self._width):
                if a[(self._height-i-1) * self._width + j] > 0:
                    print 1,
                else:
                    print 0,
            print " "

        print " "
        print " "

    def draw_target(self):
        glBegin(GL_QUADS)
        for surface in self._surfaces:
            for vertex in surface:
                glColor3fv(self._color_red)
                glVertex3fv(self._vertices[vertex])
        glEnd()

        glBegin(GL_LINES)
        for edge in self._edges:
            for vertex in edge:
                glVertex3fv(self._vertices[vertex])
        glEnd()
