import numpy as np
import matplotlib.pyplot as plt
import diskpics.diskpics.yso_utils as yso
import diskpics.diskpics.bh_utils as bh
from astropy import units as u
from astropy.units import Quantity
import matplotlib as mpl

class CentralObject(object):
    """
    Central object to the accretion disk
    """
    def __init__(self,type,mass,mdot=1.*u.Msun/u.yr,radius = 1.*u.Rsun, temp = 1.*u.K, magnetosphere = False, ):

        """Obligatory variables """

        if not isinstance(type, str):
            raise TypeError("object type must be one of this str: 'BH', 'TTauri', 'Herbig' ")
        
        type = type.lower()
        type = type.replace('-','')
        type = type.replace(' ','')


        if type not in ['bh','ttauri','herbig']:
            raise ValueError("object type must be one of this str: 'BH', 'TTauri', 'Herbig' ")
        else:
            self.type = type

        if not isinstance(mass, Quantity):
            raise ValueError("object mass must be a Quantity (uses astropy units) ")
        else:
            self.mass = mass

        if not isinstance(mdot, Quantity):
            raise ValueError("object accretion rate must be a Quantity (uses astropy units) ")
        elif mdot.value ==1. :
            print('Using typical values for mdot. if object is a yso then mdot = 1e-8 Msun/yr, if object is a black hole then mdot is 10^(-8.5)Msun/yr')
            if self.type == 'bh':
                self.mdot = mdot * 10**(-8.5) 
            else:
                self.mdot = mdot * 1e-8 
        else:
             self.mdot = mdot

        "Required only if type is T Tauri or Herbig"

        if not isinstance(radius, Quantity):
            raise ValueError("object accretion rate must be a Quantity (uses astropy units) ")
        elif radius.value == 1:
            print('Usind Default values for radius. if BH this is the Schwartzchild Radius. If object is a YSO, default value is 1 Rsun')
            if self.type == 'bh':
                self.radius = bh.get_SchwartzchildRadius(self.mass.cgs.value) *u.cm
            else:
                self.radius = radius
        else:
            self.radius = radius


        if not isinstance(temp, Quantity):
            raise ValueError("object accretion rate must be a Quantity (uses astropy units) ")
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
            self.Rin =  bh.get_InnermostCircularStableOrbit(self.mass.cgs.value) 
        else:
            self.Rin = yso.get_Rsub(self.Lstar.to(u.Lsun),self.Lacc.to(u.Lsun))


    def get_disk_temperature(self,R):
        if self.type == 'bh':
            self.tdisk = bh.get_DiskTemp(R, self.mass.cgs.value, self.mdot.value)
        else:
            self.tdisk = yso.temp(self)


    def get_disk_shape(self,R):
        if self.type == 'bh':
            self.scale_height =  bh.get_ScaleHeight(R, self.mass.cgs.value, mdot = self.mdot.value)
        else:
            self.scale_height = yso.get_flared_disk(self,R) #ADD NECESARY PARAM
        
    

def plot_disk(disco,rout=1.*u.Rsun):
    
    with plt.xkcd():

        plt.figure(figsize=(10,2.5))
        # if isinstance(type(thing), CentralObject):
        #     raise TypeError("central_object but be a CentralObjecy type")
        # else:  
        #     disco = Disk(thing)

        disco.get_inner_radii()

        if not isinstance(rout, Quantity):
                raise ValueError("object Rdisk must be a Quantity (uses astropy units) ")
        elif rout.value == 1:
            print("Using default velue for the outer radius of the disk. Rout = 5 Rin")
            rout = 5*disco.Rin
        else:
            rout = rout

        print(f'Potting your {disco.type}')

        R = np.linspace(disco.Rin,rout)

        # plt.style.use('./diskpic.mplstyle')


        disco.get_disk_shape(R)
        disco.get_disk_temperature(R)

        yaxis = disco.scale_height/disco.radius.value
        xaxis = R/disco.radius.value
        plt.plot(xaxis, yaxis, c= 'k')

        disco.get_disk_temperature(R)

        cmap =  mpl.cm.get_cmap('Spectral_r')

    
        # circle_r = np.sqrt((1)**2 + (disco.radius.value)**2)
        # circle_r = np.sqrt((1)**2 + (disco.radius.to(u.km).value)**2)
        circle_r = 1
        if disco.type == 'bh':
            normalize =  mpl.colors.Normalize(vmin=min(disco.tdisk), vmax=max(disco.tdisk))
            circle = plt.Circle((0, 0), circle_r, color='k')
        else:
            normalize =  mpl.colors.Normalize(vmin=min(disco.tdisk), vmax=max(disco.temp))
            circle = plt.Circle((0, 0), circle_r, color=disco.temp)

        plt.gca().add_patch(circle)
        
        for i in range(len(R) - 1):
            color_val = disco.tdisk[i]
            color = cmap(normalize(color_val))
            plt.fill_between(xaxis[i:i+2], yaxis[i:i+2], color=color)
            # plt.fill_between(R,yaxis,color=cmap(normalize(disco.tdisk)),zorder=0)




        # plt.xlim(0,max(R/disco.radius))
        plt.xlabel(r'$\rm R/R_{obj}$')
        plt.ylabel(r'$\rm H/R_{obj}$')

        plt.ylim(0,max(yaxis))
        plt.xlim(0,max(xaxis))

        # plt.semilogy()
        # plt.gca().set_aspect('equal')
        plt.show()