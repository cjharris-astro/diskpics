import numpy as np
import constants as c

def get_ScaleHeight(rads, mbh, mdot, alpha=0.1):
    """
    DOCUMENTATION HERE
    """

    Rs = 2 * c.G * mbh / c.c**2

    mcrit = 1.5e18 * (Rs/3e5)

    p1 = 3 * Rs * mdot
    p2 = 4 * 0.1 * mcrit
    p3 = 1-np.sqrt(Rs/rads)

    return (p1/p2) * p3