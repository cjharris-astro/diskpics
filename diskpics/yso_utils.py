import numpy as np
# import diskpics.constants as con
from astropy import constants as con
from astropy import units as u

sig_sb = con.sigma_sb.to(u.erg/(u.cm**2*u.Kelvin**4*u.s))

def get_Lstar(radius,temp):
      return 4*np.pi*(radius.cgs)**2 * sig_sb * (temp)**4

def get_Lacc(mass,radius,mdot):
    return con.G.cgs * mass.cgs * (mdot.cgs/(radius.cgs))

def get_Rsub(Lstar,Lacc, Tsub = 1400*u.K):
        # return np.sqrt( (Lstar.cgs+Lacc.cgs)/ (4*np.pi *Tsub) )
        return 1/(4*np.pi) * np.sqrt( (Lstar.cgs+Lacc.cgs)/ (sig_sb*Tsub**4) )

def magnetosphere():
    return print("Module under construction")

def flared_temp_distribution(Lstar,Mstar,Rarray,mu = 2.3):
    """
    Units don't work out in this equation!!!
    """

    one = (Lstar.cgs/(4*np.pi*(Rarray.cgs)**2*sig_sb))**2
    two = con.k_B.cgs/(mu*con.u.cgs)
    three = Rarray.cgs/(con.G.cgs*Mstar.cgs)
    Td = (one*two*three)**(1/7)
    return Td.value * u.K
    # return Lstar.cgs**(2/7)*(Rarray.cgs)**(-3/7)

def flared_disk_ScaleHeight(Mstar,Rarray,Tdisk, mu = 2.3):

    cs = np.sqrt((con.k_B.cgs*Tdisk.cgs)/(mu*con.u.cgs))

    v_k = np.sqrt(con.G.cgs*Mstar.cgs/Rarray.cgs)

    return (cs/v_k)*Rarray.cgs
     