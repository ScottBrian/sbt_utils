#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 15:48:21 2020

@author: Scott Tuttle

"""


from datetime import datetime, timedelta
import pytest
import sys

from typing import Any, Callable, cast

from sbt_utils.time_hdr import StartStopHeader as StartStopHeader
from sbt_utils.time_hdr import time_box as time_box
from sbt_utils.time_hdr import DT_Format as DT_Format

# from sbt_utils.time_hdr import StartStopHeader, time_box, DT_Format

format_list = [('%H:%M'),
               ('%H:%M:%S'),
               ('%m/%d %H:%M:%S'),
               ('%b %d %H:%M:%S'),
               ('%m/%d/%y %H:%M:%S'),
               ('%m/%d/%Y %H:%M:%S'),
               ('%b %d %Y %H:%M:%S'),
               ('%a %b %d %Y %H:%M:%S'),
               ('%a %b %d %H:%M:%S.%f'),
               ('%A %b %d %H:%M:%S.%f'),
               ('%A %B %d %H:%M:%S.%f')]


@pytest.fixture(params=format_list)  # type: ignore
def dt_format(request: Any) -> str:
    """Using different time formats"""
    return cast(str, request.param)


msg_list = ['this is short test msg',
            'this is a much longer test message to test the header']


@pytest.fixture(params=msg_list)  # type: ignore
def a_test_msg(request: Any) -> str:
    """Using different test messages"""
    return cast(str, request.param)


test_num_list = [3, 5]


@pytest.fixture(params=test_num_list)  # type: ignore
def a_test_num(request: Any) -> int:
    """Using different test numbers"""
    return cast(int, request.param)


use_stderr_list = [False, True]


@pytest.fixture(params=use_stderr_list)  # type: ignore
def use_stderr(request: Any) -> bool:
    """False: use sys.stdout, True: use sys.stderr """
    return cast(bool, request.param)


print_end_list = ['\n', '\n\n']


@pytest.fixture(params=print_end_list)  # type: ignore
def print_end(request: Any) -> str:
    """Choose single or double space """
    return cast(str, request.param)


static_TF_list = [False, True]


@pytest.fixture(params=static_TF_list)  # type: ignore
def static_TF(request: Any) -> bool:
    """False: do not wrap with time_box, True: wrap with time_box """
    return cast(bool, request.param)


flush_TF_list = [False, True]


@pytest.fixture(params=flush_TF_list)  # type: ignore
def flush_TF(request: Any) -> bool:
    """False: do not flush print stream, True: flush print stream """
    return cast(bool, request.param)


style_num_list = [1, 2, 3]


@pytest.fixture(params=style_num_list)  # type: ignore
def style_num(request: Any) -> int:
    """Using different time_box styles"""
    return cast(int, request.param)


file_num_list = [0, 1, 2, 3]


@pytest.fixture(params=file_num_list)  # type: ignore
def file_num(request: Any) -> int:
    """Using different file arg"""
    return cast(int, request.param)


class TestStartStopHeader():

    @pytest.fixture(scope='class')  # type: ignore
    def hdr(self) -> "StartStopHeader":
        return StartStopHeader('TestName')

    def test_print_start_msg(self, hdr: "StartStopHeader", capsys: Any,
                             file_num: int,
                             dt_format: DT_Format) -> None:

        if file_num == 0:
            hdr.print_start_msg(dt_format=dt_format,
                                end='\n', flush=False)
            captured = capsys.readouterr().out
        elif file_num == 1:
            hdr.print_start_msg(dt_format=dt_format,
                                file=None,
                                end='\n', flush=False)
            captured = capsys.readouterr().out
        elif file_num == 2:
            hdr.print_start_msg(dt_format=dt_format,
                                end='\n', file=sys.stdout, flush=False)
            captured = capsys.readouterr().out
        else:
            hdr.print_start_msg(dt_format=dt_format,
                                end='\n', file=sys.stderr, flush=False)
            captured = capsys.readouterr().err

        start_DT = hdr.start_DT
        formatted_DT = start_DT.strftime(dt_format)
        msg = '* Starting TestName on ' + formatted_DT + ' *'
        flowers = '*' * len(msg)
        expected = '\n' + flowers + '\n' + msg + '\n' + flowers + '\n'
        assert captured == expected

    def test_print_end_msg(self, hdr: "StartStopHeader", capsys: Any,
                           file_num: int,
                           dt_format: DT_Format) -> None:

        if file_num == 0:
            hdr.print_end_msg(dt_format=dt_format,
                              end='\n', flush=False)
            captured = capsys.readouterr().out
        elif file_num == 1:
            hdr.print_end_msg(dt_format=dt_format,
                              file=None,
                              end='\n', flush=False)
            captured = capsys.readouterr().out
        elif file_num == 2:
            hdr.print_end_msg(dt_format=dt_format,
                              end='\n', file=sys.stdout, flush=False)
            captured = capsys.readouterr().out
        else:
            hdr.print_end_msg(dt_format=dt_format,
                              end='\n', file=sys.stderr, flush=False)
            captured = capsys.readouterr().err

        start_DT = hdr.start_DT
        end_DT = hdr.end_DT
        formatted_delta = str(end_DT - start_DT)
        formatted_DT = end_DT.strftime(dt_format)
        msg1 = '* Ending TestName on ' + formatted_DT
        msg2 = '* Elapsed time: ' + formatted_delta
        flower_len = max(len(msg1), len(msg2)) + 2
        flowers = '*' * flower_len
        msg1 += ' ' * (flower_len - len(msg1) - 1) + '*'
        msg2 += ' ' * (flower_len - len(msg2) - 1) + '*'
        expected = '\n' + flowers + '\n' + msg1 + '\n' + msg2 + '\n' +\
                   flowers + '\n'
        assert captured == expected


class TestTimeBox():

    @staticmethod
    def get_expected_msg(aFunc_msg: str, actual: str,
                         dt_format: DT_Format =
                         DT_Format('%a %b %d %Y %H:%M:%S'),
                         # StartStopHeader.default_dt_format,
                         end: str = '\n',
                         enabled_TF: bool = True) -> str:
        """Helper function to build the expected message to compare
        with the actual message captured with capsys
        """

        if enabled_TF is False:
            if aFunc_msg == '':
                return ''
            else:
                return aFunc_msg + '\n'

        start_DT = datetime.now()
        end_DT = datetime.now() + timedelta(microseconds=42)
        formatted_delta = str(end_DT - start_DT)
        formatted_delta_len = len(formatted_delta)

        # dt_format = '%a %b %d %Y %H:%M:%S'
        formatted_DT = start_DT.strftime(dt_format)
        formatted_DT_len = len(formatted_DT)

        start_time_marks = '#' * formatted_DT_len

        start_time_len = len(start_time_marks)
        end_time_marks = '%' * formatted_DT_len
        end_time_len = len(end_time_marks)
        elapsed_time_marks = '$' * formatted_delta_len
        elapsed_time_len = len(elapsed_time_marks)
        # build expected0
        msg0 = '* Starting aFunc on ' + start_time_marks

        flower_len = len(msg0) + len(' *')
        flowers = '*' * flower_len

        msg0 += ' ' * (flower_len - len(msg0) - 1) + '*'

        expected0 = '\n' + flowers + end + msg0 + end + flowers + end

        # build expected1
        msg1 = '* Ending aFunc on ' + end_time_marks
        msg2 = '* Elapsed time: ' + elapsed_time_marks

        flower_len = max(len(msg1), len(msg2)) + 2
        flowers = '*' * flower_len

        msg1 += ' ' * (flower_len - len(msg1) - 1) + '*'
        msg2 += ' ' * (flower_len - len(msg2) - 1) + '*'

        expected1 = '\n' + flowers + end + msg1 + end + msg2 + end +\
            flowers + end

        if aFunc_msg == '':
            expected = expected0 + expected1
        else:
            expected = expected0 + aFunc_msg + '\n' + expected1

        # find positions of the start, end, and elapsed times
        start_time_index = expected.index(start_time_marks)
        end_time_index = expected.index(end_time_marks)
        elapsed_time_index = expected.index(elapsed_time_marks)

        modified_expected = expected[0:start_time_index] \
            + actual[start_time_index:start_time_index+start_time_len] \
            + expected[start_time_index+start_time_len:end_time_index] \
            + actual[end_time_index:end_time_index+end_time_len] \
            + expected[end_time_index+end_time_len:elapsed_time_index] \
            + actual[elapsed_time_index:elapsed_time_index+elapsed_time_len] \
            + expected[elapsed_time_index+elapsed_time_len:]

        return modified_expected

    def test_call_timebox_with_func_default_args(self) -> None:
        """Basic first test to make sure nothing obvious is wrong"""

        def aFunc(msg: str) -> None:
            print(msg)

        aFunc = time_box(aFunc)
        aFunc_msg = 'this is a default test func for timebox'
        aFunc(aFunc_msg)

    def test_pie_timebox_with_func_default_args(self) -> None:
        """Basic first test to make sure nothing obvious is wrong"""

        @time_box
        def aFunc(msg: str) -> None:
            print(msg)

        aFunc_msg = 'this is a default test func for pie timebox'
        aFunc(aFunc_msg)

    def test_call_timebox_with_func(self, capsys: Any, dt_format: DT_Format,
                                    a_test_msg: str, a_test_num: int,
                                    use_stderr: bool, print_end: str) -> None:
        """This test has variations for aFunc msg and num arguments along
        with variations for the datetime format and print end argument.
        The time_box decorator is called for both stdout and stderr.
        """

        def aFunc(msg: str, num: int) -> int:
            print(msg)
            return num*2 + 1

        if use_stderr:
            aFunc = time_box(aFunc, dt_format=dt_format, file=sys.stderr,
                             end=print_end)
        else:
            aFunc = time_box(aFunc, dt_format=dt_format, file=sys.stdout,
                             end=print_end)

        aFunc_msg = a_test_msg
        actual_return_value = aFunc(aFunc_msg, a_test_num)

        if use_stderr:
            actual = capsys.readouterr().err
            expected = TestTimeBox.get_expected_msg('', actual, dt_format,
                                                    end=print_end)
        else:
            actual = capsys.readouterr().out
            expected = TestTimeBox.get_expected_msg(aFunc_msg, actual,
                                                    dt_format, end=print_end)
        assert actual == expected

        # check that aFunc returns the correct value
        expected_return_value = a_test_num*2 + 1
        message = "Expected return value: {0}, Actual return value: {1}"\
            .format(expected_return_value, actual_return_value)
        assert expected_return_value == actual_return_value, message

    def test_pie_timebox_with_func(self, capsys: Any, dt_format: DT_Format,
                                   a_test_msg: str, a_test_num: int,
                                   use_stderr: bool, print_end: str) -> None:
        """This test has variations for aFunc msg and num arguments along
        with variations for the datetime format and print end argument.
        The time_box decorator uses the pie style for both stdout and stderr.
        """

        if use_stderr:
            file_to_use = sys.stderr
        else:
            file_to_use = sys.stdout

        @time_box(dt_format=dt_format, file=file_to_use, end=print_end)
        def aFunc(msg: str, num: int) -> int:
            print(msg)
            return num*2 + 1

        aFunc_msg = a_test_msg
        actual_return_value = aFunc(aFunc_msg, a_test_num)

        if use_stderr:
            actual = capsys.readouterr().err
            expected = TestTimeBox.get_expected_msg('', actual, dt_format,
                                                    end=print_end)
        else:
            actual = capsys.readouterr().out
            expected = TestTimeBox.get_expected_msg(aFunc_msg, actual,
                                                    dt_format, end=print_end)
        assert actual == expected

        # check that aFunc return the correct value
        expected_return_value = a_test_num*2 + 1
        message = "Expected return value: {0}, Actual return value: {1}"\
            .format(expected_return_value, actual_return_value)
        assert expected_return_value == actual_return_value, message

    def test_pie_timebox_with_static_control(self, capsys: Any,
                                             static_TF: bool,
                                             a_test_msg: str,
                                             a_test_num: int) -> None:

        _tbe = static_TF

        @time_box(time_box_enabled=_tbe, file=sys.stdout)
        def aFunc(msg: str, num: int) -> int:
            print(msg)
            return num*2 + 1

        aFunc_msg = a_test_msg
        actual_return_value = aFunc(aFunc_msg, a_test_num)

        actual = capsys.readouterr().out

        expected = TestTimeBox.get_expected_msg(aFunc_msg,
                                                actual,
                                                enabled_TF=static_TF)

        assert actual == expected

        # check that aFunc return the correct value
        expected_return_value = a_test_num*2 + 1
        message = "Expected return value: {0}, Actual return value: {1}"\
            .format(expected_return_value, actual_return_value)
        assert expected_return_value == actual_return_value, message

    def test_pie_timebox_with_dynamic_control(self, capsys: Any,
                                              static_TF: bool,
                                              a_test_msg: str,
                                              a_test_num: int) -> None:

        _tbe = True
        def tbe() -> bool: return _tbe

        @time_box(time_box_enabled=tbe, file=sys.stdout)
        def aFunc(msg: str, num: int) -> int:
            print(msg)
            return num*2 + 1

        aFunc_msg = a_test_msg

        for TF in [True, False]:
            _tbe = TF
            actual_return_value = aFunc(aFunc_msg, a_test_num)

            actual = capsys.readouterr().out

            expected = TestTimeBox.get_expected_msg(aFunc_msg,
                                                    actual,
                                                    enabled_TF=TF)
            assert actual == expected

            # check that aFunc return the correct value
            expected_return_value = a_test_num*2 + 1
            message = "Expected return value: {0}, Actual return value: {1}"\
                .format(expected_return_value, actual_return_value)
            assert expected_return_value == actual_return_value, message

    """
    The following section tests each combination of arguments to the time_box
    decorator for three styles of decoration (using pie, calling the
    with the function as the first parameter, and calling the decortor with
    the function specified after the call. This test is especially useful to
    ensure that the type hints are working correctly, and that all
    combinations are accepted by python.

    The following keywords with various values and in all combinations are
    tested:
        dt_format - several different datetime formats - see format_list
        end - either '\n' for single space, and '\n\n' for double space
        file - either sys.stdout or sys.stderr
        flush - true/false
        time_box_enabled - true/false

    Each test case is named test_timebox_casexx where xx is 00 to 1F (i.e.,
    in hex). The hex value indicates the combination of keywords that are
    coded on the time_box invocation.
    """

    @staticmethod
    def check_results(capsys: Any,
                      style_num_to_use: int,
                      aFunc: Callable[[int, str], int],
                      case_num: int,
                      dt_format_to_use: DT_Format,
                      print_end_to_use: str,
                      use_stderr_to_use: bool,
                      static_TF_to_use: bool,
                      ) -> None:
        """
        This function invokes the decorated input function and verifies the
        result for each of the 32 test cases following this function
        """

        aFunc_msg = 'The answer is: ' + str(case_num)
        actual_return_value = aFunc(case_num, aFunc_msg)
        if use_stderr_to_use:
            actual = capsys.readouterr().err
            expected = TestTimeBox.get_expected_msg(
                '', actual,
                dt_format_to_use,
                end=print_end_to_use,
                enabled_TF=static_TF_to_use)
        else:
            actual = capsys.readouterr().out
            expected = TestTimeBox.get_expected_msg(
                aFunc_msg, actual,
                dt_format_to_use,
                end=print_end_to_use,
                enabled_TF=static_TF_to_use)

        assert actual == expected

        # check that aFunc returns the correct value
        expected_return_value = case_num * style_num_to_use
        message = "Expected return value: {0}, Actual return value: {1}"\
            .format(expected_return_value, actual_return_value)
        assert expected_return_value == actual_return_value, message

    def test_timebox_case00(self,
                            capsys: Any,
                            style_num: int
                            # dt_format: DT_Format,
                            # print_end: str,
                            # use_stderr: bool,
                            # flush_TF: bool,
                            # static_TF: bool,
                            ) -> None:

        dt_format = StartStopHeader.default_dt_format
        print_end = '\n'
        use_stderr = False
        static_TF = True

        # if use_stderr:
        #     file_to_use = sys.stderr
        # else:
        #     file_to_use = sys.stdout

        if style_num == 1:
            @time_box
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc)
            else:
                aFunc = time_box(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=0,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case01(self,
                            capsys: Any,
                            style_num: int,
                            # dt_format: DT_Format,
                            # print_end: str,
                            # use_stderr: bool,
                            # flush_TF: bool,
                            static_TF: bool,
                            ) -> None:

        dt_format = StartStopHeader.default_dt_format
        print_end = '\n'
        use_stderr = False
        # static_TF = True

        # if use_stderr:
        #     file_to_use = sys.stderr
        # else:
        #     file_to_use = sys.stdout

        if style_num == 1:
            @time_box(time_box_enabled=static_TF)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc, time_box_enabled=static_TF)
            else:
                aFunc = time_box(time_box_enabled=static_TF)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=1,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case02(self,
                            capsys: Any,
                            style_num: int,
                            # dt_format: DT_Format,
                            # print_end: str,
                            # use_stderr: bool,
                            flush_TF: bool,
                            # static_TF: bool,
                            ) -> None:

        dt_format = StartStopHeader.default_dt_format
        print_end = '\n'
        use_stderr = False
        static_TF = True

        # if use_stderr:
        #     file_to_use = sys.stderr
        # else:
        #     file_to_use = sys.stdout

        if style_num == 1:
            @time_box(flush=flush_TF)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc, flush=flush_TF)
            else:
                aFunc = time_box(flush=flush_TF)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=2,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case03(self,
                            capsys: Any,
                            style_num: int,
                            # dt_format: DT_Format,
                            # print_end: str,
                            # use_stderr: bool,
                            flush_TF: bool,
                            static_TF: bool,
                            ) -> None:

        dt_format = StartStopHeader.default_dt_format
        print_end = '\n'
        use_stderr = False
        # static_TF = True

        # if use_stderr:
        #     file_to_use = sys.stderr
        # else:
        #     file_to_use = sys.stdout

        if style_num == 1:
            @time_box(flush=flush_TF, time_box_enabled=static_TF)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc,
                                 flush=flush_TF,
                                 time_box_enabled=static_TF)
            else:
                aFunc = time_box(flush=flush_TF,
                                 time_box_enabled=static_TF)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=3,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case04(self,
                            capsys: Any,
                            style_num: int,
                            # dt_format: DT_Format,
                            # print_end: str,
                            use_stderr: bool,
                            # flush_TF: bool,
                            # static_TF: bool,
                            ) -> None:

        dt_format = StartStopHeader.default_dt_format
        print_end = '\n'
        # use_stderr = False
        static_TF = True

        if use_stderr:
            file_to_use = sys.stderr
        else:
            file_to_use = sys.stdout

        if style_num == 1:
            @time_box(file=file_to_use)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc, file=file_to_use)
            else:
                aFunc = time_box(file=file_to_use)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=4,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case05(self,
                            capsys: Any,
                            style_num: int,
                            # dt_format: DT_Format,
                            # print_end: str,
                            use_stderr: bool,
                            # flush_TF: bool,
                            static_TF: bool,
                            ) -> None:

        dt_format = StartStopHeader.default_dt_format
        print_end = '\n'
        # use_stderr = False
        # static_TF = True

        if use_stderr:
            file_to_use = sys.stderr
        else:
            file_to_use = sys.stdout

        if style_num == 1:
            @time_box(file=file_to_use, time_box_enabled=static_TF)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc,
                                 file=file_to_use,
                                 time_box_enabled=static_TF)
            else:
                aFunc = time_box(file=file_to_use,
                                 time_box_enabled=static_TF)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=5,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case06(self,
                            capsys: Any,
                            style_num: int,
                            # dt_format: DT_Format,
                            # print_end: str,
                            use_stderr: bool,
                            flush_TF: bool,
                            # static_TF: bool,
                            ) -> None:

        dt_format = StartStopHeader.default_dt_format
        print_end = '\n'
        # use_stderr = False
        static_TF = True

        if use_stderr:
            file_to_use = sys.stderr
        else:
            file_to_use = sys.stdout

        if style_num == 1:
            @time_box(file=file_to_use, flush=flush_TF)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc,
                                 file=file_to_use,
                                 flush=flush_TF)
            else:
                aFunc = time_box(file=file_to_use,
                                 flush=flush_TF)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=6,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case07(self,
                            capsys: Any,
                            style_num: int,
                            # dt_format: DT_Format,
                            # print_end: str,
                            use_stderr: bool,
                            flush_TF: bool,
                            static_TF: bool,
                            ) -> None:

        dt_format = StartStopHeader.default_dt_format
        print_end = '\n'
        # use_stderr = False
        # static_TF = True

        if use_stderr:
            file_to_use = sys.stderr
        else:
            file_to_use = sys.stdout

        if style_num == 1:
            @time_box(file=file_to_use,
                      flush=flush_TF,
                      time_box_enabled=static_TF)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc,
                                 file=file_to_use,
                                 flush=flush_TF,
                                 time_box_enabled=static_TF)
            else:
                aFunc = time_box(file=file_to_use,
                                 flush=flush_TF,
                                 time_box_enabled=static_TF)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=7,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case08(self,
                            capsys: Any,
                            style_num: int,
                            # dt_format: DT_Format,
                            print_end: str,
                            # use_stderr: bool,
                            # flush_TF: bool,
                            # static_TF: bool,
                            ) -> None:

        dt_format = StartStopHeader.default_dt_format
        # print_end = '\n'
        use_stderr = False
        static_TF = True

        # if use_stderr:
        #     file_to_use = sys.stderr
        # else:
        #     file_to_use = sys.stdout

        if style_num == 1:
            @time_box(end=print_end)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc, end=print_end)
            else:
                aFunc = time_box(end=print_end)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=8,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case09(self,
                            capsys: Any,
                            style_num: int,
                            # dt_format: DT_Format,
                            print_end: str,
                            # use_stderr: bool,
                            # flush_TF: bool,
                            static_TF: bool,
                            ) -> None:

        dt_format = StartStopHeader.default_dt_format
        # print_end = '\n'
        use_stderr = False
        # static_TF = True

        # if use_stderr:
        #     file_to_use = sys.stderr
        # else:
        #     file_to_use = sys.stdout

        if style_num == 1:
            @time_box(end=print_end, time_box_enabled=static_TF)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc,
                                 end=print_end,
                                 time_box_enabled=static_TF)
            else:
                aFunc = time_box(end=print_end,
                                 time_box_enabled=static_TF)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=9,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case0A(self,
                            capsys: Any,
                            style_num: int,
                            # dt_format: DT_Format,
                            print_end: str,
                            # use_stderr: bool,
                            flush_TF: bool,
                            # static_TF: bool,
                            ) -> None:

        dt_format = StartStopHeader.default_dt_format
        # print_end = '\n'
        use_stderr = False
        static_TF = True

        # if use_stderr:
        #     file_to_use = sys.stderr
        # else:
        #     file_to_use = sys.stdout

        if style_num == 1:
            @time_box(end=print_end, flush=flush_TF)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc, end=print_end, flush=flush_TF)
            else:
                aFunc = time_box(end=print_end, flush=flush_TF)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=10,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case0B(self,
                            capsys: Any,
                            style_num: int,
                            # dt_format: DT_Format,
                            print_end: str,
                            # use_stderr: bool,
                            flush_TF: bool,
                            static_TF: bool,
                            ) -> None:

        dt_format = StartStopHeader.default_dt_format
        # print_end = '\n'
        use_stderr = False
        # static_TF = True

        # if use_stderr:
        #     file_to_use = sys.stderr
        # else:
        #     file_to_use = sys.stdout

        if style_num == 1:
            @time_box(end=print_end, flush=flush_TF,
                      time_box_enabled=static_TF)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc,
                                 end=print_end,
                                 flush=flush_TF,
                                 time_box_enabled=static_TF)
            else:
                aFunc = time_box(end=print_end,
                                 flush=flush_TF,
                                 time_box_enabled=static_TF)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=11,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case0C(self,
                            capsys: Any,
                            style_num: int,
                            # dt_format: DT_Format,
                            print_end: str,
                            use_stderr: bool,
                            # flush_TF: bool,
                            # static_TF: bool,
                            ) -> None:

        dt_format = StartStopHeader.default_dt_format
        # print_end = '\n'
        # use_stderr = False
        static_TF = True

        if use_stderr:
            file_to_use = sys.stderr
        else:
            file_to_use = sys.stdout

        if style_num == 1:
            @time_box(end=print_end, file=file_to_use)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc, end=print_end, file=file_to_use)
            else:
                aFunc = time_box(end=print_end, file=file_to_use)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=12,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case0D(self,
                            capsys: Any,
                            style_num: int,
                            # dt_format: DT_Format,
                            print_end: str,
                            use_stderr: bool,
                            # flush_TF: bool,
                            static_TF: bool,
                            ) -> None:

        dt_format = StartStopHeader.default_dt_format
        # print_end = '\n'
        # use_stderr = False
        # static_TF = True

        if use_stderr:
            file_to_use = sys.stderr
        else:
            file_to_use = sys.stdout

        if style_num == 1:
            @time_box(end=print_end, file=file_to_use,
                      time_box_enabled=static_TF)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc,
                                 end=print_end,
                                 file=file_to_use,
                                 time_box_enabled=static_TF)
            else:
                aFunc = time_box(end=print_end,
                                 file=file_to_use,
                                 time_box_enabled=static_TF)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=13,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case0E(self,
                            capsys: Any,
                            style_num: int,
                            # dt_format: DT_Format,
                            print_end: str,
                            use_stderr: bool,
                            flush_TF: bool,
                            # static_TF: bool,
                            ) -> None:

        dt_format = StartStopHeader.default_dt_format
        # print_end = '\n'
        # use_stderr = False
        static_TF = True

        if use_stderr:
            file_to_use = sys.stderr
        else:
            file_to_use = sys.stdout

        if style_num == 1:
            @time_box(end=print_end, file=file_to_use,
                      flush=flush_TF)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc,
                                 end=print_end,
                                 file=file_to_use,
                                 flush=flush_TF)
            else:
                aFunc = time_box(end=print_end,
                                 file=file_to_use,
                                 flush=flush_TF)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=14,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case0F(self,
                            capsys: Any,
                            style_num: int,
                            # dt_format: DT_Format,
                            print_end: str,
                            use_stderr: bool,
                            flush_TF: bool,
                            static_TF: bool,
                            ) -> None:

        dt_format = StartStopHeader.default_dt_format
        # print_end = '\n'
        # use_stderr = False
        # static_TF = True

        if use_stderr:
            file_to_use = sys.stderr
        else:
            file_to_use = sys.stdout

        if style_num == 1:
            @time_box(end=print_end, file=file_to_use,
                      flush=flush_TF, time_box_enabled=static_TF)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc,
                                 end=print_end,
                                 file=file_to_use,
                                 flush=flush_TF,
                                 time_box_enabled=static_TF)
            else:
                aFunc = time_box(end=print_end,
                                 file=file_to_use,
                                 flush=flush_TF,
                                 time_box_enabled=static_TF)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=15,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case10(self,
                            capsys: Any,
                            style_num: int,
                            dt_format: DT_Format,
                            # print_end: str,
                            # use_stderr: bool,
                            # flush_TF: bool,
                            # static_TF: bool,
                            ) -> None:

        # dt_format = StartStopHeader.default_dt_format
        print_end = '\n'
        use_stderr = False
        static_TF = True

        # if use_stderr:
        #     file_to_use = sys.stderr
        # else:
        #     file_to_use = sys.stdout

        if style_num == 1:
            @time_box(dt_format=dt_format)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc, dt_format=dt_format)
            else:
                aFunc = time_box(dt_format=dt_format)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=16,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case11(self,
                            capsys: Any,
                            style_num: int,
                            dt_format: DT_Format,
                            # print_end: str,
                            # use_stderr: bool,
                            # flush_TF: bool,
                            static_TF: bool,
                            ) -> None:

        # dt_format = StartStopHeader.default_dt_format
        print_end = '\n'
        use_stderr = False
        # static_TF = True

        # if use_stderr:
        #     file_to_use = sys.stderr
        # else:
        #     file_to_use = sys.stdout

        if style_num == 1:
            @time_box(dt_format=dt_format, time_box_enabled=static_TF)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc, dt_format=dt_format,
                                 time_box_enabled=static_TF)
            else:
                aFunc = time_box(dt_format=dt_format,
                                 time_box_enabled=static_TF)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=17,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case12(self,
                            capsys: Any,
                            style_num: int,
                            dt_format: DT_Format,
                            # print_end: str,
                            # use_stderr: bool,
                            flush_TF: bool,
                            # static_TF: bool,
                            ) -> None:

        # dt_format = StartStopHeader.default_dt_format
        print_end = '\n'
        use_stderr = False
        static_TF = True

        # if use_stderr:
        #     file_to_use = sys.stderr
        # else:
        #     file_to_use = sys.stdout

        if style_num == 1:
            @time_box(dt_format=dt_format, flush=flush_TF)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc, dt_format=dt_format, flush=flush_TF)
            else:
                aFunc = time_box(dt_format=dt_format, flush=flush_TF)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=18,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case13(self,
                            capsys: Any,
                            style_num: int,
                            dt_format: DT_Format,
                            # print_end: str,
                            # use_stderr: bool,
                            flush_TF: bool,
                            static_TF: bool,
                            ) -> None:

        # dt_format = StartStopHeader.default_dt_format
        print_end = '\n'
        use_stderr = False
        # static_TF = True

        # if use_stderr:
        #     file_to_use = sys.stderr
        # else:
        #     file_to_use = sys.stdout

        if style_num == 1:
            @time_box(dt_format=dt_format, flush=flush_TF,
                      time_box_enabled=static_TF)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc,
                                 dt_format=dt_format,
                                 flush=flush_TF,
                                 time_box_enabled=static_TF)
            else:
                aFunc = time_box(dt_format=dt_format,
                                 flush=flush_TF,
                                 time_box_enabled=static_TF)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=19,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case14(self,
                            capsys: Any,
                            style_num: int,
                            dt_format: DT_Format,
                            # print_end: str,
                            use_stderr: bool,
                            # flush_TF: bool,
                            # static_TF: bool,
                            ) -> None:

        # dt_format = StartStopHeader.default_dt_format
        print_end = '\n'
        # use_stderr = False
        static_TF = True

        if use_stderr:
            file_to_use = sys.stderr
        else:
            file_to_use = sys.stdout

        if style_num == 1:
            @time_box(dt_format=dt_format, file=file_to_use)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc, dt_format=dt_format, file=file_to_use)
            else:
                aFunc = time_box(dt_format=dt_format, file=file_to_use)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=20,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case15(self,
                            capsys: Any,
                            style_num: int,
                            dt_format: DT_Format,
                            # print_end: str,
                            use_stderr: bool,
                            # flush_TF: bool,
                            static_TF: bool,
                            ) -> None:

        # dt_format = StartStopHeader.default_dt_format
        print_end = '\n'
        # use_stderr = False
        # static_TF = True

        if use_stderr:
            file_to_use = sys.stderr
        else:
            file_to_use = sys.stdout

        if style_num == 1:
            @time_box(dt_format=dt_format, file=file_to_use,
                      time_box_enabled=static_TF)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc,
                                 dt_format=dt_format,
                                 file=file_to_use,
                                 time_box_enabled=static_TF)
            else:
                aFunc = time_box(dt_format=dt_format,
                                 file=file_to_use,
                                 time_box_enabled=static_TF)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=21,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case16(self,
                            capsys: Any,
                            style_num: int,
                            dt_format: DT_Format,
                            # print_end: str,
                            use_stderr: bool,
                            flush_TF: bool,
                            # static_TF: bool,
                            ) -> None:

        # dt_format = StartStopHeader.default_dt_format
        print_end = '\n'
        # use_stderr = False
        static_TF = True

        if use_stderr:
            file_to_use = sys.stderr
        else:
            file_to_use = sys.stdout

        if style_num == 1:
            @time_box(dt_format=dt_format, file=file_to_use, flush=flush_TF)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc,
                                 dt_format=dt_format,
                                 file=file_to_use,
                                 flush=flush_TF)
            else:
                aFunc = time_box(dt_format=dt_format,
                                 file=file_to_use,
                                 flush=flush_TF)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=22,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case17(self,
                            capsys: Any,
                            style_num: int,
                            dt_format: DT_Format,
                            # print_end: str,
                            use_stderr: bool,
                            flush_TF: bool,
                            static_TF: bool,
                            ) -> None:

        # dt_format = StartStopHeader.default_dt_format
        print_end = '\n'
        # use_stderr = False
        # static_TF = True

        if use_stderr:
            file_to_use = sys.stderr
        else:
            file_to_use = sys.stdout

        if style_num == 1:
            @time_box(dt_format=dt_format, file=file_to_use,
                      flush=flush_TF,
                      time_box_enabled=static_TF)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc,
                                 dt_format=dt_format,
                                 file=file_to_use,
                                 flush=flush_TF,
                                 time_box_enabled=static_TF)
            else:
                aFunc = time_box(dt_format=dt_format,
                                 file=file_to_use,
                                 flush=flush_TF,
                                 time_box_enabled=static_TF)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=23,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case18(self,
                            capsys: Any,
                            style_num: int,
                            dt_format: DT_Format,
                            print_end: str,
                            # use_stderr: bool,
                            # flush_TF: bool,
                            # static_TF: bool,
                            ) -> None:

        # dt_format = StartStopHeader.default_dt_format
        # print_end = '\n'
        use_stderr = False
        static_TF = True

        # if use_stderr:
        #     file_to_use = sys.stderr
        # else:
        #     file_to_use = sys.stdout

        if style_num == 1:
            @time_box(dt_format=dt_format, end=print_end)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc, dt_format=dt_format, end=print_end)
            else:
                aFunc = time_box(dt_format=dt_format, end=print_end)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=24,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case19(self,
                            capsys: Any,
                            style_num: int,
                            dt_format: DT_Format,
                            print_end: str,
                            # use_stderr: bool,
                            # flush_TF: bool,
                            static_TF: bool,
                            ) -> None:

        # dt_format = StartStopHeader.default_dt_format
        # print_end = '\n'
        use_stderr = False
        # static_TF = True

        # if use_stderr:
        #     file_to_use = sys.stderr
        # else:
        #     file_to_use = sys.stdout

        if style_num == 1:
            @time_box(dt_format=dt_format, end=print_end,
                      time_box_enabled=static_TF)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc,
                                 dt_format=dt_format,
                                 end=print_end,
                                 time_box_enabled=static_TF)
            else:
                aFunc = time_box(dt_format=dt_format,
                                 end=print_end,
                                 time_box_enabled=static_TF)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=25,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case1A(self,
                            capsys: Any,
                            style_num: int,
                            dt_format: DT_Format,
                            print_end: str,
                            # use_stderr: bool,
                            flush_TF: bool,
                            # static_TF: bool,
                            ) -> None:

        # dt_format = StartStopHeader.default_dt_format
        # print_end = '\n'
        use_stderr = False
        static_TF = True

        # if use_stderr:
        #     file_to_use = sys.stderr
        # else:
        #     file_to_use = sys.stdout

        if style_num == 1:
            @time_box(dt_format=dt_format, end=print_end, flush=flush_TF)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc, dt_format=dt_format,
                                 end=print_end, flush=flush_TF)
            else:
                aFunc = time_box(dt_format=dt_format,
                                 end=print_end, flush=flush_TF)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=26,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case1B(self,
                            capsys: Any,
                            style_num: int,
                            dt_format: DT_Format,
                            print_end: str,
                            # use_stderr: bool,
                            flush_TF: bool,
                            static_TF: bool,
                            ) -> None:

        # dt_format = StartStopHeader.default_dt_format
        # print_end = '\n'
        use_stderr = False
        # static_TF = True

        # if use_stderr:
        #     file_to_use = sys.stderr
        # else:
        #     file_to_use = sys.stdout

        if style_num == 1:
            @time_box(dt_format=dt_format, end=print_end, flush=flush_TF,
                      time_box_enabled=static_TF)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc,
                                 dt_format=dt_format,
                                 end=print_end,
                                 flush=flush_TF,
                                 time_box_enabled=static_TF)
            else:
                aFunc = time_box(dt_format=dt_format,
                                 end=print_end,
                                 flush=flush_TF,
                                 time_box_enabled=static_TF)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=27,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case1C(self,
                            capsys: Any,
                            style_num: int,
                            dt_format: DT_Format,
                            print_end: str,
                            use_stderr: bool,
                            # flush_TF: bool,
                            # static_TF: bool,
                            ) -> None:

        # dt_format = StartStopHeader.default_dt_format
        # print_end = '\n'
        # use_stderr = False
        static_TF = True

        if use_stderr:
            file_to_use = sys.stderr
        else:
            file_to_use = sys.stdout

        if style_num == 1:
            @time_box(dt_format=dt_format, end=print_end, file=file_to_use)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc, dt_format=dt_format,
                                 end=print_end, file=file_to_use)
            else:
                aFunc = time_box(dt_format=dt_format,
                                 end=print_end, file=file_to_use)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=28,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case1D(self,
                            capsys: Any,
                            style_num: int,
                            dt_format: DT_Format,
                            print_end: str,
                            use_stderr: bool,
                            # flush_TF: bool,
                            static_TF: bool,
                            ) -> None:

        # dt_format = StartStopHeader.default_dt_format
        # print_end = '\n'
        # use_stderr = False
        # static_TF = True

        if use_stderr:
            file_to_use = sys.stderr
        else:
            file_to_use = sys.stdout

        if style_num == 1:
            @time_box(dt_format=dt_format, end=print_end, file=file_to_use,
                      time_box_enabled=static_TF)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc,
                                 dt_format=dt_format,
                                 end=print_end,
                                 file=file_to_use,
                                 time_box_enabled=static_TF)
            else:
                aFunc = time_box(dt_format=dt_format,
                                 end=print_end,
                                 file=file_to_use,
                                 time_box_enabled=static_TF)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=29,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case1E(self,
                            capsys: Any,
                            style_num: int,
                            dt_format: DT_Format,
                            print_end: str,
                            use_stderr: bool,
                            flush_TF: bool,
                            # static_TF: bool,
                            ) -> None:

        # dt_format = StartStopHeader.default_dt_format
        # print_end = '\n'
        # use_stderr = False
        static_TF = True

        if use_stderr:
            file_to_use = sys.stderr
        else:
            file_to_use = sys.stdout

        if style_num == 1:
            @time_box(dt_format=dt_format, end=print_end, file=file_to_use,
                      flush=flush_TF)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc,
                                 dt_format=dt_format,
                                 end=print_end,
                                 file=file_to_use,
                                 flush=flush_TF)
            else:
                aFunc = time_box(dt_format=dt_format,
                                 end=print_end,
                                 file=file_to_use,
                                 flush=flush_TF)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=30,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)

    def test_timebox_case1F(self,
                            capsys: Any,
                            style_num: int,
                            dt_format: DT_Format,
                            print_end: str,
                            use_stderr: bool,
                            flush_TF: bool,
                            static_TF: bool,
                            ) -> None:

        # dt_format = StartStopHeader.default_dt_format
        # print_end = '\n'
        # use_stderr = False
        # static_TF = True

        if use_stderr:
            file_to_use = sys.stderr
        else:
            file_to_use = sys.stdout

        if style_num == 1:
            @time_box(dt_format=dt_format, end=print_end, file=file_to_use,
                      flush=flush_TF, time_box_enabled=static_TF)
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
        else:
            def aFunc(num: int, msg: str) -> int:
                print(msg)
                return num * style_num
            if style_num == 2:
                aFunc = time_box(aFunc,
                                 dt_format=dt_format,
                                 end=print_end,
                                 file=file_to_use,
                                 flush=flush_TF,
                                 time_box_enabled=static_TF)
            else:
                aFunc = time_box(dt_format=dt_format,
                                 end=print_end,
                                 file=file_to_use,
                                 flush=flush_TF,
                                 time_box_enabled=static_TF)(aFunc)

        TestTimeBox.check_results(capsys=capsys,
                                  style_num_to_use=style_num,
                                  aFunc=aFunc,
                                  case_num=31,
                                  dt_format_to_use=dt_format,
                                  print_end_to_use=print_end,
                                  use_stderr_to_use=use_stderr,
                                  static_TF_to_use=static_TF)


class TestTimeBoxDocstrings():
    def test_timebox_with_example_1(self) -> None:
        print('#' * 50)
        print('Example for StartStopHeader:')
        print()
        from sbt_utils.time_hdr import StartStopHeader
        import time
        import sys

        def aFunc1() -> None:
            print('2 + 2 =', 2+2)
            time.sleep(2)

        hdr = StartStopHeader('aFunc1')
        hdr.print_start_msg(file=sys.stdout)

        aFunc1()

        hdr.print_end_msg(file=sys.stdout)

    def test_timebox_with_example_2(self) -> None:
        print('#' * 50)
        print('Example for time_box decorator:')
        print()
        from sbt_utils.time_hdr import time_box
        import time
        import sys

        @time_box(file=sys.stdout)
        def aFunc2() -> None:
            print('2 * 3 =', 2*3)
            time.sleep(1)

        aFunc2()

    def test_timebox_with_example_3(self) -> None:
        print('#' * 50)
        print('Example of printing to stderr:')
        print()
        from sbt_utils.time_hdr import time_box
        import sys

        @time_box(file=sys.stderr)
        def aFunc3() -> None:
            print('this text printed to stdout, not stderr')

        aFunc3()

    def test_timebox_with_example_4(self) -> None:
        print('#' * 50)
        print('Example of statically wrapping function with time_box:')
        print()

        from sbt_utils.time_hdr import time_box
        import sys

        _tbe = False

        @time_box(time_box_enabled=_tbe, file=sys.stdout)
        def aFunc4a() -> None:
            print('this is sample text for _tbe = False static example')

        aFunc4a()  # aFunc4a is not wrapped by time box

        _tbe = True

        @time_box(time_box_enabled=_tbe, file=sys.stdout)
        def aFunc4b() -> None:
            print('this is sample text for _tbe = True static example')

        aFunc4b()  # aFunc4b is wrapped by time box

    def test_timebox_with_example_5(self) -> None:
        print('#' * 50)
        print('Example of dynamically wrapping function with time_box:')
        print()

        from sbt_utils.time_hdr import time_box
        import sys

        _tbe = True
        def tbe() -> bool: return _tbe

        @time_box(time_box_enabled=tbe, file=sys.stdout)
        def aFunc5() -> None:
            print('this is sample text for the tbe dynamic example')

        aFunc5()  # aFunc5 is wrapped by time box

        _tbe = False
        aFunc5()  # aFunc5 is not wrapped by time_box

    def test_timebox_with_example_6(self) -> None:
        print('#' * 50)
        print('Example of using different datetime format:')
        print()

        from sbt_utils.time_hdr import time_box

        aDatetime_format: DT_Format = cast(DT_Format, '%m/%d/%y %H:%M:%S')

        @time_box(dt_format=aDatetime_format)
        def aFunc6() -> None:
            print('this is sample text for the datetime format example')

        aFunc6()
