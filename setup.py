from codecs import open
from pathlib import Path

import tomli
from setuptools import find_packages, setup

with open("pyproject.toml", "rb") as f:
    pyproject = tomli.load(f)


setup(
    name=pyproject["tool"]["poetry"]["name"],
    version=pyproject["tool"]["poetry"]["version"],
    author="Damego",
    author_email="damego.dev@gmail.com",
    description=pyproject["tool"]["poetry"]["description"],
    include_package_data=True,
    install_requires=(Path(__file__).parent / "requirements.txt").read_text().splitlines(),
    license=pyproject["tool"]["poetry"]["license"],
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/interactions-py/restful",
    packages=find_packages(),
    python_requires=">=3.8",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
)
