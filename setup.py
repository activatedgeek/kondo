import sys
import os
from setuptools import setup, find_packages

CURRENT_PYTHON = sys.version_info[:2]
MIN_PYTHON = (3, 6)

if CURRENT_PYTHON < MIN_PYTHON:
  sys.stderr.write("""
      ============================
      Unsupported Python Version
      ============================
      Python {}.{} is unsupported. Please use a version newer than Python {}.{}.
  """.format(*CURRENT_PYTHON, *MIN_PYTHON))
  sys.exit(1)

with open('requirements.txt', 'r') as f:
  install_requires = f.readlines()

if os.path.isfile('VERSION'):
  with open('VERSION') as f:
    VERSION = f.read()
else:
  VERSION = os.environ.get('TRAVIS_PULL_REQUEST_BRANCH') or \
            os.environ.get('TRAVIS_BRANCH') or \
            '0.0.dev0'

with open('README.md') as f:
  README = f.read()

setup(name='kondo',
      description='Does your experiment spark joy?',
      long_description=README,
      long_description_content_type='text/markdown',
      version=VERSION,
      url='https://github.com/activatedgeek/kondo',
      author='Sanyam Kapoor',
      license='Apache License 2.0',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
      ],
      packages=find_packages(exclude=[
          'tests',
          'tests.*',
          'examples',
          'examples.*'
      ]),
      install_requires=install_requires)
