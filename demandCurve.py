import numpy as np
from scipy.interpolate import PPoly
from random import randrange

# fitted curve coefficients
coefficients = np.array([
    [-0.0000, 0.0019, -0.0261, 0.5800],
    [-0.0000, 0.0004, 0.0104, 0.5200],
    [0.0000, -0.0010, 0.0019, 0.6500],
    [-0.0000, 0.0007, -0.0032, 0.5700],
    [-0.0000, - 0.0004, 0.0044, 0.7500]
])

# x values
x = [0, 4*4, 7.5*4, 11.5*4, 19*4, 24*4]

# Instantiate the piecewise polynomial in Python
ppoly = PPoly(coefficients.T, x)


def consumption(time, demand_factor=1, deviation=0):
    # time: time of the day in hours
    # demand_factor: factor of demanding size in different areas
    # deviation: true or false; with noise or not
    # return: power consumed in %

    # power consumption from the demand curve [0, 1]
    demand = ppoly(time * 4) * 100

    # noise [-1.5, 1.5%]
    noise = 1 + randrange(-150, 150) / 100 if deviation else 1

    return demand * demand_factor * noise


