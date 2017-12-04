import imp
import os.path as osp
import time
import logging


def load(name):
    pathname = osp.join(osp.dirname(__file__), name)
    return imp.load_source('', pathname)


now = time.localtime()
s_time = "%02d%02d-%02d%02d%02d" % (now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
result = logging.getLogger('Result')
result.setLevel(logging.INFO)
result_fh = logging.FileHandler("./result/r-" + s_time + ".txt")
result_fm = logging.Formatter('[%(filename)s:%(lineno)s] %(asctime)s\t%(message)s')
result_fh.setFormatter(result_fm)
result.addHandler(result_fh)

logger_agent = logging.getLogger('Agent')
logger_agent.setLevel(logging.INFO)
fh_agent = logging.FileHandler('./agent.log')
sh = logging.StreamHandler()
fm = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > [%(name)s] %(message)s')
fh_agent.setFormatter(fm)
sh.setFormatter(fm)
logger_agent.addHandler(fh_agent)
logger_agent.addHandler(sh)