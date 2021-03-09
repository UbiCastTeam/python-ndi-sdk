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
      requires=['logging', 'ctypes', 'enum', 'pydbus'],
      scripts=['bin/mc-magewell-signal', 'bin/mw-capture-dbus-daemon'],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: LPGL v2.1 License",
          "Operating System :: OS Independent",
      ],
      data_files=[
          ('/usr/share/dbus-1/system.d/', ['dbus-1/system.d/com.magewell.MWCapture.conf']),
          ('/usr/share/dbus-1/system-services/', ['dbus-1/system-services/com.magewell.MWCapture.service']),
      ],
      )
