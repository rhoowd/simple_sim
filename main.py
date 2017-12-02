#!/usr/bin/env python
# coding=utf8
import logging
import envs.make_env as make_env
import agent


if __name__ == '__main__':

    # === Logging setup === #
    logger = logging.getLogger('Simsim')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('./simsim.log')
    sh = logging.StreamHandler()
    fm = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > [%(name)s] %(message)s')
    fh.setFormatter(fm)
    sh.setFormatter(fm)
    logger.addHandler(fh)
    logger.addHandler(sh)

    # now = time.localtime()
    # s_time = "%02d%02d-%02d%02d%02d" % (now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    # result = logging.getLogger('Result')
    # result.setLevel(logging.INFO)
    # result_fh = logging.FileHandler("./result/r-" + s_time + ".txt")
    # result_fm = logging.Formatter('[%(filename)s:%(lineno)s] %(asctime)s\t%(message)s')
    # result_fh.setFormatter(result_fm)
    # result.addHandler(result_fh)

    # === Program start === #
    logger.info("Simsim Start")

    # == Load env == #
    env = make_env.make_env("simple", 1)

    # == Load agent == #
    agent = agent.load("keyboard_agent.py").Agent(env)

    # == Run == #
    agent.learn()




