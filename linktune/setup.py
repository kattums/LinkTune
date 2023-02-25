from setuptools import setup, find_packages
from pip._internal.req import parse_requirements

# Parse the requirements.txt file
requirements = parse_requirements('requirements.txt', session='hack')

setup(
    name='linktune',
    version='0.1',
    install_requires=[str(req.requirement) for req in requirements],
    packages=find_packages(),
    py_modules=['api', 'cli', 'config'],
    entry_points={
    'console_scripts': [
        'linktune = cli.main:main'
        ]
    }
)