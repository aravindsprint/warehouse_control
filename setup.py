# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

setup(
	name="warehouse_control",
	version="1.0.0",
	description="Building-based warehouse access control for ERPNext",
	author="Aravind",
	author_email="aravindsprint@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)