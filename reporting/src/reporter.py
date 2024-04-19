from pprint import pformat
from textwrap import indent

from src.aspects import get_aspect


def collect() -> None:
    settings = get_aspect("setup-metrics")

    report = {}
    device_info = get_aspect("read-device")
    report["device-id"] = device_info["uuid"]

    interface_stats = get_aspect(
        "read-interfaces", fields=["packets-received", "packets-sent"]
    )
    if settings["monitor-packets-received"]:
        report["packets-received"] = interface_stats["packets-received"]
    if settings["monitor-packets-sent"]:
        report["packets-sent"] = interface_stats["packets-sent"]

    if settings["monitor-peers"]:
        report["tunnel-peers"] = get_aspect("observe-tunnel")["peers"]

    print("The network stats are:")
    pretty = pformat(report)
    print(indent(pretty, prefix="\t"))
