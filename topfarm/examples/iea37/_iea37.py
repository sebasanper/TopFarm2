"""Objects useful for IEA 37 optimizations
"""
from numpy import array as npa

from py_wake.examples.data.iea37 import iea37_path
from py_wake.examples.data.iea37._iea37 import IEA37Site, IEA37_WindTurbines
from py_wake.examples.data.iea37.iea37_reader import read_iea37_windturbine
from py_wake.wake_models.gaussian import IEA37SimpleBastankhahGaussian

from topfarm.constraint_components.spacing import SpacingConstraint
from topfarm.constraint_components.boundary import CircleBoundaryConstraint
from topfarm.cost_models.py_wake_wrapper import PyWakeAEP


def get_iea37_initial(n_wt=9):
    """Initial positions for IEA Task 37 wind farms

    Parameters
    ----------
    n_wt : int, optional
        Number of wind turbines in farm (must be valid IEA 37 farm)
    """
    site = IEA37Site(n_wt)
    return site.initial_position


def get_iea37_constraints(n_wt=9):
    """Constraints for IEA Task 37 wind farms

    Parameters
    ----------
    n_wt : int, optional
        Number of wind turbines in farm (must be valid IEA 37 farm)

    Returns
    -------
    constr : list of topfarm constraints
        Spacing constraint and boundary constraint for IEA 37 model
    """
    diam = read_iea37_windturbine(iea37_path + 'iea37-335mw.yaml')[2]
    spac_constr = SpacingConstraint(2 * diam)
    bound_rad = npa([900, 1300, 2000, 3000])[n_wt == npa([9, 16, 36, 64])][0]
    bound_constr = CircleBoundaryConstraint((0, 0), bound_rad)
    return [spac_constr, bound_constr]


def get_iea37_cost(n_wt=9):
    """Cost component that wraps the IEA 37 AEP calculator"""
    wd = npa(range(16)) * 22.5  # only 16 bins
    site = IEA37Site(n_wt)
    wind_turbines = IEA37_WindTurbines()
    wake_model = IEA37SimpleBastankhahGaussian(wind_turbines)
    aep_calc = PyWakeAEP(site, wind_turbines, wake_model)
    return aep_calc.get_TopFarm_cost_component(n_wt, wd=wd)
