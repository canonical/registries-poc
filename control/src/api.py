from typing import Optional

import requests

from src.registries import set_registry_value
from src.device import generate_keys, get_architecture, get_ip_address


class HttpException(Exception):
    pass


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
    _, public_key = generate_keys()
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

    set_registry_value(
        "control-device",
        {
            "id": result["uuid"],
            "registered": result["registered"],
            "server-url": base_url,
        },
    )
