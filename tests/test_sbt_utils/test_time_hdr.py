#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 15:48:21 2020

@author: Scott Tuttle

"""


from datetime import datetime, timedelta
import pytest
import sys

from typing import Any, Callable, cast, Tuple, Union

from sbt_utils.time_hdr import StartStopHeader as StartStopHeader
from sbt_utils.time_hdr import time_box as time_box
from sbt_utils.time_hdr import DT_Format as DT_Format

_ = sys.stdout

dt_format_arg_list = ['0',
                      ('%H:%M'),
                      ('%H:%M:%S'),
                      ('%m/%d %H:%M:%S'),
                      ('%b %d %H:%M:%S'),
                      ('%m/%d/%y %H:%M:%S'),
                      ('%m/%d/%Y %H:%M:%S'),
                      ('%b %d %Y %H:%M:%S'),
                      ('%a %b %d %Y %H:%M:%S'),
                      ('%a %b %d %H:%M:%S.%f'),
                      ('%A %b %d %H:%M:%S.%f'),
                      ('%A %B %d %H:%M:%S.%f')
                      ]


@pytest.fixture(params=dt_format_arg_list)  # type: ignore
def dt_format_arg(request: Any) -> str:
    """Using different time formats"""
    return cast(str, request.param)


style_num_list = [1, 2, 3]


@pytest.fixture(params=style_num_list)  # type: ignore
def style_num(request: Any) -> int:
    """Using different time_box styles"""
    return cast(int, request.param)


end_arg_list = ['0', '\n', '\n\n']


@pytest.fixture(params=end_arg_list)  # type: ignore
def end_arg(request: Any) -> str:
    """Choose single or double space """
    return cast(str, request.param)


file_arg_list = ['0', 'None', 'sys.stdout', 'sys.stderr']


@pytest.fixture(params=file_arg_list)  # type: ignore
def file_arg(request: Any) -> str:
    """Using different file arg"""
    return cast(str, request.param)


flush_arg_list = ['0', 'True', 'False']


@pytest.fixture(params=flush_arg_list)  # type: ignore
def flush_arg(request: Any) -> str:
    """False: do not flush print stream, True: flush print stream """
    return cast(str, request.param)


enabled_arg_list = ['0',
                    'static_true',
                    'static_false',
                    'dynamic_true',
                    'dynamic_false'
                    ]


@pytest.fixture(params=enabled_arg_list)  # type: ignore
def enabled_arg(request: Any) -> str:
    """determines how to specify time_box_enabled """
    return cast(str, request.param)


class TestStartStopHeader():

    @pytest.fixture(scope='class')  # type: ignore
    def hdr(self) -> "StartStopHeader":
        return StartStopHeader('TestName')

    def test_print_start_msg(self, hdr: "StartStopHeader", capsys: Any,
                             dt_format_arg: DT_Format,
                             end_arg: str,
                             file_arg: str,
                             flush_arg: str) -> None:

        route_num, expected_dt_format, end, file, \
            flush, enabled_TF = TestTimeBox.get_arg_flags(
                      dt_format=dt_format_arg,
                      end=end_arg,
                      file=file_arg,
                      flush=flush_arg,
                      enabled='0')

        if route_num == TestTimeBox.DT0_END0_FILE0_FLUSH0_ENAB0:
            hdr.print_start_msg()
        elif route_num == TestTimeBox.DT0_END0_FILE0_FLUSH1_ENAB0:
            hdr.print_start_msg(flush=flush)
        elif route_num == TestTimeBox.DT0_END0_FILE1_FLUSH0_ENAB0:
            hdr.print_start_msg(file=eval(file_arg))
        elif route_num == TestTimeBox.DT0_END0_FILE1_FLUSH1_ENAB0:
            hdr.print_start_msg(file=eval(file_arg), flush=flush)
        elif route_num == TestTimeBox.DT0_END1_FILE0_FLUSH0_ENAB0:
            hdr.print_start_msg(end=end_arg)
        elif route_num == TestTimeBox.DT0_END1_FILE0_FLUSH1_ENAB0:
            hdr.print_start_msg(end=end_arg, flush=flush)
        elif route_num == TestTimeBox.DT0_END1_FILE1_FLUSH0_ENAB0:
            hdr.print_start_msg(end=end_arg, file=eval(file_arg))
        elif route_num == TestTimeBox.DT0_END1_FILE1_FLUSH1_ENAB0:
            hdr.print_start_msg(end=end_arg, file=eval(file_arg),
                                flush=flush)
        elif route_num == TestTimeBox.DT1_END0_FILE0_FLUSH0_ENAB0:
            hdr.print_start_msg(dt_format=dt_format_arg)
        elif route_num == TestTimeBox.DT1_END0_FILE0_FLUSH1_ENAB0:
            hdr.print_start_msg(dt_format=dt_format_arg, flush=flush)
        elif route_num == TestTimeBox.DT1_END0_FILE1_FLUSH0_ENAB0:
            hdr.print_start_msg(dt_format=dt_format_arg, file=eval(file_arg))
        elif route_num == TestTimeBox.DT1_END0_FILE1_FLUSH1_ENAB0:
            hdr.print_start_msg(dt_format=dt_format_arg, file=eval(file_arg),
                                flush=flush)
        elif route_num == TestTimeBox.DT1_END1_FILE0_FLUSH0_ENAB0:
            hdr.print_start_msg(dt_format=dt_format_arg, end=end_arg)
        elif route_num == TestTimeBox.DT1_END1_FILE0_FLUSH1_ENAB0:
            hdr.print_start_msg(dt_format=dt_format_arg, end=end_arg,
                                flush=flush)
        elif route_num == TestTimeBox.DT1_END1_FILE1_FLUSH0_ENAB0:
            hdr.print_start_msg(dt_format=dt_format_arg, end=end_arg,
                                file=eval(file_arg))
        else:  # route_num == TestTimeBox.DT1_END1_FILE1_FLUSH1_ENAB0:
            hdr.print_start_msg(dt_format=dt_format_arg, end=end_arg,
                                file=eval(file_arg), flush=flush)

        if file == 'sys.stdout':
            captured = capsys.readouterr().out
        else:
            captured = capsys.readouterr().err

        start_DT = hdr.start_DT
        formatted_DT = start_DT.strftime(expected_dt_format)
        msg = '* Starting TestName on ' + formatted_DT + ' *'
        flowers = '*' * len(msg)
        expected = '\n' + flowers + end + msg + end + flowers + end
        assert captured == expected

    def test_print_end_msg(self, hdr: "StartStopHeader", capsys: Any,
                           dt_format_arg: DT_Format,
                           end_arg: str,
                           file_arg: str,
                           flush_arg: str) -> None:

        route_num, expected_dt_format, end, file, \
            flush, enabled_TF = TestTimeBox.get_arg_flags(
                      dt_format=dt_format_arg,
                      end=end_arg,
                      file=file_arg,
                      flush=flush_arg,
                      enabled='0')

        if route_num == TestTimeBox.DT0_END0_FILE0_FLUSH0_ENAB0:
            hdr.print_end_msg()
        elif route_num == TestTimeBox.DT0_END0_FILE0_FLUSH1_ENAB0:
            hdr.print_end_msg(flush=flush)
        elif route_num == TestTimeBox.DT0_END0_FILE1_FLUSH0_ENAB0:
            hdr.print_end_msg(file=eval(file_arg))
        elif route_num == TestTimeBox.DT0_END0_FILE1_FLUSH1_ENAB0:
            hdr.print_end_msg(file=eval(file_arg), flush=flush)
        elif route_num == TestTimeBox.DT0_END1_FILE0_FLUSH0_ENAB0:
            hdr.print_end_msg(end=end_arg)
        elif route_num == TestTimeBox.DT0_END1_FILE0_FLUSH1_ENAB0:
            hdr.print_end_msg(end=end_arg, flush=flush)
        elif route_num == TestTimeBox.DT0_END1_FILE1_FLUSH0_ENAB0:
            hdr.print_end_msg(end=end_arg, file=eval(file_arg))
        elif route_num == TestTimeBox.DT0_END1_FILE1_FLUSH1_ENAB0:
            hdr.print_end_msg(end=end_arg, file=eval(file_arg),
                              flush=flush)
        elif route_num == TestTimeBox.DT1_END0_FILE0_FLUSH0_ENAB0:
            hdr.print_end_msg(dt_format=dt_format_arg)
        elif route_num == TestTimeBox.DT1_END0_FILE0_FLUSH1_ENAB0:
            hdr.print_end_msg(dt_format=dt_format_arg, flush=flush)
        elif route_num == TestTimeBox.DT1_END0_FILE1_FLUSH0_ENAB0:
            hdr.print_end_msg(dt_format=dt_format_arg, file=eval(file_arg))
        elif route_num == TestTimeBox.DT1_END0_FILE1_FLUSH1_ENAB0:
            hdr.print_end_msg(dt_format=dt_format_arg, file=eval(file_arg),
                              flush=flush)
        elif route_num == TestTimeBox.DT1_END1_FILE0_FLUSH0_ENAB0:
            hdr.print_end_msg(dt_format=dt_format_arg, end=end_arg)
        elif route_num == TestTimeBox.DT1_END1_FILE0_FLUSH1_ENAB0:
            hdr.print_end_msg(dt_format=dt_format_arg, end=end_arg,
                              flush=flush)
        elif route_num == TestTimeBox.DT1_END1_FILE1_FLUSH0_ENAB0:
            hdr.print_end_msg(dt_format=dt_format_arg, end=end_arg,
                              file=eval(file_arg))
        else:  # route_num == TestTimeBox.DT1_END1_FILE1_FLUSH1_ENAB0:
            hdr.print_end_msg(dt_format=dt_format_arg, end=end_arg,
                              file=eval(file_arg), flush=flush)

        if file == 'sys.stdout':
            captured = capsys.readouterr().out
        else:
            captured = capsys.readouterr().err

        start_DT = hdr.start_DT
        end_DT = hdr.end_DT
        formatted_delta = str(end_DT - start_DT)
        formatted_DT = end_DT.strftime(expected_dt_format)
        msg1 = '* Ending TestName on ' + formatted_DT
        msg2 = '* Elapsed time: ' + formatted_delta
        flower_len = max(len(msg1), len(msg2)) + 2
        flowers = '*' * flower_len
        msg1 += ' ' * (flower_len - len(msg1) - 1) + '*'
        msg2 += ' ' * (flower_len - len(msg2) - 1) + '*'
        expected = '\n' + flowers + end + msg1 + end + msg2 + end +\
                   flowers + end
        assert captured == expected


class TestTimeBox():

    DT1 = 0b00010000
    END1 = 0b00001000
    FILE1 = 0b00000100
    FLUSH1 = 0b00000010
    ENAB1 = 0b00000001

    DT0_END0_FILE0_FLUSH0_ENAB0 = 0b00000000
    DT0_END0_FILE0_FLUSH0_ENAB1 = 0b00000001
    DT0_END0_FILE0_FLUSH1_ENAB0 = 0b00000010
    DT0_END0_FILE0_FLUSH1_ENAB1 = 0b00000011
    DT0_END0_FILE1_FLUSH0_ENAB0 = 0b00000100
    DT0_END0_FILE1_FLUSH0_ENAB1 = 0b00000101
    DT0_END0_FILE1_FLUSH1_ENAB0 = 0b00000110
    DT0_END0_FILE1_FLUSH1_ENAB1 = 0b00000111
    DT0_END1_FILE0_FLUSH0_ENAB0 = 0b00001000
    DT0_END1_FILE0_FLUSH0_ENAB1 = 0b00001001
    DT0_END1_FILE0_FLUSH1_ENAB0 = 0b00001010
    DT0_END1_FILE0_FLUSH1_ENAB1 = 0b00001011
    DT0_END1_FILE1_FLUSH0_ENAB0 = 0b00001100
    DT0_END1_FILE1_FLUSH0_ENAB1 = 0b00001101
    DT0_END1_FILE1_FLUSH1_ENAB0 = 0b00001110
    DT0_END1_FILE1_FLUSH1_ENAB1 = 0b00001111
    DT1_END0_FILE0_FLUSH0_ENAB0 = 0b00010000
    DT1_END0_FILE0_FLUSH0_ENAB1 = 0b00010001
    DT1_END0_FILE0_FLUSH1_ENAB0 = 0b00010010
    DT1_END0_FILE0_FLUSH1_ENAB1 = 0b00010011
    DT1_END0_FILE1_FLUSH0_ENAB0 = 0b00010100
    DT1_END0_FILE1_FLUSH0_ENAB1 = 0b00010101
    DT1_END0_FILE1_FLUSH1_ENAB0 = 0b00010110
    DT1_END0_FILE1_FLUSH1_ENAB1 = 0b00010111
    DT1_END1_FILE0_FLUSH0_ENAB0 = 0b00011000
    DT1_END1_FILE0_FLUSH0_ENAB1 = 0b00011001
    DT1_END1_FILE0_FLUSH1_ENAB0 = 0b00011010
    DT1_END1_FILE0_FLUSH1_ENAB1 = 0b00011011
    DT1_END1_FILE1_FLUSH0_ENAB0 = 0b00011100
    DT1_END1_FILE1_FLUSH0_ENAB1 = 0b00011101
    DT1_END1_FILE1_FLUSH1_ENAB0 = 0b00011110
    DT1_END1_FILE1_FLUSH1_ENAB1 = 0b00011111

    @staticmethod
    def get_arg_flags(*,
                      dt_format: str,
                      end: str,
                      file: str,
                      flush: str,
                      enabled: str
                      ) -> Tuple[int, DT_Format, str, str, bool, bool]:

        route_num = TestTimeBox.DT0_END0_FILE0_FLUSH0_ENAB0

        expected_dt_format = DT_Format(StartStopHeader.default_dt_format)
        if dt_format != '0':
            route_num = route_num | TestTimeBox.DT1
            expected_dt_format = DT_Format(dt_format)

        expected_end = '\n'
        if end != '0':
            route_num = route_num | TestTimeBox.END1
            expected_end = end

        expected_file = 'sys.stdout'
        if file != '0':
            route_num = route_num | TestTimeBox.FILE1
            if file != 'None':
                expected_file = file

        # Note: we can specify flush but we can not verify whether it works
        expected_flush = False
        if flush != '0':
            route_num = route_num | TestTimeBox.FLUSH1
            if flush == 'True':
                expected_flush = True

        expected_enabled_TF = True
        if enabled != '0':
            route_num = route_num | TestTimeBox.ENAB1
            if (enabled == 'static_false') or (enabled == 'dynamic_false'):
                expected_enabled_TF = False

        return (route_num, expected_dt_format, expected_end, expected_file,
                expected_flush, expected_enabled_TF)

    @staticmethod
    def get_expected_msg(*,
                         expected_aFunc_msg: str,
                         actual: str,
                         expected_dt_format: DT_Format =
                         DT_Format('%a %b %d %Y %H:%M:%S'),
                         # StartStopHeader.default_dt_format,
                         expected_end: str = '\n',
                         expected_enabled_TF: bool = True) -> str:
        """Helper function to build the expected message to compare
        with the actual message captured with capsys
        """

        if expected_enabled_TF is False:
            if expected_aFunc_msg == '':
                return ''
            else:
                return expected_aFunc_msg + '\n'

        start_DT = datetime.now()
        end_DT = datetime.now() + timedelta(microseconds=42)
        formatted_delta = str(end_DT - start_DT)
        formatted_delta_len = len(formatted_delta)

        formatted_DT = start_DT.strftime(expected_dt_format)
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

        expected0 = '\n' + flowers + expected_end + msg0 + expected_end \
            + flowers + expected_end

        # build expected1
        msg1 = '* Ending aFunc on ' + end_time_marks
        msg2 = '* Elapsed time: ' + elapsed_time_marks

        flower_len = max(len(msg1), len(msg2)) + 2
        flowers = '*' * flower_len

        msg1 += ' ' * (flower_len - len(msg1) - 1) + '*'
        msg2 += ' ' * (flower_len - len(msg2) - 1) + '*'

        expected1 = '\n' + flowers + expected_end + msg1 + expected_end \
            + msg2 + expected_end + flowers + expected_end

        if expected_aFunc_msg == '':
            expected = expected0 + expected1
        else:
            expected = expected0 + expected_aFunc_msg + '\n' + expected1

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

    """
    The following section tests each combination of arguments to the time_box
    decorator for three styles of decoration (using pie, calling the
    with the function as the first parameter, and calling the decorator with
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

    """

    def test_timebox_router(self,
                            capsys: Any,
                            style_num: int,
                            dt_format_arg: str,
                            end_arg: str,
                            file_arg: str,
                            flush_arg: str,
                            enabled_arg: str
                            ) -> None:

        # aFunc: Union[Callable[[int, str], int],
        #              Callable[[int, str], None],
        #              Callable[[], int],
        #              Callable[[], None]]

        aFunc: Callable[..., Any]

        expected_return_value: Union[int, None]

        # route_num = 0
        # if dt_format_arg != '0':
        #     route_num += 2**4
        #     expected_dt_format = DT_Format(dt_format_arg)
        # else:
        #     expected_dt_format = DT_Format(StartStopHeader.default_dt_format)

        # if end_arg != '0':
        #     route_num += 2**3
        #     expected_end_arg = end_arg
        # else:
        #     expected_end_arg = '\n'

        # if file_arg != '0':
        #     route_num += 2**2
        #     if file_arg == 'None':
        #         expected_file_arg = 'sys.stdout'
        #     else:
        #         expected_file_arg = file_arg
        # else:
        #     expected_file_arg = 'sys.stdout'

        # # Note: we can specify flush but we can not verify whether it works
        # flush = False
        # if flush_arg != '0':
        #     route_num += 2**1
        #     if flush_arg == 'True':
        #         flush = True

        route_num, expected_dt_format, expected_end_arg, expected_file_arg, \
            flush, enabled_TF = TestTimeBox.get_arg_flags(
                      dt_format=dt_format_arg,
                      end=end_arg,
                      file=file_arg,
                      flush=flush_arg,
                      enabled=enabled_arg)

        enabled_spec: Union[bool, Callable[..., bool]] = enabled_TF
        def enabled_func() -> bool: return enabled_TF

        if (enabled_arg == 'dynamic_true') or (enabled_arg == 'dynamic_false'):
            enabled_spec = enabled_func

        if style_num == 1:
            for func_style in range(1, 5):
                aFunc = TestTimeBox.build_style1_func(
                    route_num,
                    dt_format=DT_Format(dt_format_arg),
                    end=end_arg,
                    file=file_arg,
                    flush=flush,
                    enabled=enabled_spec,
                    f_style=func_style
                    )

                if func_style == 1:
                    aFunc_msg = 'The answer is: ' + str(route_num)
                    expected_return_value = route_num * style_num
                    actual_return_value = aFunc(route_num,
                                                aFunc_msg)
                elif func_style == 2:
                    aFunc_msg = 'The answer is: ' + str(route_num)
                    expected_return_value = None
                    actual_return_value = aFunc(route_num, aFunc_msg)
                elif func_style == 3:
                    aFunc_msg = ''
                    expected_return_value = 42
                    actual_return_value = aFunc()
                else:  # func_style == 4:
                    aFunc_msg = ''
                    expected_return_value = None
                    actual_return_value = aFunc()

                TestTimeBox.check_results(
                    capsys=capsys,
                    aFunc_msg=aFunc_msg,
                    expected_dt_format=expected_dt_format,
                    expected_end=expected_end_arg,
                    expected_file=expected_file_arg,
                    expected_enabled_TF=enabled_TF,
                    expected_return_value=expected_return_value,
                    actual_return_value=actual_return_value
                    )
                if route_num > TestTimeBox.DT0_END0_FILE1_FLUSH1_ENAB1:
                    break
            return

        elif style_num == 2:
            aFunc = TestTimeBox.build_style2_func(
                route_num,
                dt_format=DT_Format(dt_format_arg),
                end=end_arg,
                file=file_arg,
                flush=flush,
                enabled=enabled_spec
                )
        else:  # style_num = 3
            aFunc = TestTimeBox.build_style3_func(
                route_num,
                dt_format=DT_Format(dt_format_arg),
                end=end_arg,
                file=file_arg,
                flush=flush,
                enabled=enabled_spec
                )

        aFunc_msg = 'The answer is: ' + str(route_num)
        expected_return_value = route_num * style_num
        actual_return_value = aFunc(route_num, aFunc_msg)
        TestTimeBox.check_results(
            capsys=capsys,
            aFunc_msg=aFunc_msg,
            expected_dt_format=expected_dt_format,
            expected_end=expected_end_arg,
            expected_file=expected_file_arg,
            expected_enabled_TF=enabled_TF,
            expected_return_value=expected_return_value,
            actual_return_value=actual_return_value
            )

    @staticmethod
    def check_results(capsys: Any,
                      aFunc_msg: str,
                      expected_dt_format: DT_Format,
                      expected_end: str,
                      expected_file: str,
                      expected_enabled_TF: bool,
                      expected_return_value: Union[int, None],
                      actual_return_value: Union[int, None]
                      ) -> None:

        if expected_file == 'sys.stdout':
            actual = capsys.readouterr().out
        else:
            actual = capsys.readouterr().err
            aFunc_msg = ''

        expected = TestTimeBox.get_expected_msg(
            expected_aFunc_msg=aFunc_msg,
            actual=actual,
            expected_dt_format=expected_dt_format,
            expected_end=expected_end,
            expected_enabled_TF=expected_enabled_TF)

        assert actual == expected

        # check that aFunc returns the correct value

        message = "Expected return value: {0}, Actual return value: {1}"\
            .format(expected_return_value, actual_return_value)
        assert expected_return_value == actual_return_value, message

    @staticmethod
    def build_style1_func(route_num: int,
                          dt_format: DT_Format,
                          end: str,
                          file: str,
                          flush: bool,
                          enabled: Union[bool, Callable[..., bool]],
                          f_style: int
                          ) -> Callable[..., Any]:

        # aFunc: Union[Callable[[int, str], int],
        #              Callable[[int, str], None],
        #              Callable[[], int],
        #              Callable[[], None]]

        if route_num == TestTimeBox.DT0_END0_FILE0_FLUSH0_ENAB0:
            if f_style == 1:
                @time_box
                def aFunc(aInt: int, aStr: str) -> int:
                    print(aStr)
                    return aInt * 1
            elif f_style == 2:
                @time_box
                def aFunc(aInt: int, aStr: str) -> None:
                    print(aStr)
            elif f_style == 3:
                @time_box
                def aFunc() -> int:
                    return 42
            else:  # f_style == 4:
                @time_box
                def aFunc() -> None:
                    pass
        elif route_num == TestTimeBox.DT0_END0_FILE0_FLUSH0_ENAB1:
            if f_style == 1:
                @time_box(time_box_enabled=enabled)
                def aFunc(aInt: int, aStr: str) -> int:
                    print(aStr)
                    return aInt * 1
            elif f_style == 2:
                @time_box(time_box_enabled=enabled)
                def aFunc(aInt: int, aStr: str) -> None:
                    print(aStr)
            elif f_style == 3:
                @time_box(time_box_enabled=enabled)
                def aFunc() -> int:
                    return 42
            else:  # f_style == 4:
                @time_box(time_box_enabled=enabled)
                def aFunc() -> None:
                    pass
        elif route_num == TestTimeBox.DT0_END0_FILE0_FLUSH1_ENAB0:
            if f_style == 1:
                @time_box(flush=flush)
                def aFunc(aInt: int, aStr: str) -> int:
                    print(aStr)
                    return aInt * 1
            elif f_style == 2:
                @time_box(flush=flush)
                def aFunc(aInt: int, aStr: str) -> None:
                    print(aStr)
            elif f_style == 3:
                @time_box(flush=flush)
                def aFunc() -> int:
                    return 42
            else:  # f_style == 4:
                @time_box(flush=flush)
                def aFunc() -> None:
                    pass
        elif route_num == TestTimeBox.DT0_END0_FILE0_FLUSH1_ENAB1:
            if f_style == 1:
                @time_box(flush=flush, time_box_enabled=enabled)
                def aFunc(aInt: int, aStr: str) -> int:
                    print(aStr)
                    return aInt * 1
            elif f_style == 2:
                @time_box(flush=flush, time_box_enabled=enabled)
                def aFunc(aInt: int, aStr: str) -> None:
                    print(aStr)
            elif f_style == 3:
                @time_box(flush=flush, time_box_enabled=enabled)
                def aFunc() -> int:
                    return 42
            else:  # f_style == 4:
                @time_box(flush=flush, time_box_enabled=enabled)
                def aFunc() -> None:
                    pass
        elif route_num == TestTimeBox.DT0_END0_FILE1_FLUSH0_ENAB0:
            if f_style == 1:
                @time_box(file=eval(file))
                def aFunc(aInt: int, aStr: str) -> int:
                    print(aStr)
                    return aInt * 1
            elif f_style == 2:
                @time_box(file=eval(file))
                def aFunc(aInt: int, aStr: str) -> None:
                    print(aStr)
            elif f_style == 3:
                @time_box(file=eval(file))
                def aFunc() -> int:
                    return 42
            else:  # f_style == 4:
                @time_box(file=eval(file))
                def aFunc() -> None:
                    pass
        elif route_num == TestTimeBox.DT0_END0_FILE1_FLUSH0_ENAB1:
            if f_style == 1:
                @time_box(file=eval(file), time_box_enabled=enabled)
                def aFunc(aInt: int, aStr: str) -> int:
                    print(aStr)
                    return aInt * 1
            elif f_style == 2:
                @time_box(file=eval(file), time_box_enabled=enabled)
                def aFunc(aInt: int, aStr: str) -> None:
                    print(aStr)
            elif f_style == 3:
                @time_box(file=eval(file), time_box_enabled=enabled)
                def aFunc() -> int:
                    return 42
            else:  # f_style == 4:
                @time_box(file=eval(file), time_box_enabled=enabled)
                def aFunc() -> None:
                    pass
        elif route_num == TestTimeBox.DT0_END0_FILE1_FLUSH1_ENAB0:
            if f_style == 1:
                @time_box(file=eval(file), flush=flush)
                def aFunc(aInt: int, aStr: str) -> int:
                    print(aStr)
                    return aInt * 1
            elif f_style == 2:
                @time_box(file=eval(file), flush=flush)
                def aFunc(aInt: int, aStr: str) -> None:
                    print(aStr)
            elif f_style == 3:
                @time_box(file=eval(file), flush=flush)
                def aFunc() -> int:
                    return 42
            else:  # f_style == 4:
                @time_box(file=eval(file), flush=flush)
                def aFunc() -> None:
                    pass
        elif route_num == TestTimeBox.DT0_END0_FILE1_FLUSH1_ENAB1:
            if f_style == 1:
                @time_box(file=eval(file), flush=flush,
                          time_box_enabled=enabled)
                def aFunc(aInt: int, aStr: str) -> int:
                    print(aStr)
                    return aInt * 1
            elif f_style == 2:
                @time_box(file=eval(file), flush=flush,
                          time_box_enabled=enabled)
                def aFunc(aInt: int, aStr: str) -> None:
                    print(aStr)
            elif f_style == 3:
                @time_box(file=eval(file), flush=flush,
                          time_box_enabled=enabled)
                def aFunc() -> int:
                    return 42
            else:  # f_style == 4:
                @time_box(file=eval(file), flush=flush,
                          time_box_enabled=enabled)
                def aFunc() -> None:
                    pass
        elif route_num == TestTimeBox.DT0_END1_FILE0_FLUSH0_ENAB0:
            @time_box(end=end)
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 1
        elif route_num == TestTimeBox.DT0_END1_FILE0_FLUSH0_ENAB1:
            @time_box(end=end, time_box_enabled=enabled)
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 1
        elif route_num == TestTimeBox.DT0_END1_FILE0_FLUSH1_ENAB0:
            @time_box(end=end, flush=flush)
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 1
        elif route_num == TestTimeBox.DT0_END1_FILE0_FLUSH1_ENAB1:
            @time_box(end=end, flush=flush, time_box_enabled=enabled)
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 1
        elif route_num == TestTimeBox.DT0_END1_FILE1_FLUSH0_ENAB0:
            @time_box(end=end, file=eval(file))
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 1
        elif route_num == TestTimeBox.DT0_END1_FILE1_FLUSH0_ENAB1:
            @time_box(end=end, file=eval(file), time_box_enabled=enabled)
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 1
        elif route_num == TestTimeBox.DT0_END1_FILE1_FLUSH1_ENAB0:
            @time_box(end=end, file=eval(file), flush=flush)
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 1
        elif route_num == TestTimeBox.DT0_END1_FILE1_FLUSH1_ENAB1:
            @time_box(end=end, file=eval(file), flush=flush,
                      time_box_enabled=enabled)
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 1
        elif route_num == TestTimeBox.DT1_END0_FILE0_FLUSH0_ENAB0:
            @time_box(dt_format=dt_format)
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 1
        elif route_num == TestTimeBox.DT1_END0_FILE0_FLUSH0_ENAB1:
            @time_box(dt_format=dt_format, time_box_enabled=enabled)
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 1
        elif route_num == TestTimeBox.DT1_END0_FILE0_FLUSH1_ENAB0:
            @time_box(dt_format=dt_format, flush=flush)
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 1
        elif route_num == TestTimeBox.DT1_END0_FILE0_FLUSH1_ENAB1:
            @time_box(dt_format=dt_format, flush=flush,
                      time_box_enabled=enabled)
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 1
        elif route_num == TestTimeBox.DT1_END0_FILE1_FLUSH0_ENAB0:
            @time_box(dt_format=dt_format, file=eval(file))
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 1
        elif route_num == TestTimeBox.DT1_END0_FILE1_FLUSH0_ENAB1:
            @time_box(dt_format=dt_format, file=eval(file),
                      time_box_enabled=enabled)
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 1
        elif route_num == TestTimeBox.DT1_END0_FILE1_FLUSH1_ENAB0:
            @time_box(dt_format=dt_format, file=eval(file), flush=flush)
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 1
        elif route_num == TestTimeBox.DT1_END0_FILE1_FLUSH1_ENAB1:
            @time_box(dt_format=dt_format, file=eval(file), flush=flush,
                      time_box_enabled=enabled)
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 1
        elif route_num == TestTimeBox.DT1_END1_FILE0_FLUSH0_ENAB0:
            @time_box(dt_format=dt_format, end=end)
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 1
        elif route_num == TestTimeBox.DT1_END1_FILE0_FLUSH0_ENAB1:
            @time_box(dt_format=dt_format, end=end, time_box_enabled=enabled)
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 1
        elif route_num == TestTimeBox.DT1_END1_FILE0_FLUSH1_ENAB0:
            @time_box(dt_format=dt_format, end=end, flush=flush)
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 1
        elif route_num == TestTimeBox.DT1_END1_FILE0_FLUSH1_ENAB1:
            @time_box(dt_format=dt_format, end=end, flush=flush,
                      time_box_enabled=enabled)
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 1
        elif route_num == TestTimeBox.DT1_END1_FILE1_FLUSH0_ENAB0:
            @time_box(dt_format=dt_format, end=end, file=eval(file))
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 1
        elif route_num == TestTimeBox.DT1_END1_FILE1_FLUSH0_ENAB1:
            @time_box(dt_format=dt_format, end=end, file=eval(file),
                      time_box_enabled=enabled)
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 1
        elif route_num == TestTimeBox.DT1_END1_FILE1_FLUSH1_ENAB0:
            @time_box(dt_format=dt_format, end=end, file=eval(file),
                      flush=flush)
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 1
        elif route_num == TestTimeBox.DT1_END1_FILE1_FLUSH1_ENAB1:
            @time_box(dt_format=dt_format, end=end, file=eval(file),
                      flush=flush, time_box_enabled=enabled)
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 1

        return aFunc

    @staticmethod
    def build_style2_func(route_num: int,
                          dt_format: DT_Format,
                          end: str,
                          file: str,
                          flush: bool,
                          enabled: Union[bool, Callable[..., bool]]
                          ) -> Callable[[int, str], int]:

        if route_num == TestTimeBox.DT0_END0_FILE0_FLUSH0_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc)
        elif route_num == TestTimeBox.DT0_END0_FILE0_FLUSH0_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, time_box_enabled=enabled)
        elif route_num == TestTimeBox.DT0_END0_FILE0_FLUSH1_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, flush=flush)
        elif route_num == TestTimeBox.DT0_END0_FILE0_FLUSH1_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, flush=flush, time_box_enabled=enabled)
        elif route_num == TestTimeBox.DT0_END0_FILE1_FLUSH0_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, file=eval(file))
        elif route_num == TestTimeBox.DT0_END0_FILE1_FLUSH0_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, file=eval(file), time_box_enabled=enabled)
        elif route_num == TestTimeBox.DT0_END0_FILE1_FLUSH1_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, file=eval(file), flush=flush)
        elif route_num == TestTimeBox.DT0_END0_FILE1_FLUSH1_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, file=eval(file), flush=flush,
                             time_box_enabled=enabled)
        elif route_num == TestTimeBox.DT0_END1_FILE0_FLUSH0_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, end=end)
        elif route_num == TestTimeBox.DT0_END1_FILE0_FLUSH0_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, end=end, time_box_enabled=enabled)
        elif route_num == TestTimeBox.DT0_END1_FILE0_FLUSH1_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, end=end, flush=flush)
        elif route_num == TestTimeBox.DT0_END1_FILE0_FLUSH1_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, end=end, flush=flush,
                             time_box_enabled=enabled)
        elif route_num == TestTimeBox.DT0_END1_FILE1_FLUSH0_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, end=end, file=eval(file))
        elif route_num == TestTimeBox.DT0_END1_FILE1_FLUSH0_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, end=end, file=eval(file),
                             time_box_enabled=enabled)
        elif route_num == TestTimeBox.DT0_END1_FILE1_FLUSH1_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, end=end, file=eval(file), flush=flush)
        elif route_num == TestTimeBox.DT0_END1_FILE1_FLUSH1_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, end=end, file=eval(file), flush=flush,
                             time_box_enabled=enabled)
        elif route_num == TestTimeBox.DT1_END0_FILE0_FLUSH0_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, dt_format=dt_format)
        elif route_num == TestTimeBox.DT1_END0_FILE0_FLUSH0_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, dt_format=dt_format,
                             time_box_enabled=enabled)
        elif route_num == TestTimeBox.DT1_END0_FILE0_FLUSH1_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, dt_format=dt_format, flush=flush)
        elif route_num == TestTimeBox.DT1_END0_FILE0_FLUSH1_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, dt_format=dt_format, flush=flush,
                             time_box_enabled=enabled)
        elif route_num == TestTimeBox.DT1_END0_FILE1_FLUSH0_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, dt_format=dt_format, file=eval(file))
        elif route_num == TestTimeBox.DT1_END0_FILE1_FLUSH0_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, dt_format=dt_format, file=eval(file),
                             time_box_enabled=enabled)
        elif route_num == TestTimeBox.DT1_END0_FILE1_FLUSH1_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, dt_format=dt_format, file=eval(file),
                             flush=flush)
        elif route_num == TestTimeBox.DT1_END0_FILE1_FLUSH1_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, dt_format=dt_format, file=eval(file),
                             flush=flush, time_box_enabled=enabled)
        elif route_num == TestTimeBox.DT1_END1_FILE0_FLUSH0_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, dt_format=dt_format, end=end)
        elif route_num == TestTimeBox.DT1_END1_FILE0_FLUSH0_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, dt_format=dt_format, end=end,
                             time_box_enabled=enabled)
        elif route_num == TestTimeBox.DT1_END1_FILE0_FLUSH1_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, dt_format=dt_format, end=end, flush=flush)
        elif route_num == TestTimeBox.DT1_END1_FILE0_FLUSH1_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, dt_format=dt_format, end=end, flush=flush,
                             time_box_enabled=enabled)
        elif route_num == TestTimeBox.DT1_END1_FILE1_FLUSH0_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, dt_format=dt_format, end=end,
                             file=eval(file))
        elif route_num == TestTimeBox.DT1_END1_FILE1_FLUSH0_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, dt_format=dt_format, end=end,
                             file=eval(file), time_box_enabled=enabled)
        elif route_num == TestTimeBox.DT1_END1_FILE1_FLUSH1_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, dt_format=dt_format, end=end,
                             file=eval(file), flush=flush)
        elif route_num == TestTimeBox.DT1_END1_FILE1_FLUSH1_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 2
            aFunc = time_box(aFunc, dt_format=dt_format, end=end,
                             file=eval(file), flush=flush,
                             time_box_enabled=enabled)

        return aFunc

    @staticmethod
    def build_style3_func(route_num: int,
                          dt_format: DT_Format,
                          end: str,
                          file: str,
                          flush: bool,
                          enabled: Union[bool, Callable[..., bool]]
                          ) -> Callable[[int, str], int]:

        if route_num == TestTimeBox.DT0_END0_FILE0_FLUSH0_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box()(aFunc)
        elif route_num == TestTimeBox.DT0_END0_FILE0_FLUSH0_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(time_box_enabled=enabled)(aFunc)
        elif route_num == TestTimeBox.DT0_END0_FILE0_FLUSH1_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(flush=flush)(aFunc)
        elif route_num == TestTimeBox.DT0_END0_FILE0_FLUSH1_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(flush=flush, time_box_enabled=enabled)(aFunc)
        elif route_num == TestTimeBox.DT0_END0_FILE1_FLUSH0_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(file=eval(file))(aFunc)
        elif route_num == TestTimeBox.DT0_END0_FILE1_FLUSH0_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(file=eval(file), time_box_enabled=enabled)(aFunc)
        elif route_num == TestTimeBox.DT0_END0_FILE1_FLUSH1_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(file=eval(file), flush=flush)(aFunc)
        elif route_num == TestTimeBox.DT0_END0_FILE1_FLUSH1_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(file=eval(file), flush=flush,
                             time_box_enabled=enabled)(aFunc)
        elif route_num == TestTimeBox.DT0_END1_FILE0_FLUSH0_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(end=end)(aFunc)
        elif route_num == TestTimeBox.DT0_END1_FILE0_FLUSH0_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(end=end, time_box_enabled=enabled)(aFunc)
        elif route_num == TestTimeBox.DT0_END1_FILE0_FLUSH1_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(end=end, flush=flush)(aFunc)
        elif route_num == TestTimeBox.DT0_END1_FILE0_FLUSH1_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(end=end, flush=flush,
                             time_box_enabled=enabled)(aFunc)
        elif route_num == TestTimeBox.DT0_END1_FILE1_FLUSH0_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(end=end, file=eval(file))(aFunc)
        elif route_num == TestTimeBox.DT0_END1_FILE1_FLUSH0_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(end=end, file=eval(file),
                             time_box_enabled=enabled)(aFunc)
        elif route_num == TestTimeBox.DT0_END1_FILE1_FLUSH1_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(end=end, file=eval(file), flush=flush)(aFunc)
        elif route_num == TestTimeBox.DT0_END1_FILE1_FLUSH1_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(end=end, file=eval(file), flush=flush,
                             time_box_enabled=enabled)(aFunc)
        elif route_num == TestTimeBox.DT1_END0_FILE0_FLUSH0_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(dt_format=dt_format)(aFunc)
        elif route_num == TestTimeBox.DT1_END0_FILE0_FLUSH0_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(dt_format=dt_format,
                             time_box_enabled=enabled)(aFunc)
        elif route_num == TestTimeBox.DT1_END0_FILE0_FLUSH1_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(dt_format=dt_format, flush=flush)(aFunc)
        elif route_num == TestTimeBox.DT1_END0_FILE0_FLUSH1_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(dt_format=dt_format, flush=flush,
                             time_box_enabled=enabled)(aFunc)
        elif route_num == TestTimeBox.DT1_END0_FILE1_FLUSH0_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(dt_format=dt_format, file=eval(file))(aFunc)
        elif route_num == TestTimeBox.DT1_END0_FILE1_FLUSH0_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(dt_format=dt_format, file=eval(file),
                             time_box_enabled=enabled)(aFunc)
        elif route_num == TestTimeBox.DT1_END0_FILE1_FLUSH1_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(dt_format=dt_format, file=eval(file),
                             flush=flush)(aFunc)
        elif route_num == TestTimeBox.DT1_END0_FILE1_FLUSH1_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(dt_format=dt_format, file=eval(file), flush=flush,
                             time_box_enabled=enabled)(aFunc)
        elif route_num == TestTimeBox.DT1_END1_FILE0_FLUSH0_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(dt_format=dt_format, end=end)(aFunc)
        elif route_num == TestTimeBox.DT1_END1_FILE0_FLUSH0_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(dt_format=dt_format, end=end,
                             time_box_enabled=enabled)(aFunc)
        elif route_num == TestTimeBox.DT1_END1_FILE0_FLUSH1_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(dt_format=dt_format, end=end,
                             flush=flush)(aFunc)
        elif route_num == TestTimeBox.DT1_END1_FILE0_FLUSH1_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(dt_format=dt_format, end=end, flush=flush,
                             time_box_enabled=enabled)(aFunc)
        elif route_num == TestTimeBox.DT1_END1_FILE1_FLUSH0_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(dt_format=dt_format, end=end,
                             file=eval(file))(aFunc)
        elif route_num == TestTimeBox.DT1_END1_FILE1_FLUSH0_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(dt_format=dt_format, end=end, file=eval(file),
                             time_box_enabled=enabled)(aFunc)
        elif route_num == TestTimeBox.DT1_END1_FILE1_FLUSH1_ENAB0:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(dt_format=dt_format, end=end, file=eval(file),
                             flush=flush)(aFunc)
        elif route_num == TestTimeBox.DT1_END1_FILE1_FLUSH1_ENAB1:
            def aFunc(aInt: int, aStr: str) -> int:
                print(aStr)
                return aInt * 3
            aFunc = time_box(dt_format=dt_format, end=end, file=eval(file),
                             flush=flush, time_box_enabled=enabled)(aFunc)

        return aFunc


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
