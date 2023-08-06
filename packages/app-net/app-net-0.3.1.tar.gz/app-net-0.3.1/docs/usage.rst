=====
Usage
=====

Core Concepts
-------------
app-net uses peer-to-peer socket servers to execute code both locally and remotely. The first
thing to understand is the difference between **local** and **remote** execution of a function.

Local
+++++
When you launch python and you execute a function, it will execute inside that instance, obviously.
app-net requires you the developer to define the peer id to execute the function on. If you don't
tell the function where to execute the code, it will default to a normal pass-through. This makes
development and testing easier. The response locally is expected to match a remote peers response.

Remote
++++++
When you execute a function, you can tell it to **connect** to a different instance of python,
execute the code, and return the result through the socket response. The thing to understand is
that a **remote** instance doesn't need to be on another host. Meaning, if you have 2 instances
of python running app-net on the same host, they can communicate the same way they would if they
were on a different host.

A Basic Example
---------------
Each connected function is registered using the functions ``func.__module__`` and ``func.__name__``
attributes and then encoded into base64 for easier transit between peers. This connection
identifier is called a "tag". So, when Peer1 wants to execute a function on Peer2, it will send
a JSON request that has the args, kwargs and the tag. The tag is then used to find the function
in Peer2's registry and then pass the args and kwargs to that function. If it succeeds, the
result is sent back to Peer1. If not, the traceback is captured and sent back and Peer1 will
throw a matching error.

We are going to write a very simple application that will multiply 2 values together.
Then we will flag this function as a "connect" function. Then we will launch 2 instances on our
local host, and trigger execution calls between the instances.

Firstly, we will define a our basic multiply function. Then we will flag it with the
``net.connect`` decorator. This connect function will launch a ``net.Peer`` server and register
our ``multiply_values`` function with it.


.. code-block:: python

    import net

    # application code
    @net.connect()
    def multiply_values(val1, val2):
        return val1 * val2



.. code-block:: python

    >>> import net
    >>>
    >>> # get all net peers reachable on local host and the local area network.
    >>> for peer_id in net.get_peers():
    >>>     #
    >>>     print(multiply_values(5, 10, peer=peer_id))
    50
    ...


.. code-block:: python

    >>> import net
    >>>
    >>> # get all net peers reachable on local host and the local area network.
    >>> for peer_id in net.get_peers():
    >>>     #
    >>>     print(multiply_values(5, 10, peer=peer_id))
    50
    ...