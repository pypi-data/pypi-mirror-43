import os

from setuptools import setup, find_packages  # noqa: H301

NAME = "smklog"
VERSION = "1.0.1"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["arrow"]

with open(os.path.join(os.pardir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=NAME,
    version=VERSION,
    description="Samarkand logger",
    author="David Chen",
    author_email="david.chen@samarkand.global",
    url="https://gitlab.com/samarkand-util/smklog",
    keywords=["logger"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
)
