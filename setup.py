from setuptools import setup, find_packages
import sys, os, shutil
from Cython.Build import cythonize

version = '0.2.1'

def parse_requirements(requirements):
    f = open(requirements,'r')
    req=[]
    for l in f.readlines():
        if not l.startswith('#'):
            req.append(l.strip('\n'))
    return (i for i in req)


requirements = parse_requirements('requirements.txt')

def copy_to_px(path):
    """
    path must be an absolute path to a directory
    """
    for sub in os.listdir(path):
        full_path = os.path.join(path, sub)
        if os.path.isdir(full_path):
            copy_to_px(full_path)
        elif full_path.endswith(".py"):
            shutil.copyfile(full_path, full_path+"x")

copy_to_px('pyerman')


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
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="wierman, lsf, katrin, kassiopeia, ROOT",
    author="Kevin Wierman",
    author_email='kwierman@gmail.com',
    url="https://github.com/kwierman/pyerman",
    license='BSD',
    requires = requirements,
    packages=find_packages(exclude=[]),
    ext_modules = cythonize("pyerman/*/*.pyx")
)
