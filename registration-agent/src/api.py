from typing import Optional

import requests
import snap_http

from src.aspects import get_aspect, set_aspect, unset_aspect
from src.device import generate_keys, get_architecture, get_ip_address


class HttpException(Exception):
    pass


def _map_snap_config(snap_config: dict):
    """Map snap config to a format that can be stored in aspects."""
    # replace _ in the snap names with - to
    # keep aspects path validation happy
    return {k.replace("_", "-"): v for k, v in snap_config.items()}


def _make_request(
    method: str,
    url: str,
    data: Optional[dict] = None,
) -> requests.Response:
    """Make a HTTP request."""
    response = requests.request(method, url, json=data)
    if response.status_code >= 400:
        raise HttpException(response.status_code, response.text)

    return response


def register(base_url: str) -> None:
    """Register a device with the server."""
    private_key, public_key = generate_keys()
    ip_address = get_ip_address()
    arch = get_architecture()

    response = _make_request(
        "post",
        base_url + "/register/",
        {
            "ip-address": ip_address,
            "arch": arch,
            "public-key-rsa": public_key,
        },
    )
    result = response.json()

    set_aspect(
        "device",
        {
            "uid": result["uuid"],
            "ip-address": ip_address,
            "public-rsa-key": public_key,
            "private-rsa-key": private_key,
            "registered": result["registered"],
            "architecture": arch,
        },
    )

    snap_http.set_conf(
        "aspects-registration-agent",
        {"is-registered": True},
    )


def poll(base_url: str) -> None:
    """Push the device's current config & pull changes if any."""
    snap_config = get_aspect("snap-config")
    uid = get_aspect("device", fields=["uid"])["uid"]

    payload = {
        "uuid": uid,
        # undo what _map_snap_config did while storing the aspects
        "config": {k.replace("-", "_"): v for k, v in snap_config.items()},
    }
    response = _make_request(
        "post",
        base_url + "/poll/",
        payload,
    )

    if response.status_code == 200:
        config = response.json()["config"]
        unset_aspect("snap-config")
        set_aspect("snap-config", _map_snap_config(config))
