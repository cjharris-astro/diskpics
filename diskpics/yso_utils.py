import numpy as np
# import diskpics.constants as con
from astropy import constants as con
from astropy import units as u

sig_sb = con.sigma_sb.to(u.erg/(u.cm**2*u.Kelvin**4*u.s))

def get_Lstar(radius,temp):
      return 4*np.pi*(radius.cgs)**2 * sig_sb * (temp)**4

def get_Lacc(mass,radius,mdot):
    return con.G * mass.cgs * (mdot.cgs/(radius.cgs))

def get_Rsub(Lstar,Lacc, Tsub = 1500*u.K):
        return np.sqrt( (Lstar+Lacc)*u.Lsun.cgs / (4*np.pi *Tsub) )

def magnetosphere():
    return print("Moduled under construction")

def flared_temp_distribution(Lstar,Rstar,Mstar,Rarray):
    Rarray = Rarray
    Ls = Lstar.cgs
    Rs = Rstar.cgs
    sigma_sb = con.sigma_sb.cgs
    K_b = con.k_B.cgs
    mu = 2.3
    mh = con.u.cgs
    G = con.G.cgs
    print(Ls)
    Ms = Mstar.cgs

    one = (Ls/(4*np.pi*Rs**2*sigma_sb))**2
    two = K_b/(mu*mh)
    three = Rarray/(G*Ms)

    Td = (one*two*three)**(1/7)

    return Td

def flared_disk_ScaleHeight(Mstar,Rarray,Tdisk):

    mu = 2.3
    mh = con.u.cgs
    G = con.G.cgs
    Ms = Mstar.cgs
    K_b = con.k_B.cgs

    cs = np.sqrt((K_b*Tdisk)/(mu*mh))

    v_k = np.sqrt(G*Ms/Rarray)

    H = cs/v_k*Rarray

    return H.cgs
     