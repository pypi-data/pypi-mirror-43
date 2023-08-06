Kickoff
=======

`Kickoff` turns your Python script or module into an application with decent user interface.

**For software developers...**

`Kickoff` is inspired by utilities like `invoke <http://www.pyinvoke.org>`__, `fire <https://github.com/google/python-fire>`__, `runfile <https://code.activestate.com/pypm/runfile/>`__. It has similar function with this difference that it looks at function signatures, therefore doesn't need from the developer to use decorators or any dedicated API. This way `Kickoff` provides developers with following advantages:

* Basic UI provided with zero overhead
* Enhanced UI provided through annotations
* Compatibility with environments where `Kickoff` is not installed
* Testability and reusability of top-level commands
* Shebang support

**For software users...**

`Kickoff` is built on top of stunning `click <https://click.palletsprojects.com/>`__ module as well as third-party add-ons to provide the users with following features:

* Hierarchical CLI interface
* Correction suggestions for misspelled commands
* REPL with command completion and access to underlying shell
* GUI (experimental feature)

Development
===========

Preparing Environment
^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    ./setup.sh

Releasing
^^^^^^^^^

.. code:: python

    # update version:
    vi docs/source/conf.py
    vi setup.py
    git tag 1.2.3
    git commit -am "foobar"
    
    # upload code
    git push --tags

    # upload documentation






        