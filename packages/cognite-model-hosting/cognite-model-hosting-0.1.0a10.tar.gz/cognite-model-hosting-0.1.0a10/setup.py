import re

from setuptools import find_packages, setup

packages = find_packages(exclude=["tests*"])

version = re.search('^__version__\s*=\s*"(.*)"', open("cognite/model_hosting/_version.py").read(), re.M).group(1)

setup(
    name="cognite-model-hosting",
    version=version,
    description="Utilities Cognite's model hosting environment",
    url="",  # TODO
    author="Nils Barlaug",
    author_email="nils.barlaug@cognite.com",
    packages=packages,
    install_requires=["pandas", "marshmallow==3.0.0rc4", "requests>=2.21.0,<3.0.0"],
    python_requires=">=3.5",
)
