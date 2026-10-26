# Hermes Google Home Skill

Control Google Home devices—lights, switches, scenes, and Hue lights—through Hermes Agent via the Google Smart Home API.

## Status
**Ready for deployment.** This repo contains the skill structure plus real Hue device registry and fulfillment logic.

## What’s inside
- `SKILL.md` — skill manifest for Hermes
- `references/setup.md` — one-time Google Cloud / Actions console setup
- `scripts/devices.py` — device registry with real Hue lights
- `scripts/auth.py` — OAuth2/JWT helpers
- `scripts/fulfillment.py` — Flask Smart Home intent handler with Hue bridge control

## Supported devices
- **Master Bedroom** — 2 Hue color lights
- **Living Room** — 3 Hue color lights
- **Office** — 1 Hue light
- **All Hue Lights** — grouped control

## Features
- Google Smart Home intents: `SYNC`, `QUERY`, `EXECUTE`
- Hue bridge control via direct API
- Brightness, on/off, and color control
- Room-aware device hints for Google Home

## Next steps
1. Follow `references/setup.md` to create a Google Cloud project and Smart Home action
2. Deploy `scripts/fulfillment.py` to a public HTTPS endpoint
3. Add your actual devices to `scripts/devices.py`
4. Link the action in the Google Home app
5. Test with "Hey Google, turn on [device]"

## Notes
- Hue bridge username is required; use the link-button registration flow in `references/setup.md`
- Account linking and device discovery must be configured in the Google Actions console

## Author
Built for Hermes Agent by bt / Joker AI
