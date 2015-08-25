#!/usr/bin/env python

from distutils.core import setup
import py2exe

options = {
    "bundle_files": 1,
    "ascii": 1, # to make a smaller executable, don't include the encodings
    "compressed": 1, # compress the library archive
    }

setup(  name = 'AnalyseGPRSServer',
        console = ['AnalyseGPRSServer.py'],
        options = {"py2exe": options},
        version = '1.1',
        zipfile = None, # append zip-archive to the executable.
        data_files=[ ('.', # directory
                     ['AnalyseGPRSServer.conf']), ]

)


