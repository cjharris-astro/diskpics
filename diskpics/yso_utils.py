import numpy as np
# import diskpics.constants as con
from astropy import constants as con
from astropy import units as u

sig_sb = con.sigma_sb.to(u.erg/(u.cm**2*u.Kelvin**4*u.s))

def get_Lstar(radius,temp):
      return 4*np.pi*(radius*con.Rsun.cgs)**2 * sig_sb * (temp)**4

def get_Lacc(mass,radius,mdot):
    return con.G * mass*con.Msun.cgs * (mdot*(con.Msun.cgs/con.yr.cgs)/(radius*con.Rsun.cgs))

def get_Rsub(Lstar,Lacc, Tsub = 1500*u.K):
        return np.sqrt( (Lstar+Lacc)*con.Lsun.cgs / (4*np.pi *Tsub) )

def get_flared_disk(param):
      return param

def magnetosphere():
    return print("Moduled under construction")