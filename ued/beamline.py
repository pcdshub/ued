import logging

from hutch_python.utils import safe_load

logger = logging.getLogger(__name__)


with safe_load('Settings'):
    from bluesky.callbacks import LiveTable
    # Disable scientific notation, looks bad for example signal
    LiveTable._FMT_MAP['number'] = 'f'


with safe_load('Disable Scan PVs'):
    from ued.db import scan_pvs
    scan_pvs.disable()


with safe_load('Test PVs'):
    from ophyd import EpicsSignal
    test_pv = EpicsSignal('SIOC:SYS7:ML00:AO023', name='test_pv')


with safe_load('BCTRL PVs'):
    from ophyd import EpicsSignal
    XC04S = EpicsSignal('XCOR:AS01:381:BCTRL', name='XC04S')
    YC04S = EpicsSignal('YCOR:AS01:382:BCTRL', name='YC04S')


with safe_load('Motors'):
    from pcdsdevices.epics_motor import EpicsMotorInterface as Motor
    LaserDelay1 = Motor('MOTR:AS01:MC06:CH5:MOTOR', name='LaserDelay1')
    LaserDelay2 = Motor('MOTR:AS01:MC06:CH6:MOTOR', name='LaserDelay2')
    SS1_X = Motor('MOTR:AS01:MC01:CH3:MOTOR', name='1st_X')
    SS1_Y = Motor('MOTR:AS01:MC01:CH4:MOTOR', name='1st_Y')


with safe_load('Basic plans'):
    from ued.db import bp
    from .plans import pv_scan, motor_pv_scan
    bp.pv_scan = pv_scan
    bp.motor_pv_scan = motor_pv_scan

