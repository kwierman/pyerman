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

for sub in os.listdir('pyerman'):
    subdir = os.path.join('pyerman', sub)
    if os.path.isdir(subdir):
        for subsub in os.listdir(subdir):
            subsubdir = os.path.join(subdir, subsub)
            if os.path.isdir(subsubdir):
                for subsubsub in os.listdir(subsubdir):
                    subsubsubdir = os.path.join(subsubdir, subsubsub)
                    if not os.path.isdir(subsubsubdir):
                        shutil.copyfile(subsubsubdir, subsubsubdir+"x")
            else:
                shutil.copyfile(subsubdir, subsubdir+"x")
    else:
        shutil.copyfile(subdir, subdir+"x")


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
