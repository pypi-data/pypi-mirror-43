import re
from distutils.core import setup

version = re.search('^__version__\s*=\s*"(.*)"', open("cognite/logger/__init__.py").read(), re.M).group(1)

setup(
    name="cognite-logger",
    version=version,
    author="Stian Lågstad",
    author_email="stian.lagstad@cognite.com",
    include_package_data=True,
    url="https://github.com/cognitedata/python-logger",
    packages=["cognite.logger"],
    description="Simple logging wrapper.",
    install_requires=["python-json-logger==0.1.8"],
)
