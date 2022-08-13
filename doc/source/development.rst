Development
===========

If developing then you'll need additional dependencies ::

    pip install -r requirements_dev.txt


then the test suite can be ran with ::

    pytest

to test one python version. Or, ::

    tox

to run over all supported python versions.

We use `black` to auto format the code. There is an pre-commit hook that can be used to run `black` on each commit.

Test suite
~~~~~~~~~~

The test suite uses `pyvcr` to cache web requests. Thus when running `pytest` we don't use the ADS API at all. 

Running all tests with the ADS API requires removing the contents of `test/cassesttes`. Note this will hammer your ADS limits 
(some endpoints have a smaller 100 per day limit rather than the 5000 of the regular search). This should be done before a release to test for changes in the API.
