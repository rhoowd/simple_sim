#!/usr/bin/env python
# coding=utf8
import logging
import envs.make_env as make_env
import agent
from envs.config_env import Flags_e



if __name__ == '__main__':

    # === Logging setup === #
    logger_env = logging.getLogger('Simsim')
    logger_agent = logging.getLogger('Agent')

    # === Program start === #
    # Load environment
    env = make_env.make_env(Flags_e.scenario, Flags_e.n_drone)
    logger_env.info('Simsim Start with %d drone(s)', Flags_e.n_drone)

    # Load agent
    logger_agent.info("Agent")
    agent = agent.load("ddpg/ddpg.py").Agent(env)
    # agent = agent.load("naive/naive.py").Agent(env)
    # agent = agent.load("keyboard_agent.py").Agent(env)

    # Start run
    agent.learn()

    env.stop()
    print "exit"