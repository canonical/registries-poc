from setuptools import setup

setup(
    name="aspects-server",
    python_requires=">=3.10",
    install_requires=[
        "fastapi==0.110.0",
        "pydantic==2.6.4",
        "starlette==0.36.3",
        "uvicorn==0.29.0",
    ],
    packages=["src"],
    entry_points={
        "console_scripts": ["server-cli=src.main:main"],
    },
)
