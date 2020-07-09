#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# =============================================================================
# Created on Wed Apr 22 15:09:41 2020
#
# @author: Scott Tuttle
# =============================================================================


"""
========
time_hdr
========

The time_hdr module contains two items:

    1) StartStopHeader class with two functions that will repectively print
       a starting time and ending time messages in a flower box (see
       flower_box module in sbt_utils package).
    2) a time_box decorator that wraps a function and uses the StartStopHeader
       to print the starting and ending time messages.

:Example: decorate a function with time_box

>>> from sbt_utils.time_hdr import time_box
>>> import time

>>> @time_box
... def aFunc2() -> None:
...      print('2 * 3 =', 2*3)
...      time.sleep(1)

>>> aFunc2()
<BLANKLINE>
***********************************************
* Starting aFunc2 on Mon Jun 29 2020 18:22:50 *
***********************************************
2 * 3 = 6
<BLANKLINE>
*********************************************
* Ending aFunc2 on Mon Jun 29 2020 18:22:51 *
* Elapsed time: 0:00:01.001204              *
*********************************************

time_box imports functools, sys, datetime, and wrapt

"""

import functools
import sys
from datetime import datetime
from typing import Any, Callable, cast, Dict, NewType, Optional, \
                   Tuple, TypeVar, Union

from typing import overload

from sbt_utils.flower_box import print_flower_box_msg

from wrapt.decorators import decorator

DT_Format = NewType('DT_Format', str)


