from setuptools import setup, find_packages
import sys,
from Cython.Build import cythonize

version = '0.2'

def parse_requirements(requirements):
    f = open(requirements,'r')
    req=[]
    for l in f.readlines():
        if not l.startswith('#'):
            req.append(l.strip('\n'))
    return (i for i in req)


requirements = parse_requirements('requirements.txt')

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
    requires = requirements,
    packages=find_packages(exclude=[]),
    ext_modules = cythonize("pyerman/*/*.pyx")
)
