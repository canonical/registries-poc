import random
import socket
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


def generate_keys() -> tuple[str, str]:
    """Generate RSA key pair."""
    key = rsa.generate_private_key(
        backend=default_backend(),
        public_exponent=65537,
        key_size=2048,
    )
    private_key = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    ).decode("utf-8")
    public_key = (
        key.public_key()
        .public_bytes(
            serialization.Encoding.OpenSSH,
            serialization.PublicFormat.OpenSSH,
        )
        .decode("utf-8")
    )

    return private_key, public_key


def get_architecture() -> str:
    """Generate a random architecture."""
    return random.choice(
        [
            "amd64",
            "arm64",
            "armhf",
            "ppc64el",
            "s390x",
            "i386",
        ]
    )


def get_ip_address() -> str:
    """Get the device's IP address."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))
    ip = sock.getsockname()[0]
    sock.close()
    return ip
