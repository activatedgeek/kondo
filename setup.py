import os
from setuptools import setup, find_packages


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
      python_requires='>=3.6, <4',
      tests_require=[
          'pytest>=4.2'
      ],
      install_requires=['numpy'],
      extras_require={
          'test': ['pytest>=4.2'],
          'all': ['torch', 'tensorflow']
      })
