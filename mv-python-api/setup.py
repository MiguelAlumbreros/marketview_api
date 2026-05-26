from setuptools import setup, find_packages

setup(
    name='mvconnectivity',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
        'pandas>=1.3.0',
        'python-dateutil>=2.8.1',
    ],
)