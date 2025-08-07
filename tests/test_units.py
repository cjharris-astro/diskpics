import numpy as np
import pytest as pt
import astropy.units as u
import diskpics.diskpics.diskpics as dp

# Check radius, mass, mdot, inner radius, temp, zeros/negs,
# order of magnitudes, height, realistic mdot, accretion luminosity,
# 

def test_input_units():
    """
    Test that will check if a input physical parameters have the right units
    """

    mass_expected = "Object mass must be a Quantity (uses astropy units) of the physical type mass"
    mdot_expected = "Accretion rate must be a Quantity (uses astropy units) of the physical type mass/time"
    temp_expected = "object effective temperature must be a Quantity (uses astropy units) of the physical type temperature"
    radius_expected = "object radius must be a Quantity (uses astropy units) of the physical type length"

    with pt.raises(ValueError,match=mass_expected):
        dp.CentralObject('bh', mass=5*u.K)

    with pt.raises(ValueError, match=mdot_expected):
        dp.CentralObject('bh', mass=5*u.g, mdot = 10*u.g)

    with pt.raises(ValueError, match=temp_expected):
        dp.CentralObject('bh', mass=5*u.g,  temp = 3*u.s )

    with pt.raises(ValueError, match=radius_expected):
        dp.CentralObject('bh', mass=5*u.g, radius = 4*u.erg )

