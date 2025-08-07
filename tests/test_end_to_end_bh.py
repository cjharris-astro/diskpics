import pytest as pt
import astropy.units as u
import numpy as np
import diskpics.diskpics.bh_utils as bh
import diskpics.diskpics.diskpics as dp

def test_bh():
    """
    Test that will check if a realistic black hole is created
    """

    mbh_expected = (10 * u.Msun).to(u.g)
    mdot_expected = 10**(-8.5)
    rin_expected = 2954126.5550554055 * u.cm
    
    R_expected = np.linspace(rin_expected.value, 5*rin_expected.value)

    temp_expected = 4222090.95037793

    BH = dp.CentralObject('bh', mass=mbh_expected)
    mbh = BH.mass
    mdot = BH.mdot
    med_temp = np.median(bh.get_DiskTemp(R_expected, mbh_expected.value, mdot_expected))

    assert mbh.value == pt.approx(mbh_expected.value, abs=0.2*mbh_expected.value)
    assert mdot.value == pt.approx(mdot_expected, abs=0.2*mdot_expected)
    assert med_temp == pt.approx(temp_expected, abs=0.2*temp_expected)