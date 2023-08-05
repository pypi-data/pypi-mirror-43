# -*- coding: utf-8 -*-

# std imports
import os
import socket
from logging import debug

# third party
import termcolor

# package imports
from net import PeerHandler
from .imports import socketserver, ConnectionRefusedError


# globals
SINGLETON = None


class _Peer(socketserver.ThreadingMixIn, socketserver.TCPServer, object):  # adding in object for 2.7 support
    def __init__(self, test=False):

        # mask with singleton catch unless being tested
        if SINGLETON and not test:
            raise RuntimeError(
                "Can not create a new peer in without shutting down the previous one. Please use net.Peer() instead."
            )

        # find port
        self._port = self.scan_for_port()
        self._host = 'localhost'

        super(_Peer, self).__init__((self.host, self.port), PeerHandler)

    @property
    def port(self):
        """
        Port that the peer is running on.
        :return:
        """
        return self._port

    @property
    def host(self):
        """
        Host that the peer is running on.
        :return:
        """
        return self._host

    @staticmethod
    def ping(port, host='localhost'):
        """
        Ping a port and check if it is alive or open.

        :param port: required port to hit
        :param host: host address default is 'localhost'
        :return:
        """

        interface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            interface.connect((host, port))
            return True
        except ConnectionRefusedError:
            return False

    @classmethod
    def scan_for_port(cls):
        """
        Scan for a free port to bind to. You can override the default port range and search range by setting the
        environment variables NET_PORT NET_PORT_RANGE.

        Port range:
            default 3010-3050

        :return: int
        """
        # cast as int and default to 3010 and 40
        port = int(os.environ.setdefault("NET_PORT", "3010"))
        port_range = port + int(os.environ.setdefault("NET_PORT_RANGE", "40"))

        debug("Scanning {} ports for open port...".format(port_range - port))
        while port <= port_range:

            # ping the local host ports
            if not cls.ping(port):
                debug("Found Port: {}".format(termcolor.colored(port, "green")))
                break

            port += 1

        # throw error if there is no open port
        if port > port_range:
            raise ValueError("No open port found between {} - {}".format(port, port_range))

        # return found port
        return port


def Peer(test=False):
    """
    Running Peer server for this instance of python.
    :return: _peer
    """
    global SINGLETON

    # handle singleton behavior
    if not SINGLETON:
        SINGLETON = _Peer()

    return SINGLETON