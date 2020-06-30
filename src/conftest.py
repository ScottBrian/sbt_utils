#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 19:54:08 2020

@author: Scott Tuttle
"""

from doctest import OutputChecker
from unittest import mock

import pytest

# import sys


class DateTimeOutputChecker(OutputChecker):
    """ This class is used to intercept the output of the doctest examples
    and change the datetime fields so they match the expected datetimes that
    are documented in the time_hdr.py module examples.
    """
    num_entered = 0

    def check_output(self, want: str, got: str, optionFlags: int) -> bool:
        """
        :param want : the expected output described in the time_hdr module
            example
        :type func_name: str

        :param got : the output collected by doctest when the example is run
        :type func_name: str

        :param optionFlags : provides some customization options - see doctest
            documentation for details
        :type func_name: int

        :returns: True if the example want matches the got, False if not
        :rtype: bool
        """

        new_got = got
        DateTimeOutputChecker.num_entered += 1

        # handle starting case
        if (('Starting' in want)
           and ('Starting' in new_got)):
            DT_idx_want_start = want.find('Starting')
            DT_idx_got_start = new_got.find('Starting')
            DT_idx_want_stop = want.find('*', DT_idx_want_start)
            DT_idx_got_stop = new_got.find('*', DT_idx_got_start)

            new_got = new_got[0:DT_idx_got_start] \
                + want[DT_idx_want_start:DT_idx_want_stop] \
                + new_got[DT_idx_got_stop:]

        # handle ending case
        if (('Ending aFunc' in want)
           and ('Ending aFunc' in new_got)):
            DT_idx_want_start = want.find('Ending aFunc')
            DT_idx_got_start = new_got.find('Ending aFunc')
            DT_idx_want_stop = want.find('*', DT_idx_want_start)
            DT_idx_got_stop = new_got.find('*', DT_idx_got_start)

            new_got = new_got[0:DT_idx_got_start] \
                + want[DT_idx_want_start:DT_idx_want_stop] \
                + new_got[DT_idx_got_stop:]

        # handle elapsed time case
        if (('Elapsed time:' in want)
           and ('Elapsed time:' in new_got)):
            DT_idx_want_start = want.find('Elapsed time:')
            DT_idx_got_start = new_got.find('Elapsed time:')
            DT_idx_want_stop = want.find('*', DT_idx_want_start)
            DT_idx_got_stop = new_got.find('*', DT_idx_got_start)

            new_got = new_got[0:DT_idx_got_start] \
                + want[DT_idx_want_start:DT_idx_want_stop] \
                + new_got[DT_idx_got_stop:]

        # print('DateTimeOutputChecker.num_entered:',
        #       DateTimeOutputChecker.num_entered, file=sys.stderr)
        # print('sbt want:', file=sys.stderr)
        # print(want, file=sys.stderr)
        # print('sbt got:', file=sys.stderr)
        # print(got, file=sys.stderr)
        # print('sbt new_got:', file=sys.stderr)
        # print(new_got, file=sys.stderr)

        return OutputChecker.check_output(self, want, new_got, optionFlags)


@pytest.fixture(autouse=True)
def DateTime_out():
    with mock.patch('doctest.OutputChecker', DateTimeOutputChecker):
        yield
