This guide is originally from [Tutsplus](https://code.tutsplus.com/tutorials/how-to-write-package-and-distribute-a-library-in-python--cms-28693). Full credit goes to them, this is just a condensed version for my reference.


### The Pathology Package

Let's quickly write a little Python 3 package to illustrate all of the below.
A basic library to get started with.

Here is the implementation:

```
import pathlib
import inspect
 
class Path(type(pathlib.Path())):
    @staticmethod
    def script_dir():
        print(inspect.stack()[1].filename)
        p = pathlib.Path(inspect.stack()[1].filename)
        return p.parent.resolve()
```

### Testing the Pathology Package

Here are the tests using the standard unit test framework: 

```
import os
import shutil 
from unittest import TestCase
from pathology.path import Path
 
 
class PathTest(TestCase):
    def test_script_dir(self):
        expected = os.path.abspath(os.path.dirname(__file__))
        actual = str(Path.script_dir())
        self.assertEqual(expected, actual)
 
    def test_file_access(self):
        script_dir = os.path.abspath(os.path.dirname(__file__))
        subdir = os.path.join(script_dir, 'test_data')
        if Path(subdir).is_dir():
            shutil.rmtree(subdir)
        os.makedirs(subdir)
        file_path = str(Path(subdir)/'file.txt')
        content = '123'
        open(file_path, 'w').write(content)
        test_path = Path.script_dir()/subdir/'file.txt'
        actual = open(str(test_path)).read()
 
        self.assertEqual(content, actual)
```

### How to Package a Python Library

Now that we have our code and tests, let's package it all into a proper library. Python provides an easy way via the setup module. You create a file called setup.py in your package's root directory. Then, to create a source distribution, you run: python setup.py sdist

To create a binary distribution called a wheel, you run: python setup.py bdist_wheel

Here is the setup.py file of the pathology package:

```
from setuptools import setup, find_packages
 
setup(name='pathology',
      version='0.1',
      url='https://github.com/the-gigi/pathology',
      license='MIT',
      author='Gigi Sayfan',
      author_email='the.gigi@gmail.com',
      description='Add static script_dir() method to Path',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      zip_safe=False)
```

Let's build a source distribution:

```
> $ python setup.py sdist
```

The result is a tar-gzipped file under the dist directory.

And here is a binary distribution:

```
> $ python setup.py bdist_wheel
```

The pathology package contains only pure Python modules, so a universal package can be built. If your package includes C extensions, you'll have to build a separate wheel for each platform.

### How to Distribute a Python Package

Python has a central package repository called PyPI we need to upload it to PyPI and provide some extra metadata PyPI requires. The steps are:

* Create an account on PyPI (just once).
* Register your package.
* Upload your package.

### Create an Account

You can create an account on the PyPI website. Then create a .pypirc file in your home directory:

```
[distutils] 
index-servers=pypi
  
[pypi]
repository = https://pypi.python.org/pypi
username = the_gigi
For testing purposes, you can add a "pypitest" index server to your .pypirc file:

[distutils]
index-servers=
    pypi
    pypitest
 
[pypitest]
repository = https://testpypi.python.org/pypi
username = the_gigi
 
[pypi]
repository = https://pypi.python.org/pypi
username = the_gigi
```

### Register Your Package

If this is the first release of your package, you need to register it with PyPI. Use the register command of setup.py. It will ask you for your password. Note that I point it to the test repository here:

```
> $ python setup.py register -r pypitest
```

### Upload Your Package

Now that the package is registered, we can upload it. I recommend using twine, which is more secure. Install it as usual using pip install twine. Then upload your package using twine and provide your password (redacted below):

```
> $ twine upload -r pypitest -p <redacted> dist/*
```