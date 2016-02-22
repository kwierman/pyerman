# Pyerman
The python playspace for Kevin Wierman and his notebooks. Some of this will be broken out into separate modules in the future

Features:
* ROOT
    * In-line file streaming using generator objects instead of c-style array copying
    * Safe library importing (uses root-config to bypass framework-oriented systems. I'm looking at you, OSX)
    * Some stream-lined functions for pulling objects out of files.
* Tables
    * Tabular data slicing (horiz and vert)
    * Paintable objects in IPython notebooks
* Statistics
    * GaussianValues automatically calculate statistics for iterable objects
    * Represents in scientific format
* Style
    * Improved color tables for graphic readability
    * Painter/Actor patterns for plotting in notebooks
* Configuration
    * Allows configuration of analyses on the fly
    * Reads and writes configs for workspaces
* LSF
    * Remote management of LSF-based cluster system
    * Move files around
    * Submit jobs
    * Never have to shell into a system again

# Installation

Using pip:
~~~
   pip install git+https://github.com/kwierman/pyerman/
~~~

Cloning from github:
~~~
   git clone https://github.com/kwierman/pyerman/
   cd pyerman
   python setup.py install
~~~
