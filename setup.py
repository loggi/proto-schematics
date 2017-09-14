import codecs
import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


REQUIREMENTS = [
    'schematics',
    'protobuf',
]

TEST_REQUIREMENTS = [
    'flake8',
    'mock',
    'tox',
    'pytest',
    'pytest-cache',
    'pytest-cover',
    'pytest-sugar',
    'pytest-xdist',
]

with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    README = f.read()


setup(name='proto_schematics',
      version='0.1.0',
      description='Converts protobuf generated messages to Python friendly schematics models.',
      long_description=README,
      license='Apache License (2.0)',
      author='Gabriela Surita',
      author_email='gsurita@loggi.com',
      url='https://github.com/loggi/proto-schematics',
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],
      keywords=[
          'loggi',
          'schematics',
          'protobuf',
          'grpc',
      ],
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=REQUIREMENTS,
      test_suite='tests',
      tests_require=TEST_REQUIREMENTS+REQUIREMENTS)
