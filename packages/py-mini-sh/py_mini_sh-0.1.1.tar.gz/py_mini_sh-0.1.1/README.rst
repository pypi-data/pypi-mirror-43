
py_mini_sh
==========

.. note:: Version: 0.1.1

This package provides helper functions to simplify the writing of
platform-independent sh-like scripts in Python.

Full documentation can be found at `Read-the-Docs
<http://py-mini-sh.readthedocs.io>`_, the source for which is in the
``docs`` folder.


Using this package
------------------

Either fetch this package directly from Git, or pull it from the Python
Packaging index.

#. Pip-install from Git::

       pip install -U git+https://bitbucket.org/ltunmer/py_mini_sh.git

#. Pip-install from PyPI::

       pip install -U py_mini_sh

   .. note:: The package is not quite available on pypi.org yet.

       

Dog Food
--------

The script used to develop and test this component uses the py_mini_sh
itself. To start development of this component, follow these steps:

#. Clone this repo onto a machine from ``https://bitbucket.org/ltunmer/py_mini_sh.git``::

       git clone https://bitbucket.org/ltunmer/py_mini_sh.git

#. Cd to the ``py_mini_sh`` folder and run the ``buildall`` script in
   this folder::

       buildall 36

   The argument specifies which version of Python you wish to use. 27,
   34, 35, and 36 are supported.


This ``buildall`` script will perform the following steps:

#. Builds a virtualenv derived from the specified version of Python.

#. Installs the py_mini_sh package into this virtualenv in "develop"
   mode.

#. Builds the documentation into the SHIP folder.

#. Runs pylint over the source and fails if the results are worse than
   the previous run.

#. Runs pytest tests which generate a coverage report into the SHIP
   folder.

#. Builds the bdist_wheel for this package into the SHIP folder.


License
-------

This software is made available under the MIT License (see LICENSE.txt).
