from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='moltin',
    version='0.9.0b1',
    description='Moltin Python SDK',
    long_description=long_description,
    url='https://github.com/moltin/python-sdk',
    author='Moltin, Inc.',
    author_email='support@moltin.com',
    license='MIT',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='ecommerce api sdk',
    install_requires=['requests>=2.7.0,<3.0'],
    extras_require={
        'test': ['sure', 'nose'],
    },
    test_suite='moltin.tests'
)