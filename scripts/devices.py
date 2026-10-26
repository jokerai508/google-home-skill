#!/usr/bin/env python3
"""Device registry for Google Home / Hue integration."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Device:
    id: str
    name: str
    type: str
    room: Optional[str] = None
    traits: List[str] = field(default_factory=list)
    attributes: dict = field(default_factory=dict)
    state: dict = field(default_factory=dict)


# Default device registry. Extend this with your actual devices.
DEVICES: List[Device] = [
    Device(
        id="hue-living-room-1",
        name="Living Room Light",
        type="action.devices.types.LIGHT",
        room="Living Room",
        traits=["action.devices.traits.OnOff", "action.devices.traits.Brightness", "action.devices.traits.ColorSetting"],
        attributes={"colorModel": "rgb", "commandOnlyOnOff": False},
        state={"on": False, "brightness": 80, "color": {"rgb": "#ffaa00"}},
    ),
    Device(
        id="hue-bedroom-1",
        name="Bedroom Light",
        type="action.devices.types.LIGHT",
        room="Bedroom",
        traits=["action.devices.traits.OnOff", "action.devices.traits.Brightness"],
        attributes={"commandOnlyOnOff": False},
        state={"on": False, "brightness": 50},
    ),
    Device(
        id="switch-plug-1",
        name="Desk Plug",
        type="action.devices.types.SWITCH",
        room="Office",
        traits=["action.devices.traits.OnOff"],
        attributes={"commandOnlyOnOff": True},
        state={"on": False},
    ),
]


def get_device(device_id: str) -> Optional[Device]:
    for d in DEVICES:
        if d.id == device_id:
            return d
    return None


def list_devices() -> List[dict]:
    return [d.__dict__ for d in DEVICES]
