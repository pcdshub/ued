import ophyd
from ophyd.signal import EpicsSignal

import ued.db

from pcdsdevices.epics_motor import EpicsMotorInterface as Motor
from pcdsdevices.pv_positioner import OnePVMotor


_motor_cache = {}
_pv_cache = {}
_pv_motor_cache = {}


def get_motor_by_pvname(pvname: str) -> Motor:
    """
    Get a motor given its PV name.

    If it exists in this environment, the existing instance will be reused.
    If not, a new instance will be created.
    """
    pvname = pvname.strip()
    for motor in ued.db.motors:
        try:
            if motor.prefix == pvname:
                return motor
        except AttributeError:
            ...

    if pvname not in _motor_cache:
        _motor_cache[pvname] = Motor(pvname, name=pvname)
    return _motor_cache[pvname]


def get_signal_by_pvname(pvname: str) -> ophyd.EpicsSignal:
    """
    Get an EpicsSignal given its PV name.

    If it exists in this environment, the existing instance will be reused.
    If not, a new instance will be created.
    """
    pvname = pvname.strip()
    for sig in ued.db.a:
        if getattr(sig, "setpoint_pvname", None) == pvname:
            return sig

    if pvname not in _pv_cache:
        _pv_cache[pvname] = EpicsSignal(pvname, name=pvname)
    return _pv_cache[pvname]


def get_signal_motor_by_pvname(pvname: str) -> OnePVMotor:
    """
    Get a OnePVMotor given its PV name.
    """
    pvname = pvname.strip()

    if pvname not in _pv_motor_cache:
        _pv_motor_cache[pvname] = OnePVMotor(pvname, name=pvname)
    return _pv_motor_cache[pvname]



