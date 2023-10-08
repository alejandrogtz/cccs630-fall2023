"""
Python model 'Module 8 - Investment returns.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np
from scipy import stats

from pysd.py_backend.statefuls import Integ
from pysd import Component

__pysd_version__ = "3.11.0"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 0,
    "final_time": lambda: 30,
    "time_step": lambda: 1,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="FINAL TIME", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="Year",
    limits=(0.0, np.nan),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    """
    The frequency with which output is stored.
    """
    return __data["time"].saveper()


@component.add(
    name="TIME STEP",
    units="Year",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################


@component.add(name="Random Seed", comp_type="Constant", comp_subtype="Normal")
def random_seed():
    return 10000


@component.add(
    name="Interest rate",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"random_seed": 1, "time": 1},
)
def interest_rate():
    return stats.truncnorm.rvs(-0.9, 0.9, loc=0.0778, scale=0.191, size=())


@component.add(
    name="Interests",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"interest_rate": 1, "savings": 1},
)
def interests():
    return interest_rate() * savings()


@component.add(
    name="Savings",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_savings": 1},
    other_deps={"_integ_savings": {"initial": {}, "step": {"interests": 1}}},
)
def savings():
    return _integ_savings()


_integ_savings = Integ(lambda: interests(), lambda: 10000, "_integ_savings")
