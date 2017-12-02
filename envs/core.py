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


class Drone(Entity):
    def __init__(self, e_id, n_drone):
        super(Drone, self).__init__(e_id)
        self._n_drone = n_drone
        self._reset_position_radius = 10
        self._view = View()
        self._obs = None

    @property
    def obs(self):
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
        self._x = -self._reset_position_radius * math.sin(math.radians(self._a))
        self._y = -self._reset_position_radius * math.cos(math.radians(self._a))
        self._z = self._reset_position_radius

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
        self._z += ud
        self._a += da

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
    def __init__(self, n_drone=1):

        self._n_drone = n_drone
        self._target = Target()
        self._drones = []

        # == Create drones instance == #
        for i in range(n_drone):
            self._drones.append(Drone(i, self._n_drone))

        # == Initiate the position of drone == #
        for drone in self._drones:
            drone.reset_position()

    @property
    def n_drone(self):
        return self._n_drone

    # return all entities in the world
    def get_entities(self):
        return self._drones + self._targets

    # return all agents controllable by external policies
    def get_targets(self):
        return self._targets

    # return all agents controlled by world scripts
    def get_drones(self):
        return self._drones

    # update state of the world
    def step(self, action_n):
        logger.debug("World Step " + str(action_n))

        # == set action for target

        # == Take actions and update observation for each drone == #
        for drone_id, action in action_n.iteritems():
            self._drones[drone_id].take_action(action)
            self._drones[drone_id].update_obs_from_view(self._target)

