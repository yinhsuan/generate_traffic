import numpy as np
from scipy.stats import truncnorm

def normal_distribution(mean, std):
    return np.random.normal(loc=mean, scale=std, size=None)

def truncated_normal_distribution(a, b, mean, std):
    return truncnorm.rvs(a, b, loc=mean, scale=std, size=1)

def log_normal_distribution(mean, std):
    return np.random.lognormal(mean=mean, sigma=std, size=None)

def exponential_distribution(scale):
    return np.random.exponential(scale=scale, size=None)

def weibull_distribution(shape):
    return np.random.weibull(a=shape, size=None)

def pareto_distribution(shape):
    return np.random.pareto(a=shape, size=None)

def poisson_distribution(lam):
    return np.random.poisson(lam=lam, size=None)

def uniform_distribution(low, high):
    return np.random.uniform(low=low, high=high, size=None)

# mean = 20
# std = 0.1
# a = 1
# b = 15
# scale = 2
# shape = 1
# lam = 1
# low = 10
# high = 50

# load = int(normal_distribution(mean, std))
# load = int(truncated_normal_distribution(a, b, mean, std))
# load = int(exponential_distribution(scale))
# load = int(log_normal_distribution(mean, std))
# load = int(weibull_distribution(shape))
# load = int(pareto_distribution(shape))
# load = int(poisson_distribution(lam))
# load = int(uniform_distribution(low, high))
# print("{load}".format(load=load))