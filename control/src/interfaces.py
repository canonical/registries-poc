from random import randint

from src.registries import get_registry_value, set_registry_value


def beat() -> None:
    interfaces = get_registry_value(
        "control-interfaces",
        fields=["stats"],
    )["stats"]

    for interface in interfaces.keys():
        # simulate packet flow
        up, down = randint(1, 10), randint(1, 10)
        interfaces[interface]["n-sent"] += up
        interfaces[interface]["n-received"] += down

        print(f"{interface}: {up} packets ↑, {down} packets ↓")

    set_registry_value(
        "control-interfaces",
        {"stats": interfaces},
    )
