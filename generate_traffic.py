import subprocess as sp
import numpy as np

def normal_distribution(mean, std, size):
    return np.random.normal(loc = mean, scale = std, size = size)

def generate_traffic():
    # Load
    mean = 20
    std = 0.1
    size = 1

    load = normal_distribution(mean, std, size)
    print("{load}".format(load=load))

    # Flow Duration

    # Racks Size

    # Server




if __name__ == "__main__":
    generate_traffic()