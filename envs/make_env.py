#!/usr/bin/env python
# coding=utf8

"""
====================================
 :mod:`make_env` Make environment
====================================
.. moduleauthor:: Daewoo Kim
.. note:: note...

설명
=====

Code for creating a environment with one of the scenarios listed
in ./scenarios/.
Can be called by using, for example:
    env = make_env('simple_speaker_listener')
After producing the env object, can be used similarly to an OpenAI gym
environment.
A policy using this environment must output actions in the form of a list
for all agents. Each element of the list should be a numpy array,
of size (env.world.dim_p + env.world.dim_c, 1). Physical actions precede
communication actions in this array. See environment.py for more details.
"""


def make_env(scenario_name):
    """

    :param scenario_name: name of the scenario from ./scenarios/ to be Returns
                          (without the .py extension)
    :return:
    """
    from envs.environment import Env
    import envs.scenarios as scenarios

    # load scenario from script
    scenario = scenarios.load(scenario_name + ".py").Scenario()

    # create world
    world = scenario.make_world()

    # create Simsim environment
    # env = Env(world, scenario.reset_world, scenario.reward, scenario.observation, scenario.target_move)
    env = Env()
    return env


