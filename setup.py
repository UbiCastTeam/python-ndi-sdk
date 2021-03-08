#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='python-ndi-sdk',
      version='1.0',
      description='Python Ndi SDK',
      author='Paul Goulpié',
      author_email='paul.goulpie@ubicast.eu',
      url='https://github.com/UbiCastTeam/python-ndi-sdk',
      packages=['magewell'],
      requires=['logging', 'ctypes', 'enum'],
      scripts=['bin/mc-magewell-signal'],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: LPGL v2.1 License",
          "Operating System :: OS Independent",
      ],
      )
