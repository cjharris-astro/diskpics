"""Until I can get over my apprehension toward astropy.units, I'll use my own unit module"""

# Define Constants

# Physical Constants:

c = 2.99792458e10  # cm s^-1
c_kms = 2.99792458e5 # km s^-1
G = 6.6743e-8  # cm^3 g^-1 s^-2
G_obs = 4.3009e-3 # pc/Msun (km/s)^2
h = 6.626070040e-27  # cm^2 g s^-1
h_ev = 4.1357e-15  # eV s
hbar = 1.0546e-27  # cm^2 g s^-1
hbar_ev = 6.5821e-16  # eV s
kb = 1.38064852e-16  # cm^2 g s^-2 K^-1 // erg K^-1
kb_ev = 8.6173e-5  # eV K^-1
sig_sb = 5.670367e-5  # g s^-3 K^-4
a_r = 7.565e-15 # erg cm^-3 K^-4
sig_t = 6.6524e-25 # cm^2
e = 4.8032e-10  # cm^3/2 g^1/2 s^-1
me = 9.1094e-28  # g
me_mev = 0.511  # MeV/c^2
mp = 1.672621898e-24  # g
mp_mev = 938.272  # MeV/c^2
mn = 1.6726e-24  # g
mn_mev = 939.563  # MeV/c^2
mu = 1.66053906660e-24  # g
mu_mev = 931.494  # MeV/c^2
mH = 1.6735e-24 # g
mHe = 6.6464e-24 # g

# Astronomical Constants:

Msun = 1.989e33  # g
Mearth = 5.974e27 # g
Mjup = 1.899e30 # g
Rsun = 6.955e10 # cm
Rearth = 6.378e8 # cm
Rjup = 7.149e9 # cm
Lsun = 3.839e33 # erg s^-1
Xsun = 0.71
Ysun = 0.27
Zsun = 0.019

# Cosmological Constants
Om_bh2 = 0.02242 # baryons
Om_ch2 = 0.11933 # cold dark matter
ns = 0.9665
H0 = 67.66 # km/s/Mpc
Om_L = 0.6889 # dark energy
Om_m = 0.3111 # matter
Om_mh2 = 0.14240
Om_ph2 = 2.4e-5 # photons
Om_rh2 = 4.2e-5 # radiation
sig8 = 0.8102
z_reion = 7.82
age = 13.787e9 # yr
z_rec = 1089.8
z_eq = 3387
k_eq = 0.010339
nb_np = 2.74e-8 * Om_bh2 # baryon-photon ratio

# Unit Conversions

AU = 1.496e13 # cm
pc = 3.086e18 # cm
ly = 9.461e17 # cm
yr = 3.156e7 # s
ev = 1.602e-12 # g
