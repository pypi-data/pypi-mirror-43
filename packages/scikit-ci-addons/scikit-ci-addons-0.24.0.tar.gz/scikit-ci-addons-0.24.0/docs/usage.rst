=====
Usage
=====

The scikit-ci-addons command line executable allows to discover, execute and
get the path of any of the distributed :doc:`add-ons </addons>`.

Executing an add-on
-------------------

::

    ci_addons ADDON_NAME

where ``ADDON_NAME`` can be any of the names displayed using ``ci_addons --list``.

For example:

.. code-block:: bash

    $ ci_addons appveyor/patch_vs2008


Listing available add-ons
-------------------------

::

    ci_addons --list


For example:

.. code-block:: bash

    $ ci_addons --list

    anyci/ctest_junit_formatter.py
    anyci/publish_github_release.py
    anyci/run.sh
    anyci/ctest_junit_formatter.xsl
    anyci/noop.py
    anyci/docker.py

    appveyor/enable-worker-remote-access.ps1
    appveyor/install_cmake.py
    appveyor/apply_mingw_path_fix.py
    appveyor/run.cmd
    appveyor/patch_vs2008.py
    appveyor/run-with-mingw.cmd
    appveyor/cancel-queued-build.ps1
    appveyor/rolling-build.ps1
    appveyor/tweak_environment.py
    appveyor/run-with-visual-studio.cmd

    circle/install_cmake.py

    travis/install_cmake.py
    travis/enable-worker-remote-access.sh
    travis/run-with-pyenv.sh
    travis/install_pyenv.py

    windows/install-miniconda3.ps1
    windows/install-utils.ps1
    windows/install-cmake.ps1
    windows/install-python-27-x64.ps1
    windows/install-nsis.ps1
    windows/install-svn.ps1
    windows/install-ninja.ps1
    windows/install-python.ps1
    windows/install-python-36-x64.ps1
    windows/install-git.ps1
    windows/install-flang.ps1

.. note::

    To learn more about each add-on, consider reading the
    :doc:`add-ons </addons>` section.


Getting directory containing all add-ons
----------------------------------------

::

    ci_addons --home

For example:

.. code-block:: bash

    $ ci_addons --home
    /home/jcfr/.virtualenvs/test/local/lib/python2.7/site-packages


Installing add-ons into selected directory
------------------------------------------

::

    ci_addons --install DIR

where ``DIR`` is a valid path to an existing directory.

For example:

.. code-block:: bash

    $ ci_addons --install /tmp
    /tmp/anyci/ctest_junit_formatter.py
    /tmp/anyci/publish_github_release.py
    /tmp/anyci/run.sh
    /tmp/anyci/ctest_junit_formatter.xsl
    /tmp/anyci/noop.py
    /tmp/anyci/docker.py
    /tmp/appveyor/enable-worker-remote-access.ps1
    /tmp/appveyor/install_cmake.py
    /tmp/appveyor/apply_mingw_path_fix.py
    /tmp/appveyor/run.cmd
    /tmp/appveyor/patch_vs2008.py
    /tmp/appveyor/run-with-mingw.cmd
    /tmp/appveyor/cancel-queued-build.ps1
    /tmp/appveyor/rolling-build.ps1
    /tmp/appveyor/tweak_environment.py
    /tmp/appveyor/run-with-visual-studio.cmd
    /tmp/circle/install_cmake.py
    /tmp/travis/install_cmake.py
    /tmp/travis/enable-worker-remote-access.sh
    /tmp/travis/run-with-pyenv.sh
    /tmp/travis/install_pyenv.py
    /tmp/windows/install-miniconda3.ps1
    /tmp/windows/install-utils.ps1
    /tmp/windows/install-cmake.ps1
    /tmp/windows/install-python-27-x64.ps1
    /tmp/windows/install-nsis.ps1
    /tmp/windows/install-svn.ps1
    /tmp/windows/install-ninja.ps1
    /tmp/windows/install-python.ps1
    /tmp/windows/install-python-36-x64.ps1
    /tmp/windows/install-git.ps1
    /tmp/windows/install-flang.ps1


Getting full path of an add-on
------------------------------

::

    ci_addons --path PATH

where ``PATH`` can be any of these:

- relative path with or without extension (e.g ``appveyor/patch_vs2008.py``
  or ``appveyor/patch_vs2008.py``)

- full path (e.g ``/path/to/appveyor/patch_vs2008.py``)

- script name with or without extension (e.g ``patch_vs2008.py``
  or ``patch_vs2008``). If there are multiple add-ons with the same bame,
  ``ci_addons`` reports an error message listing the add-ons to choose from.

For example:

.. code-block:: bash

    $ ci_addons --path appveyor/patch_vs2008.py
    /home/jcfr/.virtualenvs/test/local/lib/python2.7/site-packages/appveyor/patch_vs2008.py

.. note::

    This function is particularly useful when the selected add-on is not a
    python script and is expected to be used as an input to an other tool.


Calling scikit-ci-addons through ``python -m ci_addons``
--------------------------------------------------------

You can invoke scikit-ci-addons through the Python interpreter from the command
line::

    python -m ci_addons [...]

This is equivalent to invoking the command line script ``ci_addons [...]``
directly.


Getting help on version, option names
-------------------------------------

::

    ci_addons --version   # shows where ci_addons was imported from
    ci_addons -h | --help # show help on command line
