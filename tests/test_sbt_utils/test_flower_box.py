#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 23:49:49 2020

@author: Scott Tuttle
"""

import pytest
import sys


from sbt_utils.flower_box import print_flower_box_msg as print_flower_box_msg
from typing import Any, cast, List

file_num_list = [0, 1, 2, 3]


@pytest.fixture(params=file_num_list)  # type: ignore
def file_num(request: Any) -> int:
    """Using different file arg"""
    return cast(int, request.param)


class TestFlowerBox():
    # build case list for tests
    # first tuple item is the msg or msg list passed on the flower box call
    # second tuple item is the expected result capured in sysout
    # note: first few single messages are passed first as single strings, and
    # then as single item lists
    case_list = [('', '\n'
                      '****\n'
                      '*  *\n'
                      '****\n'
                  ),
                 ('A', '\n'
                       '*****\n'
                       '* A *\n'
                       '*****\n'
                  ),
                 ('AB', '\n'
                        '******\n'
                        '* AB *\n'
                        '******\n'
                  ),
                 ('A B', '\n'
                         '*******\n'
                         '* A B *\n'
                         '*******\n'
                  ),
                 ('AB CD', '\n'
                           '*********\n'
                           '* AB CD *\n'
                           '*********\n'
                  ),
                 ('ABC DEF GHI', '\n'
                                 '***************\n'
                                 '* ABC DEF GHI *\n'
                                 '***************\n'
                  ),
                 ('A BC DEF', '\n'
                              '************\n'
                              '* A BC DEF *\n'
                              '************\n'
                  ),
                 ([''], '\n'
                        '****\n'
                        '*  *\n'
                        '****\n'
                  ),
                 (['A'], '\n'
                         '*****\n'
                         '* A *\n'
                         '*****\n'
                  ),
                 (['AB'], '\n'
                          '******\n'
                          '* AB *\n'
                          '******\n'
                  ),
                 (['A B'], '\n'
                           '*******\n'
                           '* A B *\n'
                           '*******\n'
                  ),
                 (['AB CD'], '\n'
                             '*********\n'
                             '* AB CD *\n'
                             '*********\n'
                  ),
                 (['ABC DEF GHI'], '\n'
                                   '***************\n'
                                   '* ABC DEF GHI *\n'
                                   '***************\n'
                  ),
                 (['A BC DEF'], '\n'
                                '************\n'
                                '* A BC DEF *\n'
                                '************\n'
                  ),
                 (['', ''], '\n'
                            '****\n'
                            '*  *\n'
                            '*  *\n'
                            '****\n'
                  ),
                 (['A', 'B'], '\n'
                              '*****\n'
                              '* A *\n'
                              '* B *\n'
                              '*****\n'
                  ),
                 (['AB', 'CD'], '\n'
                                '******\n'
                                '* AB *\n'
                                '* CD *\n'
                                '******\n'
                  ),
                 (['A B', 'C D'], '\n'
                                  '*******\n'
                                  '* A B *\n'
                                  '* C D *\n'
                                  '*******\n'
                  ),
                 (['AB CD', 'EF GH'], '\n'
                                      '*********\n'
                                      '* AB CD *\n'
                                      '* EF GH *\n'
                                      '*********\n'
                  ),
                 (['ABC DEF GHI', 'JKL MNO PQR'], '\n'
                                                  '***************\n'
                                                  '* ABC DEF GHI *\n'
                                                  '* JKL MNO PQR *\n'
                                                  '***************\n'
                  ),
                 (['A BC DEF', 'a bc def'], '\n'
                                            '************\n'
                                            '* A BC DEF *\n'
                                            '* a bc def *\n'
                                            '************\n'
                  ),
                 (['', 'B'], '\n'
                             '*****\n'
                             '*   *\n'
                             '* B *\n'
                             '*****\n'
                  ),
                 (['A', ''], '\n'
                             '*****\n'
                             '* A *\n'
                             '*   *\n'
                             '*****\n'
                  ),
                 (['', 'AB'], '\n'
                              '******\n'
                              '*    *\n'
                              '* AB *\n'
                              '******\n'
                  ),
                 (['AB', ''], '\n'
                              '******\n'
                              '* AB *\n'
                              '*    *\n'
                              '******\n'
                  ),
                 (['AB', ' CDEF HIJ', 'One long line to test'],
                  '\n'
                  '*************************\n'
                  '* AB                    *\n'
                  '*  CDEF HIJ             *\n'
                  '* One long line to test *\n'
                  '*************************\n'
                  )]

    @pytest.mark.parametrize('msg_list, expected_result',  # type: ignore
                             case_list)
    def test_flower_box(self, capsys: Any, msg_list: List[str],
                        expected_result: str,
                        file_num: int) -> None:
        if file_num == 0:
            print_flower_box_msg(msg_list)
            captured = capsys.readouterr().out
        elif file_num == 1:
            print_flower_box_msg(msg_list, file=None)
            captured = capsys.readouterr().out
        elif file_num == 2:
            print_flower_box_msg(msg_list, file=sys.stdout)
            captured = capsys.readouterr().out
        else:
            print_flower_box_msg(msg_list, file=sys.stderr)
            captured = capsys.readouterr().err

        assert captured == expected_result
