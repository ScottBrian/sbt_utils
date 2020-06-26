#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 23:30:55 2020

@author: Scott Tuttle

The flower_box module contains one item:
1) a print_flower_box_msg function which takes one of more lines of text as
   input and prints the line or lines inside a flower box (asterisks) as a
   visual aid in finding the text on the console or in a log.

Examples for print_flower_box_msg:
example 1: print a single line message in a flower box

>>> from sbt_utils.flower_box import print_flower_box_msg
>>> import sys
>>> msg_list = ['This is my test message']
>>> print_flower_box_msg(msg_list, file=sys.stdout)
<BLANKLINE>
***************************
* This is my test message *
***************************

example 2: print a two line message in a flower box

>>> from sbt_utils.flower_box import print_flower_box_msg
>>> import sys
>>> msg_list = ['This is my first line test message', '   and my second line']
>>> print_flower_box_msg(msg_list, file=sys.stdout)
<BLANKLINE>
**************************************
* This is my first line test message *
*    and my second line              *
**************************************

"""

import sys
from typing import Any, List, Union


def print_flower_box_msg(msgs: Union[str, List[str]], end: str = '\n',
                         file: Any = sys.stdout, flush: bool = False) -> None:
    """Print a single or multi-line message inside  flower box (asterisks).

    :param msgs : single message or list of messages to print

    :param end : end specification to use on the print call

    :param file : file specification to use on the print call

    :param flush : flush specification to use on the print call

    :returns: None
    """
    if isinstance(msgs, str):  # single messsage
        msgs = [msgs]  # cconvert to list

    max_msglen: int = len(max(msgs, key=len)) + 4  # 4 for front/end asterisks

    # ensure a new line so that our flower box is properly aligned
    print('', file=file)

    print('*' * max_msglen, end=end, file=file, flush=flush)
    for msg in msgs:
        msg = '* ' + msg + ' ' * (max_msglen - len(msg) - 4) + ' *'
        print(msg, end=end, file=file, flush=flush)
    print('*' * max_msglen, end=end, file=file, flush=flush)
