import numpy as np
import matplotlib.pyplot as plt
import yso_utils as yso

# This probably would need to be used inside class for disk
class CentralObject(object):
    """
    Central object to the accretion disk
    """
    def __init__(self,type,mass,mdot,radius = 1., temp = 4000., magnetosphere = False, ):


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

        # NO LONGER NECESARY ADDED "TYPICAL" values as default
        # if self.type in ['ttauri','herbig'] and (self.radius ==. or self.temp == 4000):
        #     raise ValueError("Your object type is a T Tauri or Herbig disk, \
        #                      you need to input a real value for R* and Teff, \
        #                       default values are 0")


        """ Optional """    
        if isinstance(magnetosphere, bool):
             print("The variable must be of boolean type True or False.")
        else:
            self.magnetosphere = magnetosphere

        """ All inputs are validated. Now calculate the secundary variables needed for the type of object"""
        if self.type in ['ttauri','herbig']:
                self.Lacc = yso.get_Lacc(self.mass,self.radius,self.mdot)
                self.Lstar = yso.get_Lstar(self.radius,self.temp)
                self.Rsub = yso.get_Rsub(self.Lstar,self.Lacc)

        def magnetosphere():
            "will return magnetospheric radius"
            return print("Moduled under construction")

class Disk(object):

    def __init__(self,central_object,Rdisk =0., flared = False):
        
        if isinstance(central_object, CentralObject):
            raise TypeError("central_object but be a CentralObjecy type")
        else:  
            self.central_obj = central_object

        if not isinstance(float(Rdisk), float):
            raise ValueError("object accretion rate must be a number ")
        else:
            self.Rdisk = Rdisk

        "Optional variables"
        
        if isinstance(flared, bool):
             print("The variable must be of boolean type True or False.")
        else:
            self.flared = flared

        def flared():
            return print("Moduled under construction")

def temperature_gradient():
    return print("NOT DONE YET")

def plot_disk():
    return print("NOT DONE YET")

print("Incomming bug!")

arr = [0,1,2,3]

item = arr[6]