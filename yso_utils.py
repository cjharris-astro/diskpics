import numpy as np
import constants as con

def get_Lacc(mass,radius,mdot):
    return con.G * mass * con.Msun * (mdot*(con.Msun/con.yr)/(radius*con.Rsun))

def get_Rsub(Lstar,Lacc =False, Tsub = 1500):
        return np.sqrt( (Lstar+Lacc)*con.Lsun / (4*np.pi *Tsub) )