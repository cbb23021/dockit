#!/usr/bin/env python
from setuptools import find_packages, setup

from src import mkit

with open("README.md", "r") as f:
    long_description = f.read()

setup(name='mkit',
      version=mkit.__version__,
      description=mkit.__doc__,
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Michael Chou',
      author_email='snoopy02m@gmail.com',
      url='https://github.com/cbb23021/mkit',
      packages=find_packages(),
      license='MIT',
      python_requires='>=3.7',
      install_requires=[
          'click==8.0.3',
          'click-help-colors==0.9.1',
          'colorama==0.4.6',
      ],
      classifiers=[
          'Operating System :: Unix',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7',
          'Topic :: Terminals',
      ],
      entry_points={
          'console_scripts': ['mkit = mkit.__main__:cli'],
      })
