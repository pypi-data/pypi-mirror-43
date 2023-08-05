#! /usr/bin/env python
"""Tests for the ``edb_interface`` module.

Authors
-------

    - Johannes Sahlmann


Use
---

    These tests can be run via the command line (omit the ``-s`` to
    suppress verbose output to ``stdout``):

    ::

        pytest -s test_edb_interface.py


    All tests will pass locally if a valid MAST token is stored in
    the .netrc file in the local home directory with the following
    format:


        machine mast
            login <username>
            password <token>


"""
import netrc

from astropy.time import Time
from astroquery.mast import Mast
import pytest

from ..edb_interface import mnemonic_inventory, query_single_mnemonic, is_valid_mnemonic


def test_invalid_query():
    """Test that the mnemonic query for an unauthorized user fails."""
    Mast.logout()

    mnemonic_identifier = 'IMIR_HK_ICE_SEC_VOLT4'
    start_time = Time('2019-01-16 00:00:00.000', format='iso')
    end_time = Time('2019-01-16 00:01:00.000', format='iso')
    try:
        query_single_mnemonic(mnemonic_identifier, start_time, end_time, token='1234')
    except RuntimeError:
        pass


def test_is_valid_mnemonic():
    """Test the validation of a mnemonic identifier."""
    assert is_valid_mnemonic('MY_MNEMOMIC') is False
    assert is_valid_mnemonic('SA_ZFGBADCNT') is True


def test_mnemonic_inventory():
    """Test the retrieval of the mnemonic inventory."""
    all_mnemonics = mnemonic_inventory()[0]
    assert len(all_mnemonics) > 1000


@pytest.mark.xfail(raises=(RuntimeError, FileNotFoundError, TypeError))
def test_query_single_mnemonic():
    """Test the query of a mnemonic over a given time range."""
    # get MAST token from the .netrc file in the home directory
    host = 'mast'
    secrets = netrc.netrc()
    mast_token = secrets.authenticators(host)[2]

    mnemonic_identifier = 'SA_ZFGOUTFOV'
    start_time = Time(2018.0, format='decimalyear')
    end_time = Time(2018.1, format='decimalyear')

    data, meta, info = query_single_mnemonic(mnemonic_identifier, start_time, end_time,
                                             token=mast_token)
    assert len(data) == meta['paging']['rows']
