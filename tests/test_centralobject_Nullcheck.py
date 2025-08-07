# Tests for the CentralObject class to ensure invalid zero values raise ValueError
import pytest
from diskpics.diskpics.diskpics import CentralObject
from astropy import units as u

# Boilerplate for using a spy/mock object (e.g., unittest.mock or pytest-mock):
# from unittest.mock import MagicMock
# Example:
# mock_obj = MagicMock()
# CentralObject = mock_obj
# Use mock_obj.assert_called_with(...) to verify calls


def test_centralobject_mass_zero():
    """
    Test that CentralObject raises ValueError if mass is zero.
    """
    with pytest.raises(ValueError) as excinfo:
        CentralObject('bh', 0 * u.Msun, mdot=1 * u.Msun/u.yr, radius=1 * u.Rsun, temp=1 * u.K)
    assert "greater than 0" in str(excinfo.value).lower()

def test_centralobject_mdot_zero():
    """
    Test that CentralObject raises ValueError if mdot is zero.
    """
    with pytest.raises(ValueError) as excinfo:
        CentralObject('bh', 1 * u.Msun, mdot=0 * u.Msun/u.yr, radius=1 * u.Rsun, temp=1 * u.K)
    assert "greater than 0" in str(excinfo.value).lower() or "positive number" in str(excinfo.value).lower()

def test_centralobject_radius_zero():
    """
    Test that CentralObject raises ValueError if radius is zero.
    """
    with pytest.raises(ValueError) as excinfo:
        CentralObject('ttauri', 1 * u.Msun, mdot=1 * u.Msun/u.yr, radius=0 * u.Rsun, temp=4000 * u.K)
    assert "greater than 0" in str(excinfo.value).lower()

def test_centralobject_temp_zero():
    """
    Test that CentralObject raises ValueError if temp is zero.
    """
    with pytest.raises(ValueError) as excinfo:
        CentralObject('herbig', 1 * u.Msun, mdot=1 * u.Msun/u.yr, radius=2 * u.Rsun, temp=0 * u.K)
    assert "greater than 0" in str(excinfo.value).lower()

