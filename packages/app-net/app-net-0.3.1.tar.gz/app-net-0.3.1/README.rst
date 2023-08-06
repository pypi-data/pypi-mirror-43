.. _Documentation: https://app-net.readthedocs.io/en/latest/?
.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

=======
app-net
=======


.. image:: https://img.shields.io/pypi/v/net.svg
        :target: https://pypi.python.org/pypi/app-net

.. image:: https://img.shields.io/travis/aldmbmtl/net.svg
        :target: https://travis-ci.org/aldmbmtl/net

.. image:: https://readthedocs.org/projects/net/badge/?version=latest
        :target: https://net.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/aldmbmtl/net/shield.svg
     :target: https://pyup.io/repos/github/aldmbmtl/net/
     :alt: Updates


.. image:: https://pyup.io/repos/github/aldmbmtl/net/python-3-shield.svg
     :target: https://pyup.io/repos/github/aldmbmtl/net/
     :alt: Python 3


.. image:: https://img.shields.io/github/license/Naereen/StrapDown.js.svg
    :target: https://github.com/Naereen/StrapDown.js/blob/master/LICENSE
    :alt: MIT License

.. image:: https://mperlet.github.io/pybadge/badges/8.52.svg
    :alt: PyLint


Pure python peer-to-peer interfacing framework. Define functions that can be executed from within the
running instance of python, just like a normal function. Or execute the same function on a remote peer
running either the same application or a compatible function and return the result as though it was run
locally.

Link to the Documentation_.

.. include:: ./docs/installation.rst

Basic Example
-------------
Below is a basic example of defining an application that is running on 2 separate hosts independently.
We will define a simple function that will take a positional argument and keyword argument then multiplies
them together and returns the result.

First we will define our function

.. code-block:: python

    import net

    @net.connect
    def my_function(some_arg, some_kwarg=5):
        return some_arg * some_kwarg


Now we can launch 2 instances of python. It can be either on the same or remote host, net handles this through peer ids.

.. code-block:: python

    >>> import net
    >>> # run this function locally on this instance of python
    >>> my_function(5, some_kwarg=10)
    50
    >>> # get all peers on the network
    >>> for peer_id in net.get_peers():
    ...     # execute the same function but on other instances of python and return the results
    ...     print(my_function(5, some_kwarg=10, peer=peer_id))
    ...
    50
