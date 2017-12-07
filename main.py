#!/usr/bin/env python
# coding=utf8
import logging
import envs.make_env as make_env
import agents
import config

FLAGS = config.flags.FLAGS


if __name__ == '__main__':

    # === Logging setup === #
    logger_env = logging.getLogger('Simsim')
    logger_agent = logging.getLogger('Agent')

    # === Program start === #
    # Load environment
    env = make_env.make_env(FLAGS.scenario, FLAGS.n_drone)
    logger_env.info('Simsim Start with %d drone(s)', FLAGS.n_drone)

    # Load agent
    logger_agent.info("Agent")
    agent = agents.load(FLAGS.agent+"/agent.py").Agent(env)

    print FLAGS.agent, config.file_name

    # Start run
    agent.learn(FLAGS.train)

    env.stop()

    print "exit"
