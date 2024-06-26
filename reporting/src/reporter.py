import logging
from pprint import pformat
from textwrap import indent
from time import sleep

from src.registries import get_registry_value

logging.root.setLevel(logging.DEBUG)

# sample rate per minute,
# default = 1, updated based on control-telemetry.sample-rate
sample_rate = 1


def collect() -> None:
    global sample_rate

    settings = get_registry_value("control-telemetry")
    sample_rate = settings["sample-rate"]

    report = {}
    device_info = get_registry_value("observe-device")
    report["device-id"] = device_info["uuid"]

    interface_stats = get_registry_value(
        "observe-interfaces",
        fields=["packets-received", "packets-sent"],
    )
    if settings["monitor-packets-received"]:
        report["packets-received"] = interface_stats["packets-received"]
    if settings["monitor-packets-sent"]:
        report["packets-sent"] = interface_stats["packets-sent"]

    if settings["monitor-peers"]:
        report["tunnel-peers"] = get_registry_value("observe-tunnel")["peers"]

    logging.info("The network stats are:")
    pretty = pformat(report)
    logging.info(indent(pretty, prefix="\t"))


def main() -> None:
    while True:
        collect()

        beat = 60 / sample_rate
        logging.info(f"Next run in {beat:.2f} seconds")
        sleep(beat)
