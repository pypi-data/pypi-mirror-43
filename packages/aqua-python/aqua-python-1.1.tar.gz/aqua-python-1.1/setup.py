import setuptools
from distutils.core import setup

setup(
        name='aqua-python',
        version='1.1',
        packages=['formatter',],
        entry_points={'console_scripts': ['aqua = formatter.aqua:main']},
        data_files=[('formatter', ['formatter/__init__.py', 'formatter/aqua.py']),],
        author='Alexander J. Zerphy',
        author_email='ajz5109@psu.edu',
        license='GPL-3.0',
        description='A simple formatter for Python code that adheres to the PEP8 standards',
        long_description=open('README.txt').read(),
    )
