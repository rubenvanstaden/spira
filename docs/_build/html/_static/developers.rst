Developers
==========

Documentation for developers for maintaining and extending.
To instead install ExVerify from source, clone this repository, *cd* into it, and run:

```bash
pip install -r requirements.txt
pip install .
pip install -e .
```

Uploading package to PyPi using *twine*:

Remember to remove all Eggs before doing a push to PyPi.

```bash
sudo python3 setup.py bdist_wheel
twine upload dist/*
```

To install package systemwide set the prefix value when running setuptools:

```bash
sudo python3 setup.py install --prefix=/usr
```

or

NB dont use sudo or --user when install from sourc ein a virtual enviroment.

```bash
sudo python3 -m pip install --upgrade .
```

* https://docs.python.org/3.3/install/index.html

Unit testing overview: http://docs.python-guide.org/en/latest/writing/tests/

Documentation
-------------

If you want to generate the docs make sure the Napoleon package is installed:

```bash
pip install sphinxcontrib-napoleon
```

Coding standards for parsing the correct docs is given in:

* https://sphinxcontrib-napoleon.readthedocs.io/en/latest/

* https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt

Introduction to Python Virtual Enviroments:

* https://realpython.com/python-virtual-environments-a-primer/
* https://stackoverflow.com/questions/15746675/how-to-write-a-python-module-package
