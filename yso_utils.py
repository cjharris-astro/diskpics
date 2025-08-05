import numpy as np
import constants as con

def get_Lstar(radius,temp):
      return 4*np.pi*(radius*con.Rsun)**2 * con.sig_sb * (temp)**4

def get_Lacc(mass,radius,mdot):
    return con.G * mass * con.Msun * (mdot*(con.Msun/con.yr)/(radius*con.Rsun))

def get_Rsub(Lstar,Lacc, Tsub = 1500):
        return np.sqrt( (Lstar+Lacc)*con.Lsun / (4*np.pi *Tsub) )

def get_flared_disk(param):
      return param