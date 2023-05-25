#!/usr/bin/env python
try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

README = read('README.md')

setup(name='whisperyt',
      packages      = ['whisperyt','whisperyt.config'],
      description   = 'A simple Python module for generating youtube video transcription.',
      long_description = README,
      long_description_content_type = "text/x-rst",
      version       = 1.0,
      url           = "https://github.com/egrissino/whisper-youtube/tree/main",
      author        = "Evan Grissino",
      author_email  = "evanjGrissino@gmail.com",
      license       = "GNU GPL",
      keywords      = ['whisper','loadModel','downloadVideo','getTranscript'],
      classifiers = [
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
          'Programming Language :: Python :: 3',
          'Development Status :: 5 - Production/Stable',
          'Natural Language :: English',
          "Topic :: Software Development :: Libraries :: Python Modules",
          'Topic :: Text Processing :: Linguistic',
      ]
      )
