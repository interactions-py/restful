from interactions.ext.base import Base
from interactions.ext.version import Version, VersionAuthor

from .main import *  # noqa


version = Version(
    version="0.0.1",
    author=VersionAuthor(
        name="Damego",
        email="danyabatueff@gmail.com"
    )
)

base = Base(
    name="simple_api",
    version=version,
    description="REST api for your bot",
    link="https://github.com/Damego/interactions-simple-api",
    packages=["interactions.ext.api"],
    requirements=[
        "discord-py-interactions",
    ],
)
