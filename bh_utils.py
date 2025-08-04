import numpy as np
import constants as c

# def get_ScaleHeight(rads, mbh, mdot, alpha=0.1):
#     """
#     DOCUMENTATION HERE
#     """

#     Rs = 2 * c.G * mbh / c.c**2

#     mcrit = 1.5e18 * (Rs/3e5)

#     p1 = 3 * Rs * mdot
#     p2 = 4 * 0.1 * mcrit
#     p3 = 1-np.sqrt(Rs/rads)

#     return (p1/p2) * p3

def get_SchwartzchildRadius(mbh):

    Rs = 2 * c.G * mbh / c.c**2

    return Rs

def get_InnermostCircularStableOrbit(mbh, spin=False):

    risco = 3 * get_SchwartzchildRadius(mbh)

    if spin:
        """Not yet implimented :("""
        return risco

    return risco

def get_ScaleHeight(rads, mbh, mdot=10**(-8.5), alpha=0.1):

    zi = 3.2e6 * mdot * mbh * (1-np.power(rads,-1/2))

    zm = 1.2e4 * alpha**(-1/10) * mdot**(1/5) * mbh**(9/10) * rads**(21/20) * (1-np.power(rads,-1/2))**(1/5)

    zo = 6.1e3 * alpha**(-1/10) * mdot**(3/20) * mbh**(9/10) * rads**(9/8) * (1-np.power(rads,-1/2))**(3/20)

    zi_zm_idx = np.argwhere(np.diff(np.sign(zi - zm))).flatten()[-1]
    zm_zo_idx = np.argwhere(np.diff(np.sign(zm - zo))).flatten()[-1]

    ztot = np.concatenate((zi[:zi_zm_idx],
                            zm[zi_zm_idx:zm_zo_idx],
                             zo[:zm_zo_idx] ))
    
    return ztot