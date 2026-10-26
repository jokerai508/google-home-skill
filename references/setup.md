# Google Smart Home + Hermes Skill Setup

## Prerequisites
- Google Cloud account with billing enabled
- Hermes Agent installed locally
- Public HTTPS endpoint for fulfillment (ngrok, Cloud Run, Render, Railway, etc.)
- Optional: Philips Hue bridge for Hue light control

## Step 1: Create Google Cloud Project
1. Go to https://console.cloud.google.com/
2. Create a new project
3. Enable the **Smart Home API** in the API Library
4. Go to **APIs & Services → Credentials**
5. Create **OAuth 2.0 Client ID** (type: Web application)
   - Name: `jokerai508-home-fulfillment`
   - Add your fulfillment URL to authorized origins
   - Save the Client ID and Client Secret

## Step 2: Actions Console Setup
1. Go to https://console.actions.google.com/
2. Create a new project
3. Select **Smart Home** as the app type
4. Under **Develop → Account linking**, set:
   - Client ID: from Google Cloud
   - Client Secret: from Google Cloud
   - Authorization URL: `https://your-domain.com/auth`
   - Token URL: `https://your-domain.com/token`
5. Under **Develop → Actions**, set the **Fulfillment URL** to `https://your-domain.com/fulfillment`
6. Under **Test → Simulator**, test SYNC, QUERY, EXECUTE

## Step 3: Deploy Fulfillment Server
```bash
# Install deps
pip install flask pyjwt requests

# Run locally for testing
python scripts/fulfillment.py

# Or deploy to Cloud Run / Render / Railway
# Make sure to set env vars:
#   GOOGLE_CLIENT_ID
#   GOOGLE_CLIENT_SECRET
#   JWT_SECRET
#   HUE_BRIDGE=192.168.0.15
#   HUE_USERNAME=<from bridge registration>
```

### Testing without OAuth
If you don't have Client ID/Secret yet, set `BYPASS_AUTH=true` to skip token validation:
```bash
BYPASS_AUTH=true python scripts/fulfillment.py
```

## Step 4: Hue Bridge Username
The fulfillment server needs a Hue API username to control lights.
1. Press the **link button** on your Hue bridge
2. Run: `python -c "import requests; print(requests.post('http://<bridge-ip>/api', json={'devicetype':'hermes#jokerai'}, timeout=5).text)"`
3. Copy the `username` value from the response
4. Set it as `HUE_USERNAME` in your deployment environment

If using the bundled `devices.py`, your Hue devices are already pre-registered.

## Step 5: Expose Public URL
- Use ngrok for testing: `ngrok http 8080`
- Or deploy to Cloud Run / Render / Railway
- Update Actions console with the public URL

## Step 6: Link in Google Home App
1. Open Google Home app
2. Add device → Works with Google
3. Find your action name
4. Sign in with the same Google account
5. Devices should sync automatically

## Step 6: Test
- Say "Hey Google, turn on [device]"
- Check fulfillment logs for SYNC/QUERY/EXECUTE requests
- Adjust device registry in `scripts/devices.py` as needed

## Hue Integration
- Install OpenHue CLI: https://www.openhue.io/
- Or use direct Hue bridge API
- Add Hue devices to `scripts/devices.py` registry
- Fulfillment server routes commands to Hue bridge

## Security Notes
- Always validate JWT tokens on fulfillment requests
- Use HTTPS only
- Rotate JWT_SECRET periodically
- Never expose Client Secret in client-side code
