#!/usr/bin/env python
# coding=utf8

"""
===========================================
 :mod:`ddpg` DDPG
===========================================
.. moduleauthor:: Daewoo Kim
.. note:: note...

설명
=====

Choose action based on ddpg algorithm
"""

from agent.agent import AgentBase
import numpy as np
import tensorflow as tf
from agent.ddpg.ac_network import *
import logging

logger = logging.getLogger("Agent")

initial_noise_scale = 0.8   # scale of the exploration noise process (1.0 is the range of each action dimension)
last_noise_scale = 0.2
noise_decay = 0.9999        # decay rate (per episode) of the scale of the exploration noise process
exploration_mu = 0.0        # mu parameter for the exploration noise process: dXt = theta*(mu-Xt)*dt + sigma*dWt
exploration_theta = 0.15    # theta parameter for the exploration noise process: dXt = theta*(mu-Xt)*dt + sigma*dWt
exploration_sigma = 0.2     # sigma parameter for the exploration noise process: dXt = theta*(mu-Xt    )*dt + sigma*dWt

replay_memory_capacity = int(3e4)  # capacity of experience replay memory
minibatch_size = 512               # size of minibatch from experience replay memory for updates

load_flag = False                        # Use a pre-trained network
guide_flag = False                      # Guide during training
guide_file = "saved/train4-210000"      # Guide weights
save_file = "saved/Energy-weight5"      # Filename for saving the weights during training
naive_flag = False     # Use naive tracking algorithm

training_step = 100000


np.random.seed(0)
np.set_printoptions(threshold=np.nan)


class Agent(AgentBase):

    def __init__(self, env):
        super(Agent, self).__init__(env)
        logger.info("DDPG agent is created")

        tf.reset_default_graph()
        my_graph = tf.Graph()

        with my_graph.as_default():
            self.sess = tf.Session(graph=my_graph)

            self.actor_network = ActorNetwork(
                self.sess, self.obs_dim, self.action_dim,
                self.action_min, self.action_max)

            self.critic_network = CriticNetwork(
                self.sess, self.obs_dim, self.action_dim)

            self.sess.run(tf.global_variables_initializer())
            self.saver = tf.train.Saver()

            if load_flag:
                self.saver.restore(self.sess, None)

        self.replay_buffer = ReplayBuffer()

        # Initialize exploration noise process
        self.noise_process = np.zeros(self.action_dim)
        self.episode = 0
        self.noise_scale = (initial_noise_scale * noise_decay ** self.episode) * (self.action_max - self.action_min)

    def act(self, obs, step):
        """

        :param obs: Observation of one drone with array
        :param step: step elapsed from the start point
        :return: v_fb, v_lr, v_ud, 0
        """

        step = step / 1.
        self.noise_scale = (last_noise_scale + initial_noise_scale * (1-(step/training_step))) * (self.action_max - self.action_min)

        # choose action based on deterministic policy

        # ToDo: Error occurs here
        print obs
        np.array(obs)

        s = np.reshape(obs, self.obs_dim)

        action_for_state = self.actor_network.action_for_state(s)
        logger.info("Best Action: " + str(action_for_state))

        # add temporally-correlated exploration noise to action (using an Ornstein-Uhlenbeck process)
        self.noise_process = exploration_theta * (exploration_mu - self.noise_process) + exploration_sigma * np.random.randn(self.action_dim)

        action_for_state += self.noise_scale * self.noise_process
        action_for_state = np.maximum(action_for_state, self.action_min)
        action_for_state = np.minimum(action_for_state, self.action_max)

        # return action_for_state

        return 0, 0, 0, 0

    def learn(self, train=True):
        """
        Learn

        :param train: True for training and False for test
        :return:
        """
        logger.debug('Start running (train: {})'.format(train))

        # == Initialize == #
        step = 0
        obs_n = self._env.get_obs()

        while True:
            step += 1

            # == Get action == #
            action_n = self.act_n(obs_n, step)

            # == Take on step == #
            obs_n, reward_n, done_n, info_n = self._env.step(action_n)

            logger.debug("Result: "+str(obs_n) + " " + str(reward_n) + " " + str(done_n) + " " + str(info_n))

            if sum(done_n) == self._n_drone:
                self._env.reset()

            if step % 10 == 0:
                s = raw_input('press enter to continue, (q) for quit > ')
                if s == 'q':
                    break
