import logging

from hutch_python.utils import safe_load

logger = logging.getLogger(__name__)


with safe_load('Settings'):
    from bluesky.callbacks import LiveTable
    # Disable scientific notation, looks bad for example signal
    LiveTable._FMT_MAP['number'] = 'f'


with safe_load('LCLS-II get_daq'):
    from ued.ued_daq_rework import get_daq


with safe_load('Motors'):
    from pcdsdevices.epics_motor import EpicsMotorInterface as Motor
    # Motors here
    # my_motor = Motor('MY:PVNAME', name=my_motor)


with safe_load('Unit changes'):
    # TODO
    pass


with safe_load('Standalone PVs'):
    from ophyd import EpicsSignal
    sample_pv = EpicsSignal('ASTA:AO:BK05:V0001', name='sample_pv')
