#!/usr/bin/env python
# coding=utf8

import numpy as np
import tensorflow as tf
from collections import deque
import random

gamma = 0.99  # reward discount factor

h1_actor = 32  # hidden layer 1 size for the actor
h2_actor = 32  # hidden layer 2 size for the actor
h3_actor = 32  # hidden layer 3 size for the actor

h1_critic = 32  # hidden layer 1 size for the critic
h2_critic = 32  # hidden layer 2 size for the critic
h3_critic = 32  # hidden layer 3 size for the critic

lr_actor = 1e-5  # learning rate for the actor
lr_critic = 1e-4  # learning rate for the critic
lr_decay = 1  # learning rate decay (per episode)

tau = 1e-2  # soft target update rate
replay_memory_capacity = int(3e4)  # capacity of experience replay memory
minibatch_size = 128  # size of minibatch from experience replay memory for updates

np.set_printoptions(threshold=np.nan)


class ReplayBuffer:
    def __init__(self):
        self.replay_memory = deque(maxlen=replay_memory_capacity)

    def add_to_memory(self, experience):
        self.replay_memory.append(experience)

    def sample_from_memory(self):
        return random.sample(self.replay_memory, minibatch_size)

    def erase(self):
        self.replay_memory.popleft()


class ActorNetwork:
    def __init__(self, sess, state_dim, action_dim, action_min, action_max):

        self.sess = sess
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.action_min = action_min
        self.action_max = action_max

        # placeholders
        self.state_ph = tf.placeholder(dtype=tf.float32, shape=[None, state_dim])
        self.q_ph = tf.placeholder(dtype=tf.float32, shape=[None,1])
        self.next_state_ph = tf.placeholder(dtype=tf.float32, shape=[None, state_dim])
        self.grads_ph = tf.placeholder(dtype=tf.float32, shape=[None, action_dim])

        # indicators (go into target computation)
        self.is_training_ph = tf.placeholder(dtype=tf.bool, shape=())  # for dropout
        episodes = tf.Variable(0.0, trainable=False, name='episodes')

        # actor network
        with tf.variable_scope('actor'):
            # Policy's outputted action for each state_ph (for generating actions and training the critic)
            self.actions = self.generate_actor_network(self.state_ph, trainable = True)

        # slow target actor network
        with tf.variable_scope('slow_target_actor'):
            # Slow target policy's outputted action for each next_state_ph (for training the critic)
            # use stop_gradient to treat the output values as constant targets when doing backprop
            self.slow_target_next_actions = tf.stop_gradient(
                self.generate_actor_network(self.next_state_ph, trainable = False))

        # actor loss function (mean Q-values under current policy with regularization)
        self.actor_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='actor')

        var_grads = tf.gradients(self.actions, self.actor_vars, -self.grads_ph)
        self.actor_train_op = tf.train.AdamOptimizer(lr_actor * lr_decay).apply_gradients(zip(var_grads,self.actor_vars))
        slow_target_actor_vars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='slow_target_actor')

        # update values for slowly-changing targets towards current actor and critic
        update_slow_target_ops_a = []
        for i, slow_target_actor_var in enumerate(slow_target_actor_vars):
            update_slow_target_actor_op = slow_target_actor_var.assign(
                tau * self.actor_vars[i] + (1 - tau) * slow_target_actor_var)
            update_slow_target_ops_a.append(update_slow_target_actor_op)
        self.update_slow_targets_op_a = tf.group(*update_slow_target_ops_a)


    # will use this to initialize both the actor network its slowly-changing target network with same structure
    def generate_actor_network(self, s, trainable):
        hidden = tf.layers.dense(s, h1_actor, activation=tf.nn.elu,
                                 kernel_regularizer=tf.contrib.layers.l2_regularizer(0.01),
                                 kernel_initializer=tf.contrib.layers.variance_scaling_initializer(),
                                 use_bias=True, trainable=trainable, name='dense_a', )

        hidden_2 = tf.layers.dense(hidden, h2_actor, activation=tf.nn.elu,
                                   kernel_regularizer=tf.contrib.layers.l2_regularizer(0.01),
                                   kernel_initializer=tf.contrib.layers.variance_scaling_initializer(),
                                   trainable=trainable, name='dense_a1',
                                   use_bias=True)

        hidden_3 = tf.layers.dense(hidden_2, h3_actor, activation=tf.nn.elu,
                                   kernel_regularizer=tf.contrib.layers.l2_regularizer(0.01),
                                   kernel_initializer=tf.contrib.layers.variance_scaling_initializer(),
                                   trainable=trainable, name='dense_a2',
                                   use_bias=True)

        actions_unscaled = tf.layers.dense(hidden_3, self.action_dim,
                                           kernel_regularizer=tf.contrib.layers.l2_regularizer(0.01),
                                           kernel_initializer=tf.contrib.layers.variance_scaling_initializer(),
                                           trainable=trainable, name='dense_a3',
                                           use_bias=True)

        # bound the actions to the valid range
        actions = self.action_min + tf.nn.sigmoid(actions_unscaled) * (self.action_max - self.action_min)
        return actions

    def action_for_state(self, state_ph):
        return self.sess.run(self.actions,
                             feed_dict={self.state_ph: state_ph/10, self.is_training_ph: False})

    def target_action_for_next_state(self, next_state_ph):

        return self.sess.run(self.slow_target_next_actions,
                             feed_dict={self.next_state_ph: next_state_ph/10, self.is_training_ph: False})

    def training_actor(self, state_ph, grads_ph):

        return self.sess.run(self.actor_train_op,
                             feed_dict={self.state_ph: state_ph/10,
                                        self.grads_ph: grads_ph,
                                        self.is_training_ph: True})


    def training_target_actor(self):

        return self.sess.run(self.update_slow_targets_op_a,
                             feed_dict={self.is_training_ph: False})


