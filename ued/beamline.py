import logging

from hutch_python.utils import safe_load

logger = logging.getLogger(__name__)


with safe_load('Settings'):
    from bluesky.callbacks import LiveTable
    # Disable scientific notation, looks bad for example signal
    LiveTable._FMT_MAP['number'] = 'f'


with safe_load('LCLS-II DAQ'):
    # Set up the lcls2 daq stuff
    from psdaq.control.control import DaqControl
    from psdaq.control.DaqScan import DaqScan

    _control = DaqControl(
        host='drp-ued-cmp002',
        platform=0,
        timeout=10000,
        )

    _instr = _control.getInstrument()
    if _instr is None:
        err = 'Failed to connect to LCLS-II DAQ'
        logger.error(err)
        raise RuntimeError(err)

    _state = _control.getState()
    if _state == 'error':
        err = 'Daq is in error state'
        logger.error(err)
        raise RuntimeError(err)

    # Construct the args that DaqScan is looking for
    from types import SimpleNamespace
    args = SimpleNamespace(
        v=True,             # Verbosity
        B='DAQ:UED',        # PV Base
        detname='scan',     # Detector name
        scantype='scan',    # scan type
        g=None,             # Bit mask of readout groups
        c=120,              # Events per step
        p=0,                # Platform
        x=0,                # Master XPM
        )

    daq = DaqScan(_control, daqState=_state, args=args)

    # Hack over nabs for now to give us the lcls2 daq instead of lcls1
    def _get_daq():
        return daq

    import nabs.preprocessors
    nabs.preprocessors._get_daq = _get_daq

    # Disable the scan pvs, they are not set up for UED
    from ued.db import scan_pvs
    scan_pvs.disable()


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
