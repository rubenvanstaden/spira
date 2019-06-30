Developers
==========

Documentation for developers for maintaining and extending. Extra information is added
to better understand specific code implementations.

.. Distribtuion
.. ------------

.. Uploading package to PyPi using *twine*.
.. Remember to remove all Eggs before doing a push to PyPi.

.. .. code-block:: bash
..     :linenos:

..     sudo python3 setup.py bdist_wheel
..     twine upload dist/*

.. To install package systemwide set the prefix value when running setuptools:

.. .. code-block:: bash
..     :linenos:

..     sudo python3 setup.py install --prefix=/usr

.. .. code-block:: bash
..     :linenos:

..     sudo python3 -m pip install --upgrade .

.. * https://docs.python.org/3.3/install/index.html

.. Unit testing overview: http://docs.python-guide.org/en/latest/writing/tests/

.. Documentation
.. -------------

.. If you want to generate the docs make sure the Napoleon package is installed:

.. .. code-block:: bash
..     :linenos:

..     pip install sphinxcontrib-napoleon

.. Coding standards for parsing the correct docs is given in:

.. * https://sphinxcontrib-napoleon.readthedocs.io/en/latest/

.. * https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt

.. Introduction to Python Virtual Enviroments:

.. * https://realpython.com/python-virtual-environments-a-primer/
.. * https://stackoverflow.com/questions/15746675/how-to-write-a-python-module-package

.. .. ---------------------------------------------------------------------------------------------

.. Mixins
.. ------

.. The following are useful links to some of the mixin implementations used in the SPiRA framework,

.. * http://tobyho.com/2009/01/18/auto-mixin-in-python/
.. * http://code.activestate.com/recipes/577730-mixin-and-overlay/
.. * https://stackoverflow.com/questions/6966772/using-the-call-
.. * method-of-a-metaclass-instead-of-new

.. Metaprogramming
.. ---------------



