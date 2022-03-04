import ophyd

import ued.db

from pcdsdevices.epics_motor import EpicsMotorInterface as Motor


_motor_cache = {}
_pv_cache = {}


def get_motor_by_pvname(pvname: str) -> Motor:
    """
    Get a motor given its PV name.

    If it exists in this environment, the existing instance will be reused.
    If not, a new instance will be created.
    """
    pvname = pvname.strip()
    for motor in ued.db.motors:
        if motor.prefix == pvname:
            return motor

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
        _pv_cache[pvname] = Motor(pvname, name=pvname)
    return _pv_cache[pvname]
