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


with safe_load('Standalone PVs'):
    from ophyd import EpicsSignal
    sample_pv = EpicsSignal('ASTA:AO:BK05:V0001', name='sample_pv')