class StartStopHeader():
    """Class StartStopHeader supports the time_box decorator by providing:

        1) a place to store the start time and end time
        2) method print_start_msg to print the start header with the start time
        3) method print_end_msg to print the end trailer with end time and
           elapsed time

    While there might be some standalone uses for this class and its methods,
    its intended use is by the time_box decorator described later in this
    time_hdr module.
    """

    default_dt_format: DT_Format = DT_Format('%a %b %d %Y %H:%M:%S')

    def __init__(self, func_name: str) -> None:
        """Stores the input func_name and sets the start and end times to None

        :param func_name: The name of the function to appear in the start and
            stop messages

        :type func_name: str

        :returns: None
        :rtype: None
        """

        self.func_name = func_name
        self.start_DT: datetime = datetime.max
        self.end_DT: datetime = datetime.min

    def print_end_msg(self, dt_format: DT_Format = default_dt_format,
                      end: str = '\n',
                      file: Optional[Any] = None,
                      flush: bool = False) -> None:
        """The end time message is issued in a flower box

        The end message includes the current datetime and elapsed time
        (calculated as the difference between the end time and the saved start
        time - see the *print_start_msg* method).

        :param dt_format: Specifies the datetime format to use in the end
            time message. The default is StartStopHeader.default_dt_format.
        :type dt_format: DT_Format, optional

        :param end: Specifies the argument to use on the print statement *end*
            parameter for the end time message. The default is \'\\\\n'.
        :type end: str, optional

        :param file: Specifies the argument to use on the print statement
            *file* parameter for the end time message. The default is
            sys.stdout (via None).
        :type file: Optional[Any]

        :param flush: Specifies the argument to use on the print statement
            *flush* parameterfor the end time messsage. The default is False.
        :type flush: bool, optional

        :returns: None
        :rtype: None
        """

        #  note: the following code that sets file to sys.stdout is needed to
        #  allow the test cases to use the pytest capsys built-in fixture.
        #  Having sys.stdout as the default parameter in the function
        #  definition does not work because capsys changes sys.stdout after
        #  the test case gets control, meaning the print statements in
        #  StartStopHeader code are not captured. This is also appears to be
        #  the case for doctest. So, we simply use None as the default and set
        #  file to sys.stdout here below which works fine.

        if file is None:
            file = sys.stdout

        self.end_DT = datetime.now()
        msg1 = 'Ending ' + self.func_name + ' on '\
            + self.end_DT.strftime(dt_format)
        msg2 = 'Elapsed time: ' + str(self.end_DT - self.start_DT)
        print_flower_box_msg([msg1, msg2], end=end, file=file,
                             flush=flush)

    def print_start_msg(self, dt_format: DT_Format = default_dt_format,
                        end: str = '\n',
                        file: Optional[Any] = None,
                        flush: bool = False) -> None:
        """The start time message is issued in a flower box.

        The start message includes the current datetime which is also saved to
        be used later to calculate the elapsed time for the *print_end_msg*
        invocation.

        :param dt_format: Specifies the datetime format to use in the start
            time message. The default is StartStopHeader.default_dt_format.
        :type dt_format: DT_Format, optional

        :param end: Specifies the argument to use on the print statement *end*
            parameter for the start time message. The default is \'\\\\n'.
        :type end: str, optional

        :param file: Specifies the argument to use on the print statement
            *file* parameter for the start time message. The default is
            sys.stdout (via None).
        :type file: Optional[Any]

        :param flush: Specifies the argument to use on the print statement
            *flush* parameterfor the start time messsage. The default is False.
        :type flush: bool, optional

        :returns: None
        :rtype: None

        :Example: Using StartStopHeader with start and end messages.

        >>> from sbt_utils.time_hdr import StartStopHeader
        >>> import time

        >>> def aFunc1() -> None:
        ...      print('2 + 2 =', 2+2)
        ...      time.sleep(2)

        >>> hdr = StartStopHeader('aFunc1')
        >>> hdr.print_start_msg()
        <BLANKLINE>
        ***********************************************
        * Starting aFunc1 on Mon Jun 29 2020 18:22:48 *
        ***********************************************
        >>> aFunc1()
        2 + 2 = 4
        >>> hdr.print_end_msg()
        <BLANKLINE>
        *********************************************
        * Ending aFunc1 on Mon Jun 29 2020 18:22:50 *
        * Elapsed time: 0:00:02.001842              *
        *********************************************

        """

        #  note: the following code that sets file to sys.stdout is needed to
        #  allow the test cases to use the pytest capsys built-in fixture.
        #  Having sys.stdout as the default parameter in the function
        #  definition does not work because capsys changes sys.stdout after
        #  the test case gets control, meaning the print statements in
        # StartStopHeader code are not captured. This is also appears to be
        # the case for doctest. So, we simply use None as the default and set
        # file to sys.stdout here below which works fine.

        if file is None:
            file = sys.stdout

        self.start_DT = datetime.now()
        msg = 'Starting ' + self.func_name + ' on '\
            + self.start_DT.strftime(dt_format)
        print_flower_box_msg([msg], end=end, file=file, flush=flush)


F = TypeVar('F', bound=Callable[..., Any])


@overload
def time_box(wrapped: F, *,
             dt_format: DT_Format = StartStopHeader.default_dt_format,
             end: str = '\n',
             file: Any = sys.stdout,
             flush: bool = False,
             time_box_enabled: Union[bool, Callable[..., bool]] = True
             ) -> F: ...


@overload
def time_box(*,
             dt_format: DT_Format = StartStopHeader.default_dt_format,
             end: str = '\n',
             file: Any = sys.stdout,
             flush: bool = False,
             time_box_enabled: Union[bool, Callable[..., bool]] = True
             ) -> Callable[[F], F]: ...


