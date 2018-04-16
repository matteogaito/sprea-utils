"""
Sprea Utils
-------------

Use this module in order to navigate easly on sprea.it
"""
from setuptools import setup


setup(
    name='sprea-utils',
    version='0.1',
    url='https://github.com/matteogaito/sprea-utils.git',
    license='LICENSE',
    author='Matteo Gaito',
    author_email='matteo@gaito.net',
    description='Flask module for Sprea.it navigation',
    long_description=__doc__,
    py_modules=['sprea_utils'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'mechanicalsoup',
        'requests',
        'urllib3',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
