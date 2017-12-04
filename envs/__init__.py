import logging


logger_env = logging.getLogger('Simsim')
logger_env.setLevel(logging.INFO)
fh_env = logging.FileHandler('./simsim.log')
sh = logging.StreamHandler()
fm = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > [%(name)s] %(message)s')
fh_env.setFormatter(fm)
sh.setFormatter(fm)
logger_env.addHandler(fh_env)
logger_env.addHandler(sh)