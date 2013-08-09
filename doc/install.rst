Installation
========================================================================

Software requirements
------------------------------------------------------------------------

PyXDA has been written in the Python programming language, therefore
to use the software, you must have Python 2.6 or Python 2.7 installed. In 
addition, the following third-party Python libraries are also required:

* distribute - tools for installing Python packages
* Traits - type checking for Python
* Traits UI - visualization for Traits
* NumPy - library for scientific computing with Python
* Chaco - Python plotting library
* PyFace - another graphics tool for use with Traits 

Standard Python releases can be obtained from
http://www.python.org/download/.
The third-party libraries can be found at the
`Python Package Index <http://pypi.python.org/pypi>`_
or using any Internet search engine.

Another, more convenient option is to obtain science-oriented Python
distributions, such as `PythonXY <https://code.google.com/p/pythonxy/>`_
or `Enthought Canopy <http://www.enthought.com/>`_.  These distributions
already include all the necessary libraries, so the required Python
software can be all installed in one step.

We HIGHLY RECOMMEND using the `Enthought Python Distribution 
<https://www.enthought.com/products/epd/free/>`_, which is available for free.

On Windows operating system, it may be necessary to add the
``C:\Python27`` directory and the scripts directory
``C:\Python27\Scripts`` to the system :envvar:`!PATH`.
Some Python distributions may already do that as a part of their
installation process.  The easiest way to check is to start the
:program:`Command Prompt`, type ``python`` and see if this
starts the Python interpreter.

PyXDA installation
------------------------------------------------------------------------

PyXDA is available as a ZIP on `GitHub <https://github.com/mik854e/pyxda>`_.

Download the ZIP by clicking the button on the right, locate it on your 
computer, and unpackage it.

Once this is done, start the command prompt on Windows or the Unix terminal on Linux or Mac, and navigate to the unpackaged directory.

Once there, run the following command::

    python setup.py develop

Since this project is still in the development phase, this command will allow
users to more easily download new features and fixes. If a new build is 
released, the user need only download the new directory into the same location
and remove the old build. This avoids the hassle of installing everytime a 
build is released.

To verify if PyXDA has been correctly installed, type the following command::

  pyxda

This should display the software version and a list of further commands.
