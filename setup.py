from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='ale',
   version='0.1',
   description='Molecular Dynamics At Lowest Effort',
   license="MIT",
   long_description=long_description,
   author='ALEchemists',
   author_email='',
   url="https://github.com/martinclason/Molecular-Dynamics-Project",
   packages=['ale'],  #same as name
   install_requires=['ase'], #external packages as dependencies
   # This entry_point method also works but using scripts seems 
   # to be the more modern and recommended method.
   # entry_points={'console_scripts': ['ale=ale.main:run']},
   scripts=[
            'scripts/ale',
           ]
)
