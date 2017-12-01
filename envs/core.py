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
from view import View


class Entity(object):
    def __init__(self, e_id):
        print e_id, "is created"
        self._id = e_id
        self._x = 0
        self._y = 0
        self._z = 0
        self._a = 0

    @property
    def id(self):
        return self._id

    def get_position(self):
        return self._x, self._y, self._z, self._a

    def move(self, dx, dy, dz, da):
        self._x += dx
        self._y += dy
        self._z += dz
        self._a += da


# properties of target entities
class Target(Entity):
    def __init__(self, e_id="target"):
        super(Target, self).__init__(e_id)


# properties of drone entities
class Drone(Entity):
    def __init__(self, e_id, n_drone):
        super(Drone, self).__init__(e_id)
        self._n_drone = n_drone
        self._reset_position_radius = 1
        # action
        # self.action = Action()
        # script behavior to execute
        # self.action_callback = None
        self._view = View()

    def reset_position(self):
        print "reset"

    def take_action(self, action, target):

        self._view.get_view(action)

# multi-agent world
class World(object):
    def __init__(self, n_drone=1):
        # list of drone and target
        self._n_drone = n_drone
        self.target = Target()
        self.drones = []
        for i in range(n_drone):
            self.drones.append(Drone(i, self._n_drone))

        # position dimensionality
        # self.dim_p = 3

        # simulation timestep
        # self.dt = 0.1

    # return all entities in the world
    def get_entities(self):
        return self.drones + self.targets

    # return all agents controllable by external policies
    def get_targets(self):
        return self.targets

    # return all agents controlled by world scripts
    def get_drones(self):
        return self.drones

    # update state of the world
    def step(self,action):
        print "World Step", action
        # == set action for target
        for drone in self.drones:
            print "droneid:", drone.id
            drone.take_action(action,None)
        # == set actions for drones

        # for agent in self.scripted_agents:
        #     agent.action = agent.action_callback(agent, self)
