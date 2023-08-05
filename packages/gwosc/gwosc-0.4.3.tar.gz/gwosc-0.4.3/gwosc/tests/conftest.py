# -*- coding: utf-8 -*-
# Copyright Duncan Macleod 2018
#
# This file is part of GWOSC.
#
# GWOSC is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# GWOSC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GWOSC.  If not, see <http://www.gnu.org/licenses/>.

"""Helpers for tests
"""

import os
try:
    from unittest import mock
except ImportError:  # python < 3
    import mock

import pytest

from ..api import fetch_catalog_event_json

__author__ = 'Duncan Macleod <duncan.macleod@ligo.org>'

# unset these variables to allow the tests to run with pybuild
os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)

try:
    autouseyield = pytest.yield_fixture(autouse=True)
except AttributeError:  # pytest > 3.0.0
    autouseyield = pytest.fixture(autouse=True)


# force all tests to not rely on the catalog cache
@autouseyield
def clear_catalog_cache():
    with mock.patch.dict("gwosc.catalog.CACHE", clear=True):
        yield


def _event_urls(name):
    return fetch_catalog_event_json(name)['strain']


@pytest.fixture
def gw150914_urls(scope='module'):
    return _event_urls('GW150914')


@pytest.fixture
def gw170817_urls(scope='module'):
    return _event_urls('GW170817')
