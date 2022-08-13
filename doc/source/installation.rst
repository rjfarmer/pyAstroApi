Installation
============

The easiest way is to use PyPi ::

    pip install pyAstroApi


otherwise to build from source, after checking out the code, ::

    pip install -r requirements.txt


to install the dependencies. Then to build and install software ::

    pip install .

Documentation can be built locally with ::

    cd doc
    make html
    firefox build/html/index.html


ADS key
~~~~~~~

You will need your own ADS api key: https://ui.adsabs.harvard.edu/user/settings/token

This can be saved to the file ::

    ~/.ads/dev_key


This location was chosen to be consistent with Andy Cassey's package.

ORCID Key
~~~~~~~~~

You can saved your ORCID to ::

    ~/.dev/orcid

