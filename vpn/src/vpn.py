from random import choice, randint, random

from src.aspects import get_aspect, set_aspect


def changes() -> None:
    config = get_aspect("setup-tunnel")
    peers = set(config["peers"])

    remove_node = random() <= 0.1
    add_node = random() <= 0.1

    if remove_node and len(peers) > 0:
        peer = choice(config["peers"])
        peers.remove(peer)
        print(f"Peer node {peer} dropped.")

    if add_node:
        ip_class = choice([1, 2, 3])
        if ip_class == 1:
            peer = f"10.{randint(0,255)}.{randint(0,255)}.{randint(0,255)}"
        elif ip_class == 2:
            peer = f"172.{randint(16,31)}.{randint(0,255)}.{randint(0,255)}"
        else:
            peer = f"192.168.{randint(0,255)}.{randint(0,255)}"
        peers.add(peer)
        print(f"Peer node {peer} joined.")

    if remove_node or add_node:
        set_aspect("setup-tunnel", {"peers": list(peers)})
    else:
        print("No changes to tunnel.")