def time_box(wrapped: Optional[F] = None, *,
             dt_format: DT_Format = StartStopHeader.default_dt_format,
             end: str = '\n',
             # file: Any = sys.stdout,
             file: Optional[Any] = None,
             flush: bool = False,
             time_box_enabled: Union[bool, Callable[..., bool]] = True
             ) -> F:
    """Decorator to wrap a function in start time and end time messages.

    The time_box decorator can be invoked with or with arguments, and the
    function being wrapped can optionally take arguments and optionally
    return a value. The wrapt.decorator is used to preserve the wrapped
    function introspection capabilities, and functools.partial is used to
    handle the case where decorator arguments are specified. The examples
    further below will help demonstrate the various ways in which the
    time_box decorator can be used.

:param wrapped: Any callable function that accepts optional positional
    and/or optional keyword arguments, and optionally returns a value.
    The default is None, which will be the case when the pie decorator
    version is used with any of the following arguments specified.
:type wrapped: Callable[..., Any], optional

:param dt_format: Specifies the datetime format to use in the start
    time message. The default is StartStopHeader.default_dt_format.
:type dt_format: DT_Format, optional

:param end: Specifies the argument to use on the print statement *end*
    parameter for the start time and end time messages issued by the
    StratStopHeader methods . The default is \'\\\\n'.
:type end: str, optional

:param file: Specifies the argument to use on the print statement
    *file* parameter for the start time and end time messages issued by
    the StratStopHeader methods . The default is
    sys.stdout (via None).
:type file: Optional[Any]

:param flush: Specifies the argument to use on the print statement
    *flush* parameterfor the start time and end time messages issued by
    the StratStopHeader methods . The default is False.
:type flush: bool, optional

:param time_box_enabled: Specifies whether the start and end messages
    should be issued (True) or not (False). The default is True.
:type time_box_enabled: Union[bool, Callable[..., bool]], optional

:returns: A callable function that issues a starting time message, calls
    the wrapped function, issues the ending time message, and finally
    returns the return value from the wrapped function, if one.
:rtype: Callable[..., Any]



:Example: printing to stderr

note: the examples only show the output going to stdout



>>> from sbt_utils.time_hdr import time_box
>>> import sys

>>> @time_box(file=sys.stderr)
... def aFunc3() -> None:
...      print('this text printed to stdout, not stderr')

>>> aFunc3()
this text printed to stdout, not stderr


:Example: statically wrapping function with time_box

>>> from sbt_utils.time_hdr import time_box

>>> _tbe = False

>>> @time_box(time_box_enabled=_tbe)
... def aFunc4a() -> None:
...      print('this is sample text for _tbe = False static example')

>>> aFunc4a()  # aFunc4a is not wrapped by time box
this is sample text for _tbe = False static example

>>> _tbe = True

>>> @time_box(time_box_enabled=_tbe)
... def aFunc4b() -> None:
...      print('this is sample text for _tbe = True static example')

>>> aFunc4b()  # aFunc4b is wrapped by time box
<BLANKLINE>
************************************************
* Starting aFunc4b on Mon Jun 29 2020 18:22:51 *
************************************************
this is sample text for _tbe = True static example
<BLANKLINE>
**********************************************
* Ending aFunc4b on Mon Jun 29 2020 18:22:51 *
* Elapsed time: 0:00:00.000133               *
**********************************************


:Example: dynamically wrapping function with time_box:

>>> from sbt_utils.time_hdr import time_box

>>> _tbe = True
>>> def tbe() -> bool: return _tbe

>>> @time_box(time_box_enabled=tbe)
... def aFunc5() -> None:
...      print('this is sample text for the tbe dynamic example')

>>> aFunc5()  # aFunc5 is wrapped by time box
<BLANKLINE>
***********************************************
* Starting aFunc5 on Mon Jun 29 2020 18:22:51 *
***********************************************
this is sample text for the tbe dynamic example
<BLANKLINE>
*********************************************
* Ending aFunc5 on Mon Jun 29 2020 18:22:51 *
* Elapsed time: 0:00:00.000130              *
*********************************************

>>> _tbe = False
>>> aFunc5()  # aFunc5 is not wrapped by time_box
this is sample text for the tbe dynamic example


:Example: specifying a datetime format:

>>> from sbt_utils.time_hdr import time_box

>>> aDatetime_format: DT_Format = '%m/%d/%y %H:%M:%S'
>>> @time_box(dt_format=aDatetime_format)
... def aFunc6() -> None:
...     print('this is sample text for the datetime format example')

>>> aFunc6()
<BLANKLINE>
****************************************
* Starting aFunc6 on 06/30/20 17:07:48 *
****************************************
this is sample text for the datetime format example
<BLANKLINE>
**************************************
* Ending aFunc6 on 06/30/20 17:07:48 *
* Elapsed time: 0:00:00.000073       *
**************************************

    """

    from sbt_utils.time_hdr import StartStopHeader as StartStopHeader

    # ========================================================================
    #  The following code covers cases where time_box is used with or without
    #  parameters, and where the decorated function has or does not have
    #
    #     parameters.
    #
    #     Here's an example of time_box without args:
    #         @time_box
    #         def aFunc():
    #             print('42')
    #
    #     This is what essentially happens under the covers:
    #         def aFunc():
    #             print('42')
    #         aFunc = time_box(aFunc)
    #
    #     In fact, the above direct call can be coded as shown without using
    #     the pie style.
    #
    #     Here's an example of time_box with args:
    #         @time_box(end='\n\n')
    #         def aFunc():
    #             print('42')
    #
    #     This is what essentially happens under the covers:
    #         def aFunc():
    #             print('42')
    #         aFunc = time_box(end='\n\n')(aFunc)
    #
    #     Note that this is a bit more tricky: time_box(end='\n\n') portion
    #     results in a function being returned that takes as its first
    #     argument the separate aFunc specification in parens that we see at
    #     the end of the first portion.
    #
    #     Note that we can also code the above as shown and get the same
    #     result.
    #
    #     Also, we can code the following and get the same result:
    #         def aFunc():
    #             print('42')
    #         aFunc = time_box(aFunc, end='\n\n')
    #
    #     What happens in the tricky case is time_box gets control and tests
    #     whether aFunc was specified, and if not returns a call to
    #     functools.partial which is the function that accepts the aFunc
    #     specification and then calls time_box with aFunc as the first
    #     agument with the end='\n\n' as the second argument as we now have
    #     something that time_box can decorate.
    #
    #     One other complication is that we are also using the wrapt.decorator
    #     for the inner wrapper function which does some more smoke and
    #     mirrors to ensure the introspection will work as expected.
    # ========================================================================
