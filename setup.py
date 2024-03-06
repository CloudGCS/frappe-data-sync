from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in data_sync/__init__.py
from data_sync import __version__ as version

setup(
	name="data_sync",
	version=version,
	description="Data Sync Module for CloudGCS",
	author="CloudGCS",
	author_email="hello@cloudgcs.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
