import tensorflow as tf
from envs.config_env import config_env
from agents.config_agent import config_agent

flags = tf.flags

config_env(flags)
config_agent(flags)

# flags for setting
flags.DEFINE_integer("n_drone", 3, "Number of drones")


