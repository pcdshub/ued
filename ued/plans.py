# Custom plans for use in ued scan gui
from __future__ import annotations

from ophyd.epics_motor import EpicsMotor
from ophyd.pv_positioner import PVPositioner

from bluesky.plans import scan
from bluesky.plan_stubs import configure
from bluesky.preprocessors import stub_wrapper, run_decorator, stage_decorator


from ued.util import get_signal_motor_by_pvname, get_motor_by_pvname


def get_daq():
    """
    Find the daq object
    """
    from ued.db import daq
    return daq


def pv_scan(
    pvname: str,
    start: float,
    stop: float,
    num: int,
    events: int | None = None,
    group_mask: int | None = None,
    record: bool | None = None,
):
    """
    Scan over a PV
    """
    yield from inner_pv_scan(
        motor=get_signal_motor_by_pvname(pvname),
        start=start,
        stop=stop,
        num=num,
        events=events,
        group_mask=group_mask,
        record=record,
    )


def motor_pv_scan(
    pvname: str,
    start: float,
    stop: float,
    num: int,
    events: int | None = None,
    group_mask: int | None = None,
    record: bool | None = None,
):
    """
    Scan over a motor record
    """
    yield from inner_pv_scan(
        motor=get_motor_by_pvname(pvname),
        start=start,
        stop=stop,
        num=num,
        events=events,
        group_mask=group_mask,
        record=record,
    )


def inner_pv_scan(
    motor: EpicsMotor | PVPositioner,
    start: float,
    stop: float,
    num: int,
    subscans: int = 1,
    and_back: bool = False,
    events: int | None = None,
    group_mask: int | None = None,
    record: bool | None = None,
):
    if events:
        daq = get_daq()
        cfg = {
            "motors": [motor],
            "events": events,
            "group_mask": group_mask,
        }
        if record is not None:
            cfg['record'] = record
        yield from configure(daq, **cfg)
        detectors = [daq]
    else:
        detectors = []
    motor.wait_for_connection()

    @stage_decorator(detectors + [motor])
    @run_decorator(md={})
    def inner(start: int, stop: int):
        for _ in range(subscans):
            yield from stub_wrapper(scan(detectors, motor, start, stop, num))
            if and_back:
                start, stop = stop, start

    yield from inner(start=start, stop=stop)
