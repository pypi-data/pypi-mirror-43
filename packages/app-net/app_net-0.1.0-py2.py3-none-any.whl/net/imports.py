# -*- coding: utf-8 -*-
"""
python 2/3 imports handled here
"""

# python version handling
try:
    # python 2

    # noinspection SpellCheckingInspection
    import SocketServer as socketserver

    # noinspection PyShadowingBuiltins
    from socket import error as ConnectionRefusedError

except ImportError:

    # python 3
    import socketserver

    # noinspection PyShadowingBuiltins
    ConnectionRefusedError = ConnectionRefusedError