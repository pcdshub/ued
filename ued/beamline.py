import logging

from hutch_python.utils import safe_load

logger = logging.getLogger(__name__)


with safe_load('LCLS-II DAQ'):
    # Set up the lcls2 daq stuff
    from pcdsdaq.control.control import DaqControl
    from pcdsdaq.control.DaqScan import DaqScan

    _control = DaqControl(
        host='drp-ued-cmp001',
        platform=7,
        timeout=10000,
        )

    _instr = _control.get_instrument()
    if instrument is None:
        err = 'Failed to connect to LCLS-II DAQ'
        logger.error(err)
        raise RuntimeError(err)

    _state = _control.getState()
    if _state == 'error':
        err = 'Daq is in error state'
        logger.error(err)
        raise RuntimeError(err)

    daq = DaqScan(_control, daqState=_state)

    # Hack over nabs for now to give us the lcls2 daq instead of lcls1
    def _get_daq():
        return daq

    import nabs.preprocessors
    nabs.preprocessors._get_daq = _get_daq


with safe_load('Motors'):
    from pcdsdevices.epics_motor import EpicsMotorInterface as Motor
    # Motors here
    # my_motor = Motor('MY:PVNAME', name=my_motor)


with safe_load('Unit changes'):
    # TODO
    pass
