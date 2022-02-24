# Custom plans for use in ued scan gui
from ophyd import EpicsMotor, EpicsSignal

from bluesky.plans import scan
from bluesky.plan_stubs import configure


def get_daq():
    """
    Find the daq object
    """
    from ued.db import daq
    return daq


def pv_scan(pvname, start, stop, num, events=None, record=None):
    """
    Scan over a PV
    """
    sig = EpicsSignal(pvname, name=pvname)
    if events is None:
        detectors = []
    else:
        daq = get_daq()
        cfg = {'events': events}
        if record is not None:
            cfg['record'] = record
        yield from configure(daq, **cfg)
        detectors = [daq]
    sig.wait_for_connection()
    return (yield from scan(detectors, sig, start, stop, num))


def motor_pv_scan(pvname, start, stop, num, events=None, record=None):
    """
    Scan over a motor record
    """
    mot = EpicsMotor(pvname, name=pvname)
    if events is None:
        detectors = []
    else:
        daq = get_daq()
        cfg = {'events': events}
        if record is not None:
            cfg['record'] = record
        yield from configure(daq, **cfg)
        detectors = detectors + [daq]
    mot.wait_for_connection()
    return (yield from scan(detectors, mot, start, stop, num))
