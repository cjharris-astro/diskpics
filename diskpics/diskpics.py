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
            self.mass = mass

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
             self.mdot = mdot

        "Required only if type is T Tauri or Herbig"

        if not (isinstance(radius, Quantity) and radius.unit.is_equivalent(u.m)):
            raise ValueError(r"object radius must be a Quantity (uses astropy units) of the physical type length")
        elif radius.value <=0:
            raise ValueError("Object radius must be greater than 0")
        elif radius.value == 1:
            print('Usind Default values for radius. if BH this is the Schwartzchild Radius. If object is a YSO, default value is 1 Rsun')
            if self.type == 'bh':
                self.radius = bh.get_SchwartzchildRadius(self.mass.cgs.value) *u.cm
            else:
                self.radius = radius
        else:
            self.radius = radius


        if not (isinstance(temp, Quantity) and temp.unit.is_equivalent(u.K) ):
            raise ValueError(r"object effective temperature must be a Quantity (uses astropy units) of the physical type temperature")
        elif temp.value <=0:
            raise ValueError("Object effective temperature must be greater than 0")
        else:
            if self.type != 'bh' and temp.value == 1.:
                print('Using default Teff for YSO of 4000 K')
                self.temp = 4000.*u.K
            elif self.type != 'bh':
                self.temp = temp


        """ Optional """    
        if isinstance(magnetosphere, bool):
             print("The variable must be of boolean type True or False.")
        else:
            self.magnetosphere = magnetosphere()

        """ All inputs are validated. Now calculate the secundary variables needed for the type of object"""
        if self.type != 'bh':
                self.Lacc = yso.get_Lacc(self.mass.to(u.Msun),self.radius.to(u.Rsun),self.mdot.to(u.Msun/u.yr))
                self.Lstar = yso.get_Lstar(self.radius.to(u.Rsun),self.temp.to(u.K))



class Disk(CentralObject):

    # def __init__(self,central_object):
        
    # if isinstance(type(CentralObject), CentralObject):
        # raise TypeError("central_object but be a CentralObject type")

    def get_inner_radii(self):
        if self.type == 'bh':
            self.Rin =  bh.get_InnermostCircularStableOrbit(self.mass.cgs.value) *u.cm
        else:
            self.Rin = yso.get_Rsub(self.Lstar.to(u.Lsun),self.Lacc.to(u.Lsun))


    def get_disk_temperature(self,R):
        if self.type == 'bh':
            self.tdisk = bh.get_DiskTemp(R, self.mass.cgs.value, self.mdot.value) *u.K
        else:
            self.tdisk = yso.temp(self)


    def get_disk_shape(self,R):
        if self.type == 'bh':
            self.scale_height =  bh.get_ScaleHeight(R, self.mass.cgs.value, mdot = self.mdot.value) *u.cm
        else:
            self.scale_height = yso.get_flared_disk(self,R) #ADD NECESARY PARAM
        
    

def plot_disk(disco,rout=1.*u.Rsun):

    # plt.style.use(f'{os.getcwd()}/diskpic.mplstyle')
    # with plt.xkcd():

    plt.figure(figsize=(10,2.5))

    disco.get_inner_radii()

    if not isinstance(rout, Quantity):
            raise ValueError("object Rdisk must be a Quantity (uses astropy units) ")
    elif rout.value == 1:
        print("Using default velue for the outer radius of the disk. Rout = 5 Rin")
        rout = 5*disco.Rin
    else:
        rout = rout

    print(f'Potting your {disco.type}')

    R = np.linspace(disco.Rin.cgs,rout.cgs)

    disco.get_disk_shape(R.value)
    disco.get_disk_temperature(R.value)

    yaxis = disco.scale_height/disco.radius
    xaxis = R/disco.radius
    plt.plot(xaxis, yaxis, c= 'k')

    disco.get_disk_temperature(R.value)

    cmap =  mpl.cm.get_cmap('Spectral_r')


    # circle_r = np.sqrt((1)**2 + (disco.radius.value)**2)
    # circle_r = np.sqrt((1)**2 + (disco.radius.to(u.km).value)**2)
    circle_r = 1
    if disco.type == 'bh':
        normalize =  mpl.colors.Normalize(vmin=min(disco.tdisk.value), vmax=max(disco.tdisk.value))
        circle = plt.Circle((0, 0), circle_r, color='k')
    else:
        normalize =  mpl.colors.Normalize(vmin=min(disco.tdisk.value), vmax=max(disco.temp.value))
        circle = plt.Circle((0, 0), circle_r, color=disco.temp)

    plt.gca().add_patch(circle)
    
    for i in range(len(R) - 1):
        color_val = disco.tdisk[i].value
        color = cmap(normalize(color_val))
        plt.fill_between(xaxis[i:i+2], yaxis[i:i+2], color=color)
        # plt.fill_between(R,yaxis,color=cmap(normalize(disco.tdisk)),zorder=0)


    # plt.xlim(0,max(R/disco.radius))
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