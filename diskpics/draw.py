import matplotlib.pyplot as plt
import numpy as np
from astropy import units as u
from astropy import constants as const



sigma_sb = const.sigma_sb.cgs.value
def inner_radius(Lsun,T_sub):
    sigma_sb = const.sigma_sb.cgs
    Ls = const.L_sun.cgs *Lsun
    T_sub = T_sub*u.K
    Rin  = 1/(4*np.pi)*(Ls/(sigma_sb*T_sub**4))**0.5
    #Rin = Rin.to(u.AU)
    return Rin

inner_radius(1,1500)

def flared_temp_distribution(Lsun,Rsun,Msun,Rarray):
    Rarray = Rarray*const.au.cgs
    Ls = const.L_sun.cgs *Lsun
    Rs = const.R_sun.cgs*Rsun
    sigma_sb = const.sigma_sb.cgs
    K_b = const.k_B.cgs
    mu = 2.3
    mh = const.u.cgs
    G = const.G.cgs
    
    Ms = const.M_sun.cgs*Msun

    one = (Ls/(4*np.pi*Rs**2*sigma_sb))**2
    two = K_b/(mu*mh)
    three = Rarray/(G*Ms)
    Td = (one*two*three)**(1/7)
    cs = np.sqrt((K_b*Td)/(mu*mh))
    v_k = np.sqrt(G*Ms/Rarray)
    H = cs/v_k*Rarray
    H_r = H*(-1)
    return H, H_r


Rarray = np.linspace(inner_radius(1,1500),10*inner_radius(1,1500))
flared_temp_distribution(1,1,1,Rarray)



Td = Ls**(2/7)* R**(-3/7)
H = Td**(1/2) * R**(3/2)
H_r = H*(-1)
#Draw a flared disk
G = const.G.cgs.value
sigma_sb = const.sigma_sb.cgs.value
Lsun = const.L_sun.cgs.value
M  = 5*u.Msun.cgs
T_sub = 1500 * u.K.cgs
Rin = 1/(4*np.pi)*(Lsun/(sigma_sb*T_sub**4))**0.5
Rout = 10*Rin

#Tin = (3*G*M*Mdot)/(8*np.pi*R*sigma_sb)
R = np.linspace(Rin,Rout)
Td = Lsun**(2/7)* R**(-3/7)
H = Td**(1/2) * R**(3/2)
H_r = H*(-1)
circle = plt.Circle((0, 0), 1, color='r')
plt.plot(R,H)
plt.plot(R,H_r)

plt.gca().add_patch(circle)
plt.gca().set_aspect('equal')

plt.show()


