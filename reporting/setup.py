from setuptools import setup

setup(
    name="reporting",
    python_requires=">=3.10",
    packages=["src"],
    entry_points={
        "console_scripts": ["reporter-cli=src.reporter:main"],
    },
)
