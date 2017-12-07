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

from agents.agent import AgentBase
import numpy as np
import tensorflow as tf
from agents.ddpg.ac_network import *
import logging
import config

FLAGS = config.flags.FLAGS
logger = logging.getLogger("Agent")
result = logging.getLogger('Result')

initial_noise_scale = 0.8   # scale of the exploration noise process (1.0 is the range of each action dimension)
last_noise_scale = 0.2
noise_decay = 0.9999        # decay rate (per episode) of the scale of the exploration noise process
exploration_mu = 0.0        # mu parameter for the exploration noise process: dXt = theta*(mu-Xt)*dt + sigma*dWt
exploration_theta = 0.15    # theta parameter for the exploration noise process: dXt = theta*(mu-Xt)*dt + sigma*dWt
exploration_sigma = 0.2     # sigma parameter for the exploration noise process: dXt = theta*(mu-Xt    )*dt + sigma*dWt

replay_memory_capacity = int(3e4)  # capacity of experience replay memory
minibatch_size = FLAGS.minibatch_size             # size of minibatch from experience replay memory for updates

load_flag = FLAGS.load_nn                      # Use a pre-trained network
save_file = "result/nn/nn-" + config.file_name  # Filename for saving the weights during training

training_step = FLAGS.training_step


np.random.seed(0)
np.set_printoptions(threshold=np.nan)


class Agent(AgentBase):

    def __init__(self, env):
        super(Agent, self).__init__(env)
        logger.info("DDPG agent is created")

        print "1", minibatch_size, training_step

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

    def act(self, obs, step, drone_id):
        """

        :param obs: Observation of one drone with array
        :param step: step elapsed from the start point
        :return: v_fb, v_lr, v_ud, 0
        """

        step = step / 1.
        self.noise_scale = (last_noise_scale + initial_noise_scale * (1-(step/training_step))) * (self.action_max - self.action_min)

        # choose action based on deterministic policy

        # ToDo: Error occurs here
        np.array(obs)

        s = np.reshape(obs, self.obs_dim)

        action = self.actor_network.action_for_state(s[None])

        # add temporally-correlated exploration noise to action (using an Ornstein-Uhlenbeck process)
        self.noise_process = exploration_theta * (exploration_mu - self.noise_process) + exploration_sigma * np.random.randn(self.action_dim)

        action += self.noise_scale * self.noise_process
        action = np.maximum(action, self.action_min)
        action = np.minimum(action, self.action_max)

        action = np.squeeze(action)

        logger.debug("Action (Drone " + str(drone_id) + "): " + str(action))

        return action

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
        obs_single = np.squeeze(obs_n)  # This is for init # TODO  obs_single = np.squeeze(obs_n) is more natural
        acc_reward = 0
        prev_reset_step = 0
        reset_cnt = 0
        acc_reset_step = 0

        while True:
            step += 1

            # == Get action == #
            action_n = self.act_n(obs_n, step)

            # == Take on step == #
            obs_n, reward_n, done_n, info_n = self._env.step(action_n)
            logger.debug("Result: "+str(obs_n) + " " + str(reward_n) + " " + str(done_n) + " " + str(info_n))

            # == Reset decision == #
            # TODO: Where is proper location of this? What is impact of reset
            # TODO: Need to discuss with KH


            # == DDPG start == #

            # Erase one entry in replay buffer when it is full
            if len(self.replay_buffer.replay_memory) == replay_memory_capacity:
                self.replay_buffer.erase()

            obs_single_next = np.squeeze(obs_n)
            action_single = np.squeeze(action_n)
            reward_single = reward_n[0]
            # print obs_single, action_single, reward_single, obs_single_next

            self.replay_buffer.add_to_memory((obs_single, action_single, reward_single, obs_single_next,
                                              0.0 if sum(done_n) == self._n_drone else 1.0))
            # is next_observation a terminal state? means that sum(done_n) == self._n_drone
            # 0.0 if done and not env.env._past_limit() else 1.0))

            if sum(done_n) == self._n_drone:
                self._env.reset()
                obs_n = self._env.get_obs()
                obs_single = np.squeeze(obs_n)  # This is for init
                logger.debug('({}/{}) RESET step {}'.format(step, training_step, step - prev_reset_step))
                reset_cnt += 1
                acc_reset_step += (step - prev_reset_step)
                prev_reset_step = step
                continue

            # update network weights to fit a minibatch of experience
            if len(self.replay_buffer.replay_memory) >= minibatch_size*5:
                # grab N (s,a,r,s') tuples from replay memory
                minibatch = self.replay_buffer.sample_from_memory()

                # update the critic and actor params using mean-square value error and deterministic policy gradient, respectively
                sugg_action = self.actor_network.action_for_state(np.asarray([elem[0] for elem in minibatch]))
                q_sugg_action = self.critic_network.q_for_given_action(np.asarray([elem[0] for elem in minibatch]),sugg_action)

                gradient = self.critic_network.grads_for_action(np.asarray([elem[0] for elem in minibatch]),
                                                             sugg_action)

                target_action_next_state = self.actor_network.target_action_for_next_state(np.asarray([elem[3] for elem in minibatch]))

                _ = self.critic_network.training_critic(np.asarray([elem[0] for elem in minibatch]),
                                                        np.asarray([elem[1] for elem in minibatch]),
                                                        target_action_next_state,
                                                        np.asarray([elem[2] for elem in minibatch]),
                                                        np.asarray([elem[3] for elem in minibatch]),
                                                        np.asarray([elem[4] for elem in minibatch]))
                _ = self.actor_network.training_actor(np.asarray([elem[0] for elem in minibatch]),
                                                      gradient)

                # update slow actor and critic targets towards current actor and critic
                _ = self.actor_network.training_target_actor()
                _ = self.critic_network.training_target_critic()

            obs_single = obs_single_next

            # == Print progress == #
            acc_reward += reward_single
            if step % 1000 == 0:
                if reset_cnt == 0:
                    reset_cnt = 1
                logger.info(
                    '({}/{}) Avg. reward: {}, Avg. reset step {}'.format(step, training_step, acc_reward / 1000.0,
                                                                         acc_reset_step / reset_cnt))
                result.info(
                    '({}/{}) Avg. reward: {}, Avg. reset step {}'.format(step, training_step, acc_reward / 1000.0,
                                                                         acc_reset_step / reset_cnt))

                acc_reward = 0
                reset_cnt = 0
                acc_reset_step = 0

                self.saver.save(self.sess, save_file, step)

            # == Key board interrupt enable == #
            # if step % 100 == 0:
            #     logger.info('{}/{}'.format(step, training_step))
            #
            #     s = raw_input('press enter to continue, (q) for quit > ')
            #     if s == 'q':
            #         break

            if step > training_step:
                break