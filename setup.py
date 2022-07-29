import re
from codecs import open
from os import path

from setuptools import setup, find_packages


# Package information
AUTHOR = "Damego"
AUTHOR_EMAIL = "danyabatueff@gmail.com"
DESCRIPITON = "The cooooool description of your project"
PROJECT_NAME = "project.py"
MAIN_PACKAGE_NAME = "project"
URL = "https://github.com/Damego/..."

# Other variables
HERE = path.abspath(path.dirname(__file__))

with open("README.md", "r", encoding="utf-8") as f:
    README = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read()

# Documentation requiremets
# with open("requirements-docs.txt", "r", encoding="utf-8") as f:
#     requirements_docs = f.read()

with open(path.join(HERE, MAIN_PACKAGE_NAME, "__init__.py"), encoding="utf-8") as fp:
    VERSION = re.search('__version__ = "([^"]+)"', fp.read())[1]


setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPITON,
    # extras_require={"readthedocs": requirements_docs},
    include_package_data=True,
    install_requires=requirements,
    license="GPL-3.0 License",
    long_description=README,
    long_description_content_type="text/markdown",
    url=URL,
    packages=find_packages(),
    python_requires=">=3.8",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
)
