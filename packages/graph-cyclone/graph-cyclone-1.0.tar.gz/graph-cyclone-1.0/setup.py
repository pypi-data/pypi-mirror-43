from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='graph-cyclone',
   version='1.0',
   description='Utilities for powers of cycle graphs',
   license="GPL",
   long_description=long_description,
   author='Noemi Glaeser',
   author_email='',
   url="https://github.com/nglaeser/graph-cyclone",
   packages=['graph-cyclone'],  #same as name
   install_requires=['numpy', 'random'], #external packages as dependencies
)