# ============================================================================
#  This is the what appears in stderr:
#
#  ***********************************************
#  * Starting aFunc3 on Mon Jun 29 2020 18:22:51 *
#  ***********************************************
#  this text printed to stdout, not stderr

#  *********************************************
#  * Ending aFunc3 on Mon Jun 29 2020 18:22:51 *
#  * Elapsed time: 0:00:00.000131              *
#  *********************************************
# ============================================================================
    # ========================================================================
    #  note: the following code that sets file to sys.stdout is needed to
    #  allow the test cases to use the pytest capsys built-in fixture.
    #  Having sys.stdout as the default parameter in the function
    #  definition does not work because capsys changes sys.stdout after
    #  the test case gets control, meaning the print statements in
    #  time_box code are not captured. This is also appears to be
    #  the case for doctest. So, we simply use None as the default and set
    #  file to sys.stdout here below which works fine.
    # ========================================================================

    if file is None:
        file = sys.stdout

    if wrapped is None:
        return cast(F, functools.partial(time_box, dt_format=dt_format,
                    end=end, file=file, flush=flush,
                    time_box_enabled=time_box_enabled))

    @decorator(enabled=time_box_enabled)
    def wrapper(wrapped: F, instance: Optional[Any],
                args: Tuple[Any, ...],
                kwargs: Dict[str, Any]) -> Any:
        header = StartStopHeader(wrapped.__name__)
        header.print_start_msg(dt_format=dt_format,
                               end=end, file=file, flush=flush)
        ret_value = wrapped(*args, **kwargs)

        header.print_end_msg(dt_format=dt_format,
                             end=end, file=file, flush=flush)

        return ret_value
    return cast(F, wrapper(wrapped))
