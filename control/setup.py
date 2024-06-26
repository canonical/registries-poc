from setuptools import setup

setup(
    name="control",
    python_requires=">=3.10",
    install_requires=[
        "snap-http==1.4.0",
        "requests==2.31.0",
        "cryptography==42.0.5",
    ],
    packages=["src"],
    entry_points={
        "console_scripts": ["control-cli=src.interfaces:beat"],
    },
)
