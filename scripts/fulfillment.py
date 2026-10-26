#!/usr/bin/env python3
"""Minimal Google Smart Home fulfillment server."""
from __future__ import annotations

import os
import json
from typing import Any, Dict

from flask import Flask, request, jsonify

from auth import verify_token
from devices import get_device, list_devices

app = Flask(__name__)


def ok(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"requestId": request.headers.get("X-Request-Id", ""), "payload": payload}


def err(code: str, msg: str) -> Dict[str, Any]:
    return {"requestId": request.headers.get("X-Request-Id", ""), "errorCode": code, "errorMessage": msg}


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
            result[device_id] = {"online": True, "status": "SUCCESS", "states": d.state if d else {"on": False}}
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
                for exec_cmd in cmd.get("execution", []):
                    command = exec_cmd.get("command")
                    params = exec_cmd.get("params", {})
                    if command == "action.devices.commands.OnOff":
                        dev.state["on"] = params.get("on", dev.state["on"])
                    elif command == "action.devices.commands.BrightnessAbsolute":
                        dev.state["brightness"] = params.get("brightness", dev.state.get("brightness"))
                    elif command == "action.devices.commands.ColorAbsolute":
                        color = params.get("color", {})
                        if "rgb" in color:
                            dev.state["color"] = {"rgb": color["rgb"]}
                    print(f"[exec] {device_id} {command} {params}")
                results.append({"ids": [device_id], "status": "SUCCESS", "states": dev.state})
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
