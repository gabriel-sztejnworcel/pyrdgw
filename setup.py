from setuptools import find_packages, setup

setup(
    name='pyrdgw',
    packages=find_packages(),
    version='0.1.0',
    description='PyRDGW - Remote Desktop Gateway in Python',
    author='Gabriel Sztejnworcel',
    install_requires=['websockets'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)