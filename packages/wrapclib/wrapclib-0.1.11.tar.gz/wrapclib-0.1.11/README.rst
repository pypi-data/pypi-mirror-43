.. image:: https://travis-ci.org/sdpython/wrapclib.svg?branch=master
    :target: https://travis-ci.org/sdpython/wrapclib
    :alt: Build status

.. image:: https://ci.appveyor.com/api/projects/status/auonxiihm1eihv3t?svg=true
    :target: https://ci.appveyor.com/project/sdpython/wrapclib
    :alt: Build Status Windows

.. image:: https://circleci.com/gh/sdpython/wrapclib/tree/master.svg?style=svg
    :target: https://circleci.com/gh/sdpython/wrapclib/tree/master

.. image:: https://dev.azure.com/xavierdupre3/wrapclib/_apis/build/status/sdpython.wrapclib
    :target: https://dev.azure.com/xavierdupre3/wrapclib/

.. image:: https://badge.fury.io/py/wrapclib.svg
    :target: https://pypi.org/project/wrapclib/

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :alt: MIT License
    :target: http://opensource.org/licenses/MIT

.. image:: https://requires.io/github/sdpython/wrapclib/requirements.svg?branch=master
     :target: https://requires.io/github/sdpython/wrapclib/requirements/?branch=master
     :alt: Requirements Status

.. image:: https://codecov.io/github/sdpython/wrapclib/coverage.svg?branch=master
    :target: https://codecov.io/github/sdpython/wrapclib?branch=master

.. image:: http://img.shields.io/github/issues/sdpython/wrapclib.png
    :alt: GitHub Issues
    :target: https://github.com/sdpython/wrapclib/issues

.. image:: https://badge.waffle.io/sdpython/wrapclib.png?label=to%20do&title=to%20do
    :alt: Waffle
    :target: https://waffle.io/wrapclib/wrapclib

.. image:: http://www.xavierdupre.fr/app/wrapclib/helpsphinx/_images/nbcov.png
    :target: http://www.xavierdupre.fr/app/wrapclib/helpsphinx/all_notebooks_coverage.html
    :alt: Notebook Coverage

.. _l-README:

wrapclib
========

*wrapclib* is a wrapper for some C libraries difficult to build
otherwise. One if them is
`re2 <https://github.com/google/re2>`_
with some taken from
`pyre2 <https://github.com/facebook/pyre2>`_.

::

    from wrapclib import re2
    s = "<h1>mot</h1>"
    print(re2.compile("(<.*>)").match(s).groups())

**Links:**

* `GitHub/wrapclib <https://github.com/sdpython/wrapclib/>`_
* `documentation <http://www.xavierdupre.fr/app/wrapclib/helpsphinx/index.html>`_
* `Blog <http://www.xavierdupre.fr/app/wrapclib/helpsphinx/blog/main_0000.html#ap-main-0>`_
