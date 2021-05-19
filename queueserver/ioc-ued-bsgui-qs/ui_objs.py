# Sorry, we need to monkey-patch this temporarily.
import bluesky_queueserver.manager.profile_ops
import psdaq.control.DaqScan

def devices_from_nspace(nspace):
    """
    Extract devices from the namespace. 
    Returns the dict of ophyd.Device objects. **and** daq objects.
    
    Parameters
    ----------
    nspace: dict
        Namespace that may contain plans.
    Returns
    -------
    dict(str: callable)
        Dictionary of devices.
    """
    import ophyd

    devices = {}
    for item in nspace.items():
        if isinstance(item[1], (ophyd.Device, psdaq.control.DaqScan.DaqScan)):
            devices[item[0]] = item[1]
    return devices


# This is important for **listing** the daq in the YAML file:
bluesky_queueserver.manager.profile_ops.devices_from_nspace = devices_from_nspace
# This is important for actually **using** the daq:
bluesky_queueserver.manager.worker.devices_from_nspace = devices_from_nspace

from ued.plans import pv_scan, motor_pv_scan
from ued.ued_daq_rework import get_daq

daq = get_daq()
daq.name = "daq"

print("The daq object's name is", daq.name)
