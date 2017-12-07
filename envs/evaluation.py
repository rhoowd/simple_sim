#!/usr/bin/env python
# coding=utf8

"""
=====================================
 :mod:`evaluation` Evaluation module
=====================================
.. moduleauthor:: Daewoo Kim
.. note:: note...

설명
=====

Evaluation training and test
"""
import numpy as np
import logging

result = logging.getLogger('Result')


class Evaluation(object):

    def __init__(self, world):
        self._world = world
        self._n_drone = world.n_drone
        self._step = 0
        self._flush_time_step = 1000

        # evaluation for all time
        self._reset_cnt = 0
        self._trk_error = [0.0] * self._n_drone
        self._trk_size = [0] * self._n_drone
        self._distance = [0.0] * self._n_drone
        self._reward = [0.0] * self._n_drone

        # evaluation for each time slot
        self._i_reset_cnt = 0
        self._i_trk_error = [0.0] * self._n_drone
        self._i_trk_size = [0] * self._n_drone
        self._i_distance = [0.0] * self._n_drone
        self._i_reward = [0.0] * self._n_drone

    def update(self, reward):
        self._step += 1
        target_position = self._world.get_target().get_position()
        drones = self._world.get_drones()

        for drone in drones:
            obs = drone.get_obs()
            # update size
            self._trk_size[drone.id] += obs['view']['size']
            self._i_trk_size[drone.id] += obs['view']['size']
            # update error
            error = np.sqrt((obs['view']['t_x'] - 32)**2 + (obs['view']['t_y'] - 32)**2)
            self._trk_error[drone.id] += error
            self._i_trk_error[drone.id] += error
            # distance
            drone_position = drone.get_position()
            distance = np.sqrt((target_position[0]-drone_position[0])**2 + (target_position[1]-drone_position[1])**2)
            self._distance[drone.id] += distance
            self._i_distance[drone.id] += distance

        self._reward = np.vstack((self._reward, reward))
        self._reward = np.sum(self._reward, axis=0)
        self._i_reward = np.vstack((self._i_reward, reward))
        self._i_reward = np.sum(self._i_reward, axis=0)

        if self._step % self._flush_time_step == 0:
            self.progress()

        return 0

    def update_reset(self):
        self._reset_cnt += 1
        return 0

    def progress(self):
        result.info("reset   \t" + str(self._step) + "\t" + str(self._i_reset_cnt))
        result.info("trk_error\t" + str(self._step) + "\t" + str([x / self._flush_time_step for x in self._i_trk_error]))
        result.info("trk_size\t" + str(self._step) + "\t" + str([x / float(self._flush_time_step) for x in self._i_trk_size]))
        result.info("distance\t" + str(self._step) + "\t" + str([x / self._flush_time_step for x in self._i_distance]))
        result.info("reward  \t" + str(self._step) + "\t" + str([x / self._flush_time_step for x in self._i_reward]))
        print str(self._step)+"/400000", "reset cnt:", self._i_reset_cnt, \
            "reward:", [x / self._flush_time_step for x in self._i_reward], \
            "size:", self._i_trk_size, "error:", self._i_trk_error

        self._i_reset_cnt = 0
        self._i_trk_error = [0.0] * self._n_drone
        self._i_trk_size = [0] * self._n_drone
        self._i_distance = [0.0] * self._n_drone
        self._i_reward = [0.0] * self._n_drone

    def finish(self):

        return 0

