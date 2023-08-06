app-net
=======

![PyPI](https://img.shields.io/pypi/v/net.svg)
![PyLint](https://mperlet.github.io/pybadge/badges/8.52.svg)
![Travis](https://img.shields.io/travis/aldmbmtl/net.svg)
![Documentation Status](https://readthedocs.org/projects/net/badge/?version=latest)
![PyUp](https://pyup.io/repos/github/aldmbmtl/net/shield.svg)
![Python 3](https://pyup.io/repos/github/aldmbmtl/net/python-3-shield.svg)
![License](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)

Pure python peer-to-peer interfacing framework. Define functions that
can be executed from within the running instance of python, just like a
normal function. Or execute the same function on a remote peer running
either the same application or a compatible function and return the
result as though it was run locally.

Link to the [Documentation](https://app-net.readthedocs.io/en/latest/?).

Basic Example
-------------

Below is a basic example of defining an application that is running on 2
separate hosts independently. We will define a simple function that will
take a positional argument and keyword argument then multiplies them
together and returns the result.

First we will define our function

```python
import net

@net.connect()
def my_function(some_arg, some_kwarg=5):
    return some_arg * some_kwarg
```

Now we can launch 2 instances of python. It can be either on the same or
remote host, net handles this through peer ids.

```python
>>> import net
>>> # run this function locally on this instance of python
>>> my_function(5, some_kwarg=10)
50
>>> # get all peers on the network
>>> for peer_id in net.peers():
...     # execute the same function but on other instances of python and return the results
...     print(my_function(5, some_kwarg=10, peer=peer_id))
...
50
```