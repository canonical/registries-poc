from setuptools import setup

setup(
    name="aspects-follower",
    python_requires=">=3.10",
    install_requires=[
        "snap-http==1.4.0",
    ],
    packages=["src"],
    entry_points={
        "console_scripts": ["follower-cli=src.main:main"],
    },
)
