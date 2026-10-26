# Hermes Google Home Skill

Control Google Home devices—lights, switches, scenes, and Hue lights—through Hermes Agent via the Google Smart Home API.

## Status
**Scaffold ready.** This repo contains the initial skill structure:
- `SKILL.md` — skill manifest for Hermes
- `references/setup.md` — one-time Google Cloud / Actions console setup
- `scripts/devices.py` — device registry
- `scripts/auth.py` — OAuth2/JWT helpers
- `scripts/fulfillment.py` — Smart Home intent handler (`SYNC`, `QUERY`, `EXECUTE`)

## What’s inside
- Minimal Flask fulfillment server for Google Smart Home intents
- Device registry with example lights and switches
- Hue-ready device definitions
- Setup guide for Google Cloud, Actions console, and HTTPS endpoint

## Next steps
1. Follow `references/setup.md` to create a Google Cloud project and Smart Home action
2. Deploy `scripts/fulfillment.py` to a public HTTPS endpoint
3. Add your actual devices to `scripts/devices.py`
4. Link the action in the Google Home app
5. Test with "Hey Google, turn on [device]"

## Notes
- This is a **starting scaffold**, not a finished production skill
- Hue integration requires OpenHue CLI or direct Hue bridge API
- Account linking and device discovery must be configured in the Google Actions console

## Author
Built for Hermes Agent by bt / Joker AI
