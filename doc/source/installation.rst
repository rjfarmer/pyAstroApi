Installation
============

The easiest way is to use PyPi ::

    pip install pyAstroApi


otherwise to build from source, after checking out the code, ::

    pip install -r requirements.txt


to install the dependencies. Then to build and install software ::

    pip install .


Development
~~~~~~~~~~~

If developing then you'll need additional dependencies ::

    pip install -r requirements_dev.txt


then the test suite can be ran with ::

    pytest

to test one python version. Or, ::

    tox

to run over all supported python versions.