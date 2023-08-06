Installation
============

.. contents:: Page contents
   :local:
   :backlinks: none


Requirements
------------

Gomill requires Python 2.5, 2.6, or 2.7.

For Python 2.5 only, the :option:`--parallel <ringmaster --parallel>` feature
requires the external `multiprocessing`__ package.

.. __: https://pypi.org/pypi/multiprocessing

Gomill is intended to run on any modern Unix-like system.


Installing
----------

Gomill can be installed from the Python Package Index::

    pip install gomill

Installing Gomill puts the :mod:`!gomill` package onto the Python module
search path, and the ringmaster executable onto the executable
:envvar:`!PATH`.

To install for the current user only (Python 2.6 or 2.7), run ::

    pip install --user gomill

(In this case the ringmaster executable will be placed in
:file:`~/.local/bin`.)

To remove an installed version of Gomill, run ::

    pip uninstall gomill


Downloading sources and documentation
-------------------------------------

The source distribution can be downloaded from the `Python Package index`__,
or from https://mjw.woodcraft.me.uk/gomill/, as a file named
:file:`gomill-{version}.tar.gz`.

.. __: https://pypi.org/project/gomill/

This documentation is distributed separately in html form at
https://mjw.woodcraft.me.uk/gomill/ as :file:`gomill-doc-{version}.tar.gz`.

The version-control history is available at
https://github.com/mattheww/gomill.

Once you have downloaded the source archive, extract it using a command like
:samp:`tar -xzf gomill-{version}.tar.gz`. This will create a directory named
:file:`gomill-{version}`, referred to below as the :dfn:`distribution
directory`.


Installing from the source distribution
---------------------------------------

- to install into a virtualenv, or for the system as a whole, run (as a
  sufficiently privileged user) ::

    python setup.py install


- to install for the current user only (Python 2.6 or 2.7), run ::

    python setup.py install --user

  (in this case the ringmaster executable will be placed in
  :file:`~/.local/bin`.)

Pass :option:`!--dry-run` to see what these will do. See
https://docs.python.org/2.7/install/ for more information.

To remove a version of Gomill installed in this way, run ::

  python setup.py uninstall

(This uses the Python module search path and the executable :envvar:`!PATH` to
find the files to remove; pass :option:`!--dry-run` to see what it will do.)


Running the ringmaster from the source distribution
---------------------------------------------------

The ringmaster executable in the distribution directory can be run directly
without any further installation; it will use the copy of the :mod:`!gomill`
package in the distribution directory.

A symbolic link to the ringmaster executable will also work, but if you move
the executable elsewhere it will not be able to find the :mod:`!gomill`
package unless the package is installed.


Running the test suite
----------------------

To run the testsuite against the distributed :mod:`!gomill` package, change to
the distribution directory and run ::

  python -m gomill_tests.run_gomill_testsuite


To run the testsuite against an installed :mod:`!gomill` package, change to
the distribution directory and run ::

  python test_installed_gomill.py


With Python versions earlier than 2.7, the unittest2__ library is required
to run the testsuite.

.. __: https://pypi.org/project/unittest2/


.. _running the example scripts:

Running the example scripts
---------------------------

The example scripts are included in the source distribution. To run them, it
is simplest to install the :mod:`!gomill` package first.

If you do not wish to do so, you can run ::

  export PYTHONPATH=<path to the distribution directory>

so that the example scripts will be able to find the :mod:`!gomill` package.


Building the documentation
--------------------------

The sources for this HTML documentation are included in the Gomill source
archive. To rebuild the documentation, change to the distribution directory
and run ::

   python setup.py build_sphinx

The documentation will be generated in :file:`build/sphinx/html`.

Requirements:

- Sphinx__ version 1.0 or later
  (at least 1.0.4 recommended; tested with 1.4)
- LaTeX__
- dvipng__

.. __: https://www.sphinx-doc.org/
.. __: https://www.latex-project.org/
.. __: https://www.nongnu.org/dvipng/

