#!/usr/bin/env python3
"""Minimal Google Smart Home fulfillment server."""
from __future__ import annotations

import os
import json
import requests
from typing import Any, Dict

from flask import Flask, request, jsonify

from auth import verify_token
from devices import get_device, list_devices

HUE_BRIDGE = os.getenv("HUE_BRIDGE", "192.168.0.15")
HUE_USERNAME = os.getenv("HUE_USERNAME", "")
HUE_V1_MAP = {
    "1d2be6d4-cfa3-4bad-ae34-7b9fefb261c2": "5",
    "e183b237-6801-473f-95bd-954b45e0906f": "6",
    "a5bc5274-92c8-45cb-96c9-2cb05308d7c7": "4",
    "fba5f3ea-343c-466b-ac85-93638bdc67f9": "7",
    "4443dc09-4130-4d49-a95f-8404a4b11a18": "8",
    "3f940eee-fd06-46b2-8c0b-0634284a26e9": "9",
}
app = Flask(__name__)


def ok(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"requestId": request.headers.get("X-Request-Id", ""), "payload": payload}


def err(code: str, msg: str) -> Dict[str, Any]:
    return {"requestId": request.headers.get("X-Request-Id", ""), "errorCode": code, "errorMessage": msg}


def hue_set_light(light_id: str, on: bool = None, brightness: int = None, xy: list = None):
    if not HUE_USERNAME:
        return False, "HUE_USERNAME not configured"
    v1_id = HUE_V1_MAP.get(light_id, light_id)
    url = f"http://{HUE_BRIDGE}/api/{HUE_USERNAME}/lights/{v1_id}/state"
    body = {}
    if on is not None:
        body["on"] = on
    if brightness is not None:
        body["bri"] = max(1, min(254, int(brightness * 254 / 100)))
    if xy:
        body["xy"] = xy
    try:
        r = requests.put(url, json=body, timeout=3)
        data = r.json()
        if isinstance(data, list) and data and "success" in data[0]:
            return True, data[0]["success"]
        return False, str(data)
    except Exception as e:
        return False, str(e)


def xy_from_spectrum_rgb(spectrum_rgb: int):
    # Placeholder: spectrumRgb is deprecated in modern Google Smart Home.
    # For now we keep current color unchanged unless caller sends xy explicitly.
    return None


@app.route("/fulfillment", methods=["POST"])
def fulfillment():
    auth = request.headers.get("Authorization")
    user = verify_token(auth)
    if not user:
        return jsonify(err("auth_required", "Invalid or missing token")), 401

    body = request.get_json(force=True)
    intent = body.get("inputs", [{}])[0].get("intent")
    print(f"[fulfillment] intent={intent} user={user}")

    if intent == "action.devices.SYNC":
        return jsonify(ok({
            "devices": [
                {
                    "id": d["id"],
                    "type": d["type"],
                    "traits": d["traits"],
                    "name": {"name": d["name"], "nicknames": [d["name"]]},
                    "willReportState": True,
                    "attributes": d.get("attributes", {}),
                    "roomHint": d.get("room"),
                }
                for d in list_devices()
            ]
        }))

    if intent == "action.devices.QUERY":
        devices = body.get("inputs", [{}])[0].get("payload", {}).get("devices", {})
        result = {}
        for device_id in devices:
            d = get_device(device_id)
            states = dict(d.state) if d else {"on": False}
            result[device_id] = {"online": True, "status": "SUCCESS", "states": states}
        return jsonify(ok({"devices": result}))

    if intent == "action.devices.EXECUTE":
        commands = body.get("inputs", [{}])[0].get("payload", {}).get("commands", [])
        results = []
        for cmd in commands:
            for d in cmd.get("devices", []):
                device_id = d.get("id")
                dev = get_device(device_id)
                if not dev:
                    results.append({"ids": [device_id], "status": "ERROR", "errorCode": "deviceNotFound"})
                    continue

                on = None
                brightness = None
                xy = None
                for exec_cmd in cmd.get("execution", []):
                    command = exec_cmd.get("command")
                    params = exec_cmd.get("params", {})
                    if command == "action.devices.commands.OnOff":
                        on = params.get("on", dev.state.get("on", False))
                    elif command == "action.devices.commands.BrightnessAbsolute":
                        brightness = params.get("brightness", dev.state.get("brightness"))
                    elif command == "action.devices.commands.ColorAbsolute":
                        color = params.get("color", {})
                        if "spectrumRgb" in color:
                            dev.state["color"] = {"spectrumRgb": color["spectrumRgb"]}
                        if "xy" in color:
                            xy = color["xy"]

                ok_hue = True
                hue_msg = ""
                if device_id == "hue-all-lights":
                    all_ids = [
                        x.id for x in list_devices()
                        if x.id != "hue-all-lights" and x.type == "action.devices.types.LIGHT"
                    ]
                    for lid in all_ids:
                        ok2, msg2 = hue_set_light(lid, on=on, brightness=brightness, xy=xy)
                        ok_hue = ok_hue and ok2
                        hue_msg += f"{lid}:{msg2};"
                else:
                    ok_hue, hue_msg = hue_set_light(device_id, on=on, brightness=brightness, xy=xy)

                if on is not None:
                    dev.state["on"] = on
                if brightness is not None:
                    dev.state["brightness"] = brightness

                status = "SUCCESS" if ok_hue else "ERROR"
                print(f"[exec] {device_id} on={on} bri={brightness} xy={xy} -> {status} {hue_msg}")
                results.append({"ids": [device_id], "status": status, "states": dev.state})
        return jsonify(ok({"commands": results}))

    return jsonify(err("invalid_intent", f"Unsupported intent: {intent}")), 400


@app.route("/auth", methods=["GET", "POST"])
def auth():
    return jsonify({"message": "OAuth2 endpoint - configure in Google Cloud / Actions console"})


@app.route("/token", methods=["POST"])
def token():
    return jsonify({"access_token": "test-token", "token_type": "bearer", "expires_in": 3600})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
