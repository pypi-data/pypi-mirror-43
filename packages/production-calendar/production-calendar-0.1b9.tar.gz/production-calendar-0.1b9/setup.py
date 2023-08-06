from os.path import join, dirname

from setuptools import setup, find_packages

import prodcal

setup(
    name='production-calendar',
    version=prodcal.__version__,
    packages=find_packages(),
    description='Given module allows to use production calendars of different countries',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    test_suite='tests',
    author='Vladimir Sidorov',
    author_email="vladimir.sidorov@raziogroup.com",
    maintainer='Artem Ivanov',
    maintainer_email="ivart@ivart.xyz",
    url='https://github.com/ivanovart/prod-cal',
    license='Apache 2.0',
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Console',
                 'License :: Freeware',
                 'License :: OSI Approved :: Apache Software License',
                 'Natural Language :: English',
                 'Programming Language :: Python :: 3.6',
                 'Topic :: Office/Business',
                 'Topic :: Office/Business :: Scheduling',
                 'Topic :: Utilities'],

)