import numpy as np
import matplotlib.pyplot as plt
import yso_utils as yso

class CentralObject(object):
    """
    Central object to the accretion disk
    """
    def __init__(self,type,mass,mdot,radius = 0., temp = 0.,
                 Rdisk =0., magnetosphere = False, flared = False):


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
            self.mass = mass

        if not isinstance(float(mdot), float):
            raise ValueError("object accretion rate must be a number ")
        else:
             self.mdot = mdot

        "Required only if type is T Tauri or Herbig"

        if not isinstance(float(radius), float):
            raise ValueError("object accretion rate must be a number ")
        else:
            self.radius = radius

        if not isinstance(float(temp), float):
            raise ValueError("object accretion rate must be a number ")
        else:
         self.temp = temp

        if not isinstance(float(Rdisk), float):
            raise ValueError("object accretion rate must be a number ")
        else:
            self.Rdisk = Rdisk

        if self.type in ['ttauri','herbig'] and (self.radius ==0. or self.temp == 0. or self.Rdisk == 0.):
            raise ValueError("Your object type is a T Tauri or Herbig disk, \
                             you need to input a real value for R*, Teff and outer radius of the disk,\
                              default values are 0")
            
        "Optional variables"

        if isinstance(magnetosphere, bool):
             print("The variable must be of boolean type True or False.")
        else:
            self.magnetosphere = magnetosphere

        if isinstance(flared, bool):
             print("The variable must be of boolean type True or False.")
        else:
            self.flared = flared

        """ All inputs are validated. Now calculate the secundary variables needed for the type of object"""
        if self.type in ['ttauri','herbig']:
                self.Lacc = yso.get_Lacc(self.mass,self.radius,self.mdot)
                self.Lstar = yso.get_Lstar(self.radius,self.temp)
                self.Rsub = yso.get_Rsub(self.Lstar,self.Lacc)


def temperature_gradient():
    return print("NOT DONE YET")

def plot_disk():
    return print("NOT DONE YET")
