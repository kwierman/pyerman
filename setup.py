from setuptools import setup, find_packages
import sys, os

version = '0.1'

def parse_requirements(requirements):
    with open(requirements) as f:
        return [l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#')]


requirements = parse_requirements('requirements.txt')
print requirements

setup(
    name='pyerman',
    version=version,
    description="Personal Modules of K. Wierman",
    long_description="""Tables, Gaussian values, Remote LSF Monitoring, etc...""",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        #"Framework :: Paste",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="wierman, killdevil, katrin, kassiopeia",
    author="Kevin Wierman",
    author_email='kwierman@gmail.com',
    url="https://github.com/PEAT-AI/Mappeat",
    license='BSD',
    requires = parse_requirements("requirements.txt"),
    packages=find_packages(exclude=[]),
)
