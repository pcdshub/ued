# Custom plans for use in ued scan gui
from ophyd import EpicsMotor, EpicsSignal

from bluesky.plans import scan
from bluesky.plan_stubs import configure

from ued.util import get_signal_by_pvname, get_motor_by_pvname


def get_daq():
    """
    Find the daq object
    """
    from ued.db import daq
    return daq


def get_begin_timeout(events: int):  #  -> float:
    """Get the DAQ begin timeout for a number of events."""
    return None
    # return max((60.0, events / 120.0 + 1.0))


def pv_scan(
    pvname: str,
    start: float,
    stop: float,
    num: int,
    events: int = None,
    record: bool = None,
):
    """
    Scan over a PV
    """
    sig = get_signal_by_pvname(pvname)
    if events:
        daq = get_daq()
        cfg = {
            "events": events,
            "controls": [sig],
            "begin_timeout": get_begin_timeout(events),
        }
        if record is not None:
            cfg['record'] = record
        yield from configure(daq, **cfg)
        detectors = [daq]
    else:
        detectors = []
    sig.wait_for_connection()
    yield from scan(detectors, sig, start, stop, num)
    if events:
        yield from configure(daq, record=False)


def motor_pv_scan(
    pvname: str,
    start: float,
    stop: float,
    num: int,
    events: int = None,
    record: bool = None,
):
    """
    Scan over a motor record
    """
    mot = get_motor_by_pvname(pvname)
    if events:
        daq = get_daq()
        cfg = {
            "events": events,
            "controls": [mot],
            "begin_timeout": get_begin_timeout(events),
        }
        if record is not None:
            cfg['record'] = record
        yield from configure(daq, **cfg)
        detectors = [daq]
    else:
        detectors = []
    mot.wait_for_connection()
    yield from scan(detectors, mot, start, stop, num)
    if events:
        yield from configure(daq, record=False)
