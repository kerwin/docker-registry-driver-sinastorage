#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import setuptools
except ImportError:
    import distutils.core as setuptools


__author__ = 'Kerwin Piao'
__copyright__ = 'Copyright 2014'
__credits__ = []

__version__ = '0.1.1'
__maintainer__ = 'Kerwin Piao'
__email__ = 'piaoyuankui@gmail.com'

__title__ = 'docker-registry-driver-sinastorage'
__build__ = 0x000000

__url__ = 'https://github.com/kerwin/docker-registry-driver-sinastorage'
__description__ = 'Docker registry sinastorage driver'

setuptools.setup(
    name=__title__,
    version=__version__,
    author=__author__,
    author_email=__email__,
    maintainer=__maintainer__,
    maintainer_email=__email__,
    url=__url__,
    description=__description__,
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: Implementation :: CPython',
                 'Operating System :: OS Independent',
                 'Topic :: Utilities'],
    platforms=['Independent'],
    namespace_packages=['docker_registry', 
                        'docker_registry.drivers', 
                        'docker_registry.contrib'],
    packages=['docker_registry', 
              'docker_registry.drivers', 
              'docker_registry.contrib', 
              'docker_registry.contrib.sinastorage'],
    install_requires=[
        "docker-registry-core>=2,<3",
        "filechunkio"
    ],
    zip_safe=True,
    tests_require=[
        "nose==1.3.3",
        "coverage==3.7.1",
    ],
    test_suite='nose.collector'
)

