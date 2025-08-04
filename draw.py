import matplotlib.pyplot as plt
import numpy as np
from astropy import units as u
from astropy import constants as const

#Draw a flared disk
G = const.G.value
sigma_sb = const.sigma_sb.value
Ls = 1
T_sub = 1500
Rin = 1/(4*np.pi)*(Ls/(sigma_sb*T_sub**4))**0.5
Rout = 10*Rin

Tin = (3*G*M*Mdot)/(8*np.pi*R*sigma_sb)
R = np.linspace(Rin,Rout)
Td = Ls**(2/7)* R**(-3/7)
H = Td**(1/2) * R**(3/2)
H_r = H*(-1)
circle = plt.Circle((0, 0), 1, color='r')
plt.plot(R,H)
plt.plot(R,H_r)

plt.gca().add_patch(circle)
plt.gca().set_aspect('equal')

plt.show()