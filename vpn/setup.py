from setuptools import setup

setup(
    name="aspects-poc-vpn",
    python_requires=">=3.10",
    install_requires=[
        "snap-http==1.4.0",
    ],
    packages=["src"],
    entry_points={
        "console_scripts": ["vpn-cli=src.vpn:changes"],
    },
)
