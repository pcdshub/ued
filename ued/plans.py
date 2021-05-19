# Custom plans for use in ued scan gui
from ophyd import EpicsMotor, EpicsSignal

from bluesky.plans import scan


class PhonyMotor:
    """
    Hack to help with current incomplete daq config handling
    """
    def __init__(self, signal):
        self.sig = signal
        self.name = signal.name

    @property
    def position(self):
        return self.sig.get()


def get_daq():
    """
    Find the daq object
    """
    from ued.ued_daq import daq
    return daq


def config_daq_options(daq, motors, events):
    """
    Set the DAQ's active motors and events per step
    """
    if events is not None:
        daq.readoutCount = events
    daq.configure(motors=motors)


def config_in_scan(detectors, motors, events):
    try:
        daq = get_daq()
    except Exception:
        return
    if daq in detectors:
        config_daq_options(daq, motors, events)


def pv_scan(detectors, pvname, start, stop, num, events=None):
    """
    Scan over a PV as a UI test utility
    """
    sig = EpicsSignal(pvname, name=pvname)
    mot = PhonyMotor(sig)
    config_in_scan(detectors, [mot], events)

    sig.wait_for_connection()
    return (yield from scan(detectors, sig, start, stop, num))


def motor_pv_scan(detectors, pvname, start, stop, num, events=None):
    """
    Scan over a motor record as a UI test utility
    """
    mot = EpicsMotor(pvname, name=pvname)
    config_in_scan(detectors, [mot], events)

    mot.wait_for_connection()
    return (yield from scan(detectors, mot, start, stop, num))
