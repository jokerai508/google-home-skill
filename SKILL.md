# Google Home

Control Google Home devices—lights, switches, scenes, and Hue lights—through Hermes Agent via the Google Smart Home API.

## When to use
- User asks to turn lights on/off, dim, change color, or run scenes
- User wants to control Google Home devices from Hermes
- User asks about device status in Google Home

## Setup
See `references/setup.md` for the one-time Google Cloud / Actions console setup.

## Commands
- `lights on [room/device]`
- `lights off [room/device]`
- `lights dim [0-100] [room/device]`
- `lights color <color> [room/device]`
- `switch on/off [device]`
- `scene activate <scene>`
- `status [room/device]`

## Integration
- Fulfillment server: `scripts/fulfillment.py`
- Device registry: `scripts/devices.py`
- Auth helpers: `scripts/auth.py`
- Works with Philips Hue via OpenHue CLI or direct bridge API.
