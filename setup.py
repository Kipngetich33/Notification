# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in notification/__init__.py
from notification import __version__ as version

setup(
	name='notification',
	version=version,
	description='this is an app that allows sending out of notifications through sms and email',
	author='Upande LTD.',
	author_email='dev@upande.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
