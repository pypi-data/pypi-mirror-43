#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `net` package."""

import pytest

import net


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_peer_construct():
    """
    Construct and connect a peer server.
    """
    master = net.Peer()
    slave = master.__class__(test=True)

    print(slave.ping(master.port, master.host))
    print(master.ping(slave.port, slave.host))

test_peer_construct()
