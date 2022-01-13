from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

dependencies_unavailable_in_pip = [
    'kim-api',
    'openkim-models',
    'openmpi',
]

setup(
   name='ale',
   version='0.1',
   description='Molecular Dynamics At Lowest Effort',
   license="MIT",
   long_description=long_description,
   author='ALEchemists',
   author_email='',
   url="https://github.com/martinclason/Molecular-Dynamics-Project",
   packages=['ale', 'ale.plotting'],  #same as name
   install_requires=[ #external packages as dependencies
        'Cython',
        'numpy',
        'scipy',
        'matplotlib',
        'ase',
        'asap3',
        'pyyaml',
        'sphinx',
        'kimpy',
        'mpi4py',
        'pytest',
        # The packages below must be installed another way, e.g. with conda
        # 'kim-api',
        # 'openkim-models',
        # 'openmpi',
   ],
   # This entry_point method also works but using scripts seems
   # to be the more modern and recommended method.
   # entry_points={'console_scripts': ['ale=ale.main:run']},
   scripts=[
            'scripts/ale',
           ]
)

print(f"""
IMPORTANT:
    For this software to work as intended, make sure
    you before installation have the following dependencies installed (e.g. with conda):
    {dependencies_unavailable_in_pip}
""")
