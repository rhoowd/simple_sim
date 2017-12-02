#!/usr/bin/env python
# coding=utf8

"""
======================================
 :mod:`core` Core
======================================
.. moduleauthor:: Daewoo Kim
.. note:: note...

설명
=====

Core module includes World
"""
import math
from view import View
import envs.render as render
from envs.config_env import Flags_e

import logging
logger = logging.getLogger('Simsim.core')


class Entity(object):
    def __init__(self, e_id):
        logger.debug(str(e_id) + " is created")
        self._id = e_id
        self._x = 0.0
        self._y = 0.0
        self._z = 0.0
        self._a = 0.0

    @property
    def id(self):
        return self._id

    def get_position(self):
        """
        return the position of entity

        :return: position of entity (x,y,z,a)
        """
        return self._x, self._y, self._z, self._a


class Target(Entity):
    def __init__(self, e_id="target"):
        super(Target, self).__init__(e_id)

    def reset_position(self):
        """
        Reset the position of target (0,0)

        :return:
        """
        self._a = 0.0
        self._x = 0.0
        self._y = 0.0
        self._z = 0.0

    def move(self, dx, dy):
        self._x += dx
        self._y += dy


class Drone(Entity):
    def __init__(self, e_id, n_drone, view):
        super(Drone, self).__init__(e_id)
        self._n_drone = n_drone
        self._view = view
        self._obs = None
        self._init_position_radius = Flags_e.init_position_radius
        self._height_threshold = Flags_e.height_threshold

    def get_obs(self):
        return self._obs

    def reset_position(self):
        """
        The position of drone is reset depending on its id
        Multiple drones form circle with given init radius (r) and face to center (0,0)
        Drone with id 0 is located at (0,-r) point and face to forward (0,1) direction
        Drones are evenly distributed in clockwise manner
        The height of drone (z) is set as r

        :return:
        """
        self._a = 360.0/self._n_drone * self._id
        self._x = -self._init_position_radius * math.sin(math.radians(self._a))
        self._y = -self._init_position_radius * math.cos(math.radians(self._a))
        self._z = self._init_position_radius

    def take_action(self, action):
        """
        Take action for given action
         - Action format: (fb, lr, ud, a)

        :param action: fb: forward/backward, lr: left/right, ud: up/down, a: angle
        :return:
        """
        logger.debug("drone_id: " + str(self._id) + ", Take action: " + str(action))
        fb, lr, ud, da = action
        # Update fb
        self._x += fb * math.sin(math.radians(self._a))
        self._y += fb * math.cos(math.radians(self._a))
        # Update lr
        self._x += lr * math.cos(math.radians(self._a))
        self._y += -lr * math.sin(math.radians(self._a))
        # Update ud, a
        self._a += da
        self._z += ud
        # Drone cannot fly below height threshold
        if self._z < self._height_threshold:
            self._z = self._height_threshold

    def update_obs_from_view(self, target):
        """
        Get observation (coordinate of target in the camera view)

        :param target: the class instance for target from which we can get the position of target

        :return
        """
        tx, ty, _, _ = target.get_position()
        self._obs = self._view.get_view(self._x, self._y, self._z, self._a, tx, ty)


# multi-agent world
class World(object):
    def __init__(self, n_drone=1, target_movement_callback=None):

        self._n_drone = n_drone
        self._target = Target()
        self._drones = []
        self._view = View()
        self.target_movement = target_movement_callback

        # == Create drones instance == #
        for i in range(n_drone):
            self._drones.append(Drone(i, self._n_drone, self._view))

        # == Initiate the position of drone == #
        for drone in self._drones:
            drone.reset_position()

        # == Initiate rendering on canvas == #
        self._render_flag = Flags_e.gui_flag
        if self._render_flag:
            self._render = render.Render()
            self._render.start()
            self._render_cnt = 0

    @property
    def n_drone(self):
        return self._n_drone

    def get_target(self):
        """
        :return: return target object
        """
        return self._target

    def get_drones(self):
        """
        :return: return all drones
        """
        return self._drones

    def step(self, action_n):
        """
        Update state of the world in following sequence
         1. Update target's position
         2. Update drones' position
         3. Update drones' observation
         4. Rendering on canvas

        :param action_n: actions of drones
        :return:
        """
        logger.debug("World Step " + str(action_n))

        # == set action for target
        dx, dy = self.target_movement(self._target, self)
        self._target.move(dx, dy)

        # == Take actions and update observation for each drone == #
        for drone_id, action in action_n.iteritems():
            self._drones[drone_id].take_action(action)
            self._drones[drone_id].update_obs_from_view(self._target)

        # == Rendering == #
        if self._render_flag:
            self._render_cnt += 1
            if self._render_flag == Flags_e.gui_timestep:
                self._render_cnt = 0
                self._render.render(self)

    def reset(self):
        """
        Reset the world. Reset the position of drones and target
        :return:
        """
        self._target.reset_position()
        for drone in self._drones:
            drone.reset_position()

    def stop(self):
        if self._render_flag:
            self._render.stop()
