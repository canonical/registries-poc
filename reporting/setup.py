from setuptools import setup

setup(
    name="aspects-poc-reporting",
    python_requires=">=3.10",
    packages=["src"],
    entry_points={
        "console_scripts": ["reporter-cli=src.reporter:collect"],
    },
)
