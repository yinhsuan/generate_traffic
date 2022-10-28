import subprocess as sp
import numpy as np
from scipy.stats import truncnorm
import argparse

from distribution import normal_distribution
from distribution import truncated_normal_distribution
from distribution import exponential_distribution
from distribution import log_normal_distribution
from distribution import weibull_distribution
from distribution import pareto_distribution
from distribution import poisson_distribution
from distribution import uniform_distribution

from traffic import *



def generate_traffic(case, mean, std, traffic_file):
    mean = 20
    std = 0.1
    a = 15
    b = 25
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
    # load = int(uniform_distribution(low, high))ß
    # print("{load}".format(load=load))


    # STEP1: Traffic Generate Case
    # Fixed
    if case == "fixed":
        traffics = get_traffics_from_file(traffic_file)
    # Whole System
    elif case == "whole":
        numberOfRack = int(truncated_normal_distribution(a, b, mean, std)) #要用哪種distribution之後再決定
        # print("{numberOfRack}".format(numberOfRack=numberOfRack))
        # print("{traffic_file}".format(traffic_file=traffic_file))

    # Locality System
    else:
        print("local")

    # STEP2: How many racks

    # STEP3: Which racks

    # STEP4: How many servers

    # STEP5: Which servers

    # STEP6: Determine src & dst pair

    # STEP7: Determine flow load & duration

    # STEP8: Start the traffic




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', type=str)
    parser.add_argument('--traffic_file', type=str)
    parser.add_argument('--mean', type=str)
    parser.add_argument('--std', type=str)
    args = parser.parse_args()

    generate_traffic(args.case, args.mean, args.std, args.traffic_file)