#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
# Created on Mon Mar 16 23:30:55 2020
#
# @author: Scott Tuttle
# =============================================================================

"""
==========
flower_box
==========

The flower_box module contains:

:function print_flower_box_msg: prints one or more lines of text in a flower
    box (i.e., surrounded by asterisks).

:Example: print a one line message in a flower box

>>> from sbt_utils.flower_box import print_flower_box_msg

>>> msg = 'This is my test message'
>>> print_flower_box_msg(msg)
<BLANKLINE>
***************************
* This is my test message *
***************************

"""

import sys
from typing import Any, List, Optional, Union


def print_flower_box_msg(msgs: Union[str, List[str]], *,
                         end: str = '\n',
                         file: Optional[Any] = None,
                         flush: bool = False) -> None:
    """Print a single or multi-line message inside a flower box (asterisks).

:param msgs: single message or list of messages to print
:type msgs: str

:param end: Specifies the argument to use on the print statement *end*
    parameter. The default is \'\\\\n'.
:type end: str, optional

:param file: Specifies the argument to use on the print statement
    *file* parameter. The default is
    sys.stdout (via None).
:type file: Optional[Any]

:param flush: Specifies the argument to use on the print statement
    *flush* parameterfor. The default is False.
:type flush: bool, optional

:returns: None
:rtype: None

:Example: print a two line message in a flower box

>>> from sbt_utils.flower_box import print_flower_box_msg

>>> msg_list = ['This is my first line test message', '   and my second line']
>>> print_flower_box_msg(msg_list)
<BLANKLINE>
**************************************
* This is my first line test message *
*    and my second line              *
**************************************

    """

# =============================================================================
#     Note: the following code that sets file to sys.stdout is needed to allow
#     the test cases to use the pytest capsys built-in fixture. Having
#     sys.stdout as the default parameter in the function definition does
#     not work because capsys changes sys.stdout after the test case gets
#     control, meaning the print statements in StartStopHeader code are not
#     captured. This is also appears to be the case for doctest.
#     So, we simply use None as the default and set file to sys.stdout here
#     which works fine.
# =============================================================================

    if file is None:
        file = sys.stdout

    if isinstance(msgs, str):  # single messsage
        msgs = [msgs]  # convert to list

    max_msglen: int = len(max(msgs, key=len)) + 4  # 4 for front/end asterisks

    # ensure a new line so that our flower box is properly aligned
    print('', file=file)

    print('*' * max_msglen, end=end, file=file, flush=flush)
    for msg in msgs:
        msg = '* ' + msg + ' ' * (max_msglen - len(msg) - 4) + ' *'
        print(msg, end=end, file=file, flush=flush)
    print('*' * max_msglen, end=end, file=file, flush=flush)
