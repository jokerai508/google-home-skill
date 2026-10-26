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


DEVICES: List[Device] = [
    Device(
        id="1d2be6d4-cfa3-4bad-ae34-7b9fefb261c2",
        name="Master room Left",
        type="action.devices.types.LIGHT",
        room="Master Bedroom",
        traits=["action.devices.traits.OnOff", "action.devices.traits.Brightness", "action.devices.traits.ColorSetting"],
        attributes={"colorModel": "xy", "commandOnlyOnOff": False},
        state={"on": False, "brightness": 3, "color": {"spectrumRgb": 15404962}},
    ),
    Device(
        id="e183b237-6801-473f-95bd-954b45e0906f",
        name="Master room Right",
        type="action.devices.types.LIGHT",
        room="Master Bedroom",
        traits=["action.devices.traits.OnOff", "action.devices.traits.Brightness", "action.devices.traits.ColorSetting"],
        attributes={"colorModel": "xy", "commandOnlyOnOff": False},
        state={"on": False, "brightness": 3, "color": {"spectrumRgb": 15404962}},
    ),
    Device(
        id="a5bc5274-92c8-45cb-96c9-2cb05308d7c7",
        name="Living room Center",
        type="action.devices.types.LIGHT",
        room="Living Room",
        traits=["action.devices.traits.OnOff", "action.devices.traits.Brightness", "action.devices.traits.ColorSetting"],
        attributes={"colorModel": "xy", "commandOnlyOnOff": False},
        state={"on": True, "brightness": 73, "color": {"spectrumRgb": 15404962}},
    ),
    Device(
        id="fba5f3ea-343c-466b-ac85-93638bdc67f9",
        name="Living room Left",
        type="action.devices.types.LIGHT",
        room="Living Room",
        traits=["action.devices.traits.OnOff", "action.devices.traits.Brightness", "action.devices.traits.ColorSetting"],
        attributes={"colorModel": "xy", "commandOnlyOnOff": False},
        state={"on": True, "brightness": 83, "color": {"spectrumRgb": 15404962}},
    ),
    Device(
        id="4443dc09-4130-4d49-a95f-8404a4b11a18",
        name="Living room Right",
        type="action.devices.types.LIGHT",
        room="Living Room",
        traits=["action.devices.traits.OnOff", "action.devices.traits.Brightness", "action.devices.traits.ColorSetting"],
        attributes={"colorModel": "xy", "commandOnlyOnOff": False},
        state={"on": True, "brightness": 73, "color": {"spectrumRgb": 15404962}},
    ),
    Device(
        id="3f940eee-fd06-46b2-8c0b-0634284a26e9",
        name="Table",
        type="action.devices.types.LIGHT",
        room="Office",
        traits=["action.devices.traits.OnOff", "action.devices.traits.Brightness"],
        attributes={"colorModel": "xy", "commandOnlyOnOff": False},
        state={"on": False, "brightness": 88, "color": {"spectrumRgb": 15404962}},
    ),
    Device(
        id="hue-all-lights",
        name="All Hue Lights",
        type="action.devices.types.LIGHT",
        room="Home",
        traits=["action.devices.traits.OnOff", "action.devices.traits.Brightness", "action.devices.traits.ColorSetting"],
        attributes={"colorModel": "xy", "commandOnlyOnOff": False},
        state={"on": False, "brightness": 70, "color": {"spectrumRgb": 15404962}},
    ),
]


def get_device(device_id: str) -> Optional[Device]:
    for d in DEVICES:
        if d.id == device_id:
            return d
    return None


def list_devices() -> List[dict]:
    return [d.__dict__ for d in DEVICES]
