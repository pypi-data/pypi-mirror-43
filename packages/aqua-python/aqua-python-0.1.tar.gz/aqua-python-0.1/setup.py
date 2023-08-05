from distutils.core import setup

setup(
        name='aqua-python',
        version='0.1',
        packages=['formatter',],
        author='Alexander J. Zerphy',
        author_email='ajz5109@psu.edu',
        license='Alexander J. Zerphy, 2019',
        description='A simple formatter for Python code that adheres to the PEP8 standards',
        long_description=open('README.txt').read(),
    )
