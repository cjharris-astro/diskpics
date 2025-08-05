import numpy as np
import matplotlib.pyplot as plt
import yso_utils as yso
import bh_utils as bh


class CentralObject(object):
    """
    Central object to the accretion disk
    """
    def __init__(self,type,mass,mdot=1.,radius = 1., temp = 1., magnetosphere = False, ):

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

        if not isinstance(float(mass), float):
            raise ValueError("object mass must be a number ")
        else:
            self.mass = float(mass)

        if not isinstance(float(mdot), float):
            raise ValueError("object accretion rate must be a number ")
        elif float(mdot) ==1. :
            print('Using typical values for mdot. if object is a yso then mdot = 1e-8,\
                    if object is a black hole then mdot is 10^(-8.5)')
            if self.type == 'bh':
                self.mdot = 10**(-8.5)
            else:
                self.mdot = 1e-8
        else:
             self.mdot = float(mdot)

        "Required only if type is T Tauri or Herbig"

        if not isinstance(float(radius), float):
            raise ValueError("object accretion rate must be a number ")
        elif float(radius) == 1:
            print('Usind Default values for radius. if BH this is the Schwartzchild Radius. \
                  If object is a YSO, radius is 1Rsun')
            if self.type == 'bh':
                self.radius = bh.get_SchwartzchildRadius(self.mass)
            else:
                self.radius = float(radius)
        else:
            self.radius = float(radius)


        if not isinstance(float(temp), float):
            raise ValueError("object accretion rate must be a number ")
        else:
            if self.type != 'bh' and float(temp) == 1.:
                print('Using default Teff for YSO of 4000 K')
                self.temp = 4000.
            elif self.type != 'bh':
                self.temp = float(temp)


        """ Optional """    
        if isinstance(magnetosphere, bool):
             print("The variable must be of boolean type True or False.")
        else:
            self.magnetosphere = magnetosphere()

        """ All inputs are validated. Now calculate the secundary variables needed for the type of object"""
        if self.type != 'bh':
                self.Lacc = yso.get_Lacc(self.mass,self.radius,self.mdot)
                self.Lstar = yso.get_Lstar(self.radius,self.temp)



class Disk(object):

    def __init__(self,central_object):
        
        if isinstance(central_object, CentralObject):
            raise TypeError("central_object but be a CentralObjecy type")
        else:  
            self.central_obj = central_object


    def get_inner_radii(self):
        if self.central_obj.type == 'bh':
            self.Rin =  bh.get_InnermostCircularStableOrbit(self.central_obj.mass) 
        else:
            self.Rin = yso.get_Rsub(self.central_obj.Lstar,self.central_obj.Lacc)


    def get_disk_temperature(self,R):
        if self.central_obj.type == 'bh':
            self.tdisk = bh.get_DiskTemp(R, self.central_obj.mass, self.central_obj.mdot)
        else:
            self.tdisk = yso.temp(self)


    def get_disk_shape(self,R):
        if self.central_obj.type == 'bh':
            self.scale_height =  bh.get_ScaleHeight(R, self.central_obj.mass, mdot = self.central_obj.mdot)
        else:
            self.scale_height = yso.get_flared_disk(self,R) #ADD NECESARY PARAM
        
    

def plot_disk(thing,rout=1.):

    if isinstance(thing, CentralObject):
        raise TypeError("central_object but be a CentralObjecy type")
    else:  
        disco = Disk(thing)

    disco.get_inner_radii()

    if not isinstance(float(rout), float):
            raise ValueError("object Rdisk must be a number ")
    elif rout == 1:
        print("Using default velue for the outer radius of the disk. Rout = 100 Rin,\
                          Rin is calculated accordingly for each object type.")
        rout = 10*disco.Rin
    else:
        rout = float(rout)

    print(f'Potting your {thing.type}')

    R = np.linspace(disco.Rin,rout)

    disco.get_disk_shape(R)
    disco.get_disk_temperature(R)

    plt.plot(R,disco.scale_height)

    plt.show()