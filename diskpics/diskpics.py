import numpy as np
import matplotlib.pyplot as plt
import diskpics.diskpics.yso_utils as yso
import diskpics.diskpics.bh_utils as bh
from astropy import units as u
from astropy.units import Quantity
import matplotlib as mpl
import os

class CentralObject(object):
    """
    Central object to the accretion disk
    """
    "Enable unit check"

   

    def __init__(self,type,mass,mdot=1.*u.Msun/u.yr,radius = 1.*u.Rsun, temp = 1.*u.K, magnetosphere = False, ):

        """Obligatory variables """

        if not isinstance(type, str):
            raise TypeError("Object type must be one of this str: 'BH', 'TTauri', 'Herbig' ")
        
        type = type.lower()
        type = type.replace('-','')
        type = type.replace(' ','')


        if type not in ['bh','ttauri','herbig']:
            raise ValueError("object type must be one of this str: 'BH', 'TTauri', 'Herbig' ")
        else:
            self.type = type

        if not (isinstance(mass, Quantity) and mass.unit.is_equivalent(u.g)):
            raise ValueError(r"Object mass must be a Quantity (uses astropy units) of the physical type mass")
        elif mass.value <=0:
            raise ValueError("Object Mass must be greater than 0")
        else:
            self.mass = mass.cgs

        if not (isinstance(mdot, Quantity) and mdot.unit.is_equivalent(u.g/u.s)):
            raise ValueError(r"Accretion rate must be a Quantity (uses astropy units) of the physical type mass/time")
        elif mdot.value <=0:
            raise ValueError("Accretion rate must be a positive number greater than 0. You may have entered Log(accrition rate)")
        elif mdot.value ==1. :
            print('Using typical values for mdot. if object is a yso then mdot = 1e-8 Msun/yr, if object is a black hole then mdot is 10^(-8.5)Msun/yr')
            if self.type == 'bh':
                self.mdot = mdot * 10**(-8.5) 
            else:
                self.mdot = mdot * 1e-8 
        else:
             self.mdot = mdot.to(u.Msun/u.yr)

        "Required only if type is T Tauri or Herbig"

        if not (isinstance(radius, Quantity) and radius.unit.is_equivalent(u.m)):
            raise ValueError(r"object radius must be a Quantity (uses astropy units) of the physical type length")
        elif radius.value <=0:
            raise ValueError("Object radius must be greater than 0")
        elif radius.value == 1:
            print('Usind default values for radius. If BH this is the Schwartzchild Radius. If object is a YSO, default value is 1 Rsun')
            if self.type == 'bh':
                self.radius = bh.get_SchwartzchildRadius(self.mass.cgs.value) *u.cm
            else:
                self.radius = radius.cgs
        else:
            self.radius = radius.cgs


        if not (isinstance(temp, Quantity) and temp.unit.is_equivalent(u.K) ):
            raise ValueError(r"object effective temperature must be a Quantity (uses astropy units) of the physical type temperature")
        elif temp.value <=0:
            raise ValueError("Object effective temperature must be greater than 0")
        else:
            if self.type != 'bh' and temp.value == 1.:
                print('Using default Teff for YSO of 4000 K')
                self.temp = 4000.*u.K
            elif self.type != 'bh':
                self.temp = temp.to(u.K)


        """ Optional """    
        if isinstance(magnetosphere, bool):
             print("The variable must be of boolean type True or False.")
        else:
            self.magnetosphere = magnetosphere()

        """ All inputs are validated. Now calculate the secundary variables needed for the type of object"""
        if self.type != 'bh':
                self.Lacc = yso.get_Lacc(self.mass,self.radius,self.mdot.cgs)
                self.Lstar = yso.get_Lstar(self.radius,self.temp)



class Disk(CentralObject):


    def get_inner_radii(self):
        """ges Innermost Circular Stable Orbit for BH or Sublimation radius for YSO
        """
        if self.type == 'bh':
            self.Rin =  bh.get_InnermostCircularStableOrbit(self.mass.cgs.value) *u.cm
        else:
            self.Rin = yso.get_Rsub(self.Lstar.cgs,self.Lacc.cgs)


    def get_disk_temperature(self,R):
        """Defines the disk temperature for a BH or YSO

        Args:
            R (array): array of radii
        """
        if self.type == 'bh':
            self.tdisk = bh.get_DiskTemp(R.value, self.mass.cgs.value, self.mdot.value) *u.K
        else:
            self.tdisk = yso.flared_temp_distribution(self.Lstar.cgs,self.mass.cgs,R.cgs)


    def get_disk_shape(self,R):
        """Scale height for BH and flared disk for YSO

        Args:
            R (array): Array of Radii
        """
        if self.type == 'bh':
            self.scale_height =  bh.get_ScaleHeight(R.value, self.mass.cgs.value, mdot = self.mdot.value) *u.cm
        else:
            self.scale_height = yso.flared_disk_ScaleHeight(self.mass.cgs,R.cgs,self.tdisk.cgs)
        
    

def plot_disk(disco,rout=1.*u.Rsun, cmap='Spectral_r'):
    """Plot Disks

    Args:
        disco (float): Inner disk radius
        rout (float, optional): Outer disk radius. Defaults to 1.*u.Rsun.
        cmap (str, optional): Color map. Defaults to 'Spectral_r'.

    Raises:
        ValueError: object Rdisk must be a Quantity
    """

    plt.figure(figsize=(10,2.5))

    disco.get_inner_radii()

    if not isinstance(rout, Quantity):
            raise ValueError("object Rdisk must be a Quantity (uses astropy units) ")
    elif rout.value == 1:
        print("Using default value for the outer radius of the disk. Rout = 5 Rin")
        rout = 5*disco.Rin
    else:
        rout = rout

    print(f'Plotting your {disco.type}')

    R = np.linspace(disco.Rin.cgs,rout.cgs)

    disco.get_disk_temperature(R.cgs)
    disco.get_disk_shape(R.cgs)
   

    yaxis = disco.scale_height/disco.radius
    xaxis = R/disco.radius
    plt.plot(xaxis, yaxis, c= 'k')

    disco.get_disk_temperature(R)

    cmap =  mpl.cm.get_cmap(cmap)
    cmap_ysos = mpl.cm.get_cmap('Oranges_r')

    circle_r = 1
    if disco.type == 'bh':
        normalize =  mpl.colors.LogNorm(vmin=min(disco.tdisk.value), vmax=max(disco.tdisk.value))
        circle = plt.Circle((0, 0), circle_r, color='k')
    else:
        normalize =  mpl.colors.LogNorm(vmin=min(disco.tdisk.value), vmax=max(disco.tdisk.value))
        norm_stars =  mpl.colors.LogNorm(vmin=300, vmax=40000)
        circle = plt.Circle((0, 0), circle_r, color=cmap_ysos(norm_stars(disco.temp.value))) #cmap(normalize(disco.temp.value))

    plt.gca().add_patch(circle)
    
    for i in range(len(R) - 1):
        color_val = disco.tdisk[i].value
        color = cmap(normalize(color_val))
        plt.fill_between(xaxis[i:i+2], yaxis[i:i+2], color=color)
 

    plt.xlabel(r'$\rm R/R_{obj}$',fontsize=16)
    plt.ylabel(r'$\rm H/R_{obj}$',fontsize=16)

    plt.ylim(0,max(yaxis))
    plt.xlim(0,max(xaxis))

    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    plt.gca().set_facecolor('none')

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['bottom'].set_linewidth(2) 
    plt.gca().spines['left'].set_linewidth(2) 

    plt.show()