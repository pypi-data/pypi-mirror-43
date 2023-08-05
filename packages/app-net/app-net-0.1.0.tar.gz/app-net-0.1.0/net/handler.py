# -*- coding: utf-8 -*-

# python 2/3 imports
from .imports import socketserver


HANDLERS = {}


class PeerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        pass


def handler(func, *args, **kwargs):
    """
    Register a function as a handler for the peer server.
    """
    print(func.__name__)

    def wrapper():
        return func(*args, **kwargs)

    return wrapper