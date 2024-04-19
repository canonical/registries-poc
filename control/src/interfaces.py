from random import randint

from src.aspects import get_aspect, set_aspect


def beat() -> None:
    interfaces = get_aspect("write-interfaces", fields=["stats"])["stats"]

    for interface in interfaces.keys():
        # simulate packet flow
        up, down = randint(1, 10), randint(1, 10)
        interfaces[interface]["n-sent"] += up
        interfaces[interface]["n-received"] += down

        print(f"{interface}: {up} packets ↑, {down} packets ↓")

    set_aspect("write-interfaces", {"stats": interfaces})
