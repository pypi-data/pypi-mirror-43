# -*- coding: utf-8 -*-
from setuptools import setup,find_packages

setup(name='webautomators',
      version='0.1',
      url='',
      license='Indra Company',
      author='Kaue Bonfim',
      author_email='koliveirab@indracompany.com',
      description='Automation library for test web with selenium',
      packages=['webautomators',],
	install_requires=['selenium', 'requests'],
      zip_safe=True)