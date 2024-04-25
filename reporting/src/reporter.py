import logging
from pprint import pformat
from textwrap import indent
from time import sleep

from src.aspects import get_aspect

logging.root.setLevel(logging.DEBUG)

# sample rate per minute,
# default = 1, updated based on setup-metrics.sample-rate
sample_rate = 1


def collect() -> None:
    global sample_rate

    settings = get_aspect("setup-metrics")
    sample_rate = settings["sample-rate"]

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

    logging.info("The network stats are:")
    pretty = pformat(report)
    logging.info(indent(pretty, prefix="\t"))


def main() -> None:
    while True:
        collect()

        beat = 60 / sample_rate
        logging.info(f"Next run in {beat:.2f} seconds")
        sleep(beat)