class CriticNetwork:
    def __init__(self, sess, state_dim, action_dim):

        self.sess = sess
        self.state_dim = state_dim
        self.action_dim = action_dim

        # placeholders
        self.state_ph = tf.placeholder(dtype=tf.float32, shape=[None, state_dim])
        self.given_action_ph = tf.placeholder(dtype=tf.float32, shape=[None, action_dim])
        self.suggested_action_ph = tf.placeholder(dtype=tf.float32, shape=[None, action_dim])
        self.slow_target_action_ph = tf.placeholder(dtype=tf.float32, shape=[None, action_dim])
        self.reward_ph = tf.placeholder(dtype=tf.float32, shape=[None])
        self.next_state_ph = tf.placeholder(dtype=tf.float32, shape=[None, state_dim])
        self.is_not_terminal_ph = tf.placeholder(dtype=tf.float32, shape=[None])  # indicators (go into target computation)
        self.is_training_ph = tf.placeholder(dtype=tf.bool, shape=())  # for dropout
        episodes = tf.Variable(0.0, trainable=False, name='episodes')

        with tf.variable_scope('critic'):
            # Critic applied to state_ph and a given action (for training critic)
            self.q_values_of_given_actions = self.generate_critic_network(self.state_ph, self.given_action_ph,
                                                                          trainable=True)

        # slow target critic network
        with tf.variable_scope('slow_target_critic'):
            # Slow target critic applied to slow target actor's outputted actions for next_state_ph (for training critic)
            self.slow_q_values_next = tf.stop_gradient(
                self.generate_critic_network(self.next_state_ph, self.slow_target_action_ph, trainable=False))

        # One step TD targets y_i for (s,a) from experience replay
        # = r_i + gamma*Q_slow(s',mu_slow(s')) if s' is not terminal
        # = r_i if s' terminal
        targets = tf.expand_dims(self.reward_ph, 1) + tf.expand_dims(self.is_not_terminal_ph, 1) * gamma * self.slow_q_values_next

        # 1-step temporal difference errors
        td_errors = targets - self.q_values_of_given_actions

        critic_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='critic')
        critic_loss = tf.reduce_mean(tf.square(td_errors))

        # critic optimizer
        self.critic_train_op = tf.train.AdamOptimizer(lr_critic * lr_decay).minimize(critic_loss, var_list = critic_vars)

        slow_target_critic_vars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='slow_target_critic')
        update_slow_target_ops_c = []
        for i, slow_target_var in enumerate(slow_target_critic_vars):
            update_slow_target_critic_op = slow_target_var.assign(tau * critic_vars[i] + (1 - tau) * slow_target_var)
            update_slow_target_ops_c.append(update_slow_target_critic_op)
        self.update_slow_targets_op_c = tf.group(*update_slow_target_ops_c)

        self.action_grads = tf.gradients(self.q_values_of_given_actions,self.given_action_ph)[0]


    # will use this to initialize both the critic network its slowly-changing target network with same structure
    def generate_critic_network(self, s, a, trainable):
        state_action = tf.concat([s, a], axis=1)
        hidden = tf.layers.dense(state_action, h1_critic, activation=tf.nn.elu,
                                 kernel_regularizer=tf.contrib.layers.l2_regularizer(0.01),
                                 kernel_initializer=tf.contrib.layers.variance_scaling_initializer(),
                                 use_bias=True, trainable=trainable, name='dense_c')

        hidden_2 = tf.layers.dense(hidden, h2_critic, activation=tf.nn.elu,
                                   kernel_regularizer=tf.contrib.layers.l2_regularizer(0.01),
                                   kernel_initializer=tf.contrib.layers.variance_scaling_initializer(),
                                   use_bias=True, trainable=trainable, name='dense_c1')

        hidden_3 = tf.layers.dense(hidden_2, h3_critic, activation=tf.nn.elu,
                                   kernel_regularizer=tf.contrib.layers.l2_regularizer(0.01),
                                   kernel_initializer=tf.contrib.layers.variance_scaling_initializer(),
                                   use_bias=True, trainable=trainable, name='dense_c2')

        q_values = tf.layers.dense(hidden_3, 1, trainable=trainable,
                                   kernel_regularizer=tf.contrib.layers.l2_regularizer(0.01),
                                   kernel_initializer=tf.contrib.layers.variance_scaling_initializer(),
                                   name='dense_c3',use_bias=False)
        return q_values

    def q_for_given_action(self, state_ph, given_action_ph):

        return self.sess.run(self.q_values_of_given_actions, feed_dict={self.state_ph: state_ph/10,
                                                                        self.given_action_ph: given_action_ph,
                                                                        self.is_training_ph: False})


    def training_critic(self, state_ph, given_action_ph, slow_target_action_ph,
                        reward_ph, next_state_ph, is_not_terminal_ph):

        return self.sess.run(self.critic_train_op,
                             feed_dict={self.state_ph: state_ph/10,
                                        self.given_action_ph: given_action_ph,
                                        self.slow_target_action_ph: slow_target_action_ph,
                                        self.reward_ph: reward_ph,
                                        self.next_state_ph: next_state_ph/10,
                                        self.is_not_terminal_ph: is_not_terminal_ph,
                                        self.is_training_ph: True})

    def grads_for_action(self, state_ph, given_action_ph):
        return self.sess.run(self.action_grads,
                             feed_dict={self.state_ph: state_ph/10,
                                        self.given_action_ph: given_action_ph,
                                        self.is_training_ph: True})

    def training_target_critic(self):
        return self.sess.run(self.update_slow_targets_op_c,
                             feed_dict={self.is_training_ph: False})