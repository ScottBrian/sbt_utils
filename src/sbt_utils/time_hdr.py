#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Created on Wed Apr 22 15:09:41 2020

@author: Scott Tuttle

The time_hdr module contains two items:
1) a StartStopHeader class with two functions that will repectively print a
   a starting time messge and an ending time and elapsed wall clock time
   message in a flower box (see flower_box module in sbt_utils package).
2) a time_box decorator that wraps a function and uses the StartStopHeader to
   print the starting and ending time headers.


Example for StartStopHeader

Notes:
    1)the example output shows elipses for where the date or elapsed time will
      appear in order to allow the doctest to succeed. The actual output will
      show a date (and elapsed time for the end message) such as in the
      following:
***********************************************
* Starting aFunc1 on Tue Apr 14 2020 18:59:43 *
***********************************************

    2) the examples show file=sys.stdout being specified even though that is
       the default. This is done to allow doctest to succeed.

>>> from sbt_utils.time_hdr import StartStopHeader
>>> import time
>>> import sys

>>> def aFunc1():
...      print('2 + 2 =', 2+2)
...      time.sleep(2)

>>> hdr = StartStopHeader('aFunc1')
>>> hdr.print_start_msg(file=sys.stdout)
<BLANKLINE>
***********************************************
* Starting aFunc1 on ...
***********************************************
>>> aFunc1()
2 + 2 = 4
>>> hdr.print_end_msg(file=sys.stdout)
<BLANKLINE>
*********************************************
* Ending aFunc1 on ...
* Elapsed time: ...
*********************************************


Example for time_box decorator:

>>> from sbt_utils.time_hdr import time_box
>>> import time
>>> import sys

>>> @time_box(file=sys.stdout)
... def aFunc2():
...      print('2 * 3 =', 2*3)
...      time.sleep(1)

>>> aFunc2()
<BLANKLINE>
***********************************************
* Starting aFunc2 on ...
***********************************************
2 * 3 = 6
<BLANKLINE>
*********************************************
* Ending aFunc2 on ...
* Elapsed time: ...
*********************************************

time_box accepts optional parameters:
    end - default is '\n' - propagated to the print statements
    file - default is sys.stdout - propagated to the print statemnents
    flush - default is False - propagated to the print statements
    time_box_enabed - default True - when True, return the wrapped function,
                                     when False, return the function unwrapped

Example of printing to stderr:

note: the examples only show the output going to stdout

>>> from sbt_utils.time_hdr import time_box
>>> import sys
>>> @time_box(file=sys.stderr)
... def func1():
...      print('this text printed to stdout, not stderr')

>>> func1()
this text printed to stdout, not stderr

Example of statically wrapping function with time_box:
>>> _tbe = False
>>> @time_box(time_box_enabled = _tbe, file=sys.stdout)
... def func1():
...      print('this is sample text for _tbe = False static example')

>>> func1() # func1 is not wrapped by time box
this is sample text for _tbe = False static example

>>> _tbe = True
>>> @time_box(time_box_enabled = _tbe, file=sys.stdout)
... def func1():
...      print('this is sample text for _tbe = True static example')

>>> func1() # func1 is wrapped by time box
<BLANKLINE>
**********************************************
* Starting func1 on ...
**********************************************
this is sample text for _tbe = True static example
<BLANKLINE>
********************************************
* Ending func1 on ...
* Elapsed time: ...
********************************************

Example of dynamically wrapping function with time_box:
>>> _tbe = True
>>> def tbe(): return _tbe
>>> @time_box(time_box_enabled = tbe, file=sys.stdout)
... def func3():
...      print('this is sample text for the tbe dynamic example')

>>> func3() # func1 is wrapped by time box
<BLANKLINE>
**********************************************
* Starting func3 on ...
**********************************************
this is sample text for the tbe dynamic example
<BLANKLINE>
********************************************
* Ending func3 on ...
* Elapsed time: ...
********************************************

>>> _tbe = False
>>> func3() # func3 is not wrapped by time_box
this is sample text for the tbe dynamic example


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
       1. a place to store the start time and end time
       2. method print_start_msg to print the start header with the start time
       3. method print_end_msg to print the end trailer with end time and
          elapsed time
    """
    default_dt_format: DT_Format = DT_Format('%a %b %d %Y %H:%M:%S')

    def __init__(self, func_name: str) -> None:
        """Stores the input func_name and sets the start and end times to None

        :param func_name : The name of the function to appear in the start and
            stop messages
        :type func_name: str

        :returns: None
        :rtype: None
        """

        self.func_name = func_name
        self.start_DT: datetime = datetime.max
        self.end_DT: datetime = datetime.min

    def print_start_msg(self, dt_format: DT_Format = default_dt_format,
                        end: str = '\n', file: Any = sys.stdout,
                        flush: bool = False) -> None:
        self.start_DT = datetime.now()
        file_text = ''
        # if file == sys.stderr:
        #     file_text = 'stderr '
        # elif file == sys.stdout:
        #     file_text = 'stdout '
        # else:
        #     file_text = 'unknown '
        msg = 'Starting ' + file_text + self.func_name + ' on '\
            + self.start_DT.strftime(dt_format)
        print_flower_box_msg([msg], end=end, file=file, flush=flush)

    def print_end_msg(self, dt_format: DT_Format = default_dt_format,
                      end: str = '\n', file: Any = sys.stdout,
                      flush: bool = False) -> None:
        self.end_DT = datetime.now()
        msg1 = 'Ending ' + self.func_name + ' on '\
            + self.end_DT.strftime(dt_format)
        msg2 = 'Elapsed time: ' + str(self.end_DT - self.start_DT)
        print_flower_box_msg([msg1, msg2], end=end, file=file,
                             flush=flush)


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
    """ This is the main decorator function that can handle being called with
    or without the function name to be decorated, and with or without
    arguments for the other optional parameters. This is a tricky interface
    that involves some smoke and mirrors with the pie decorator syntactic
    sugar style invocation. Following are the parameters, and after that some
    examples of how this can be invoked with the various flavors.

    :param wrapped : positional, optional name of the function to wrap or
                      None
    :param dt_format : optional keyword specifies the display format for the
                        start and end datetime
    :param end : optional keyword species the end argument for the print
                  statements
    :param file : optional keyword specifies the file argument for the print
                  statements
    :param flush : optional keyword specifies the flush argument for the
                    print statements
    :param time_box_enabled : optional keyword specifies whether to wrap
                              (True) or not wrap (False) the funtion
    :returns: callable, either wrapper or wrapper(wrapped)

    The following code covers cases where time_box is used with or without
    parameters, and where the decorated function has or does not have
    parameters.

    Here's an example of time_box without args:
        @time_box
        def aFunc():
            print('42')

    This is what essentially happens under the covers:
        def aFunc():
            print('42')
        aFunc = time_box(aFunc)

    In fact, the above direct call can be coded as shown without using the
    pie style.

    Here's an example of time_box with args:
        @time_box(end='\n\n')
        def aFunc():
            print('42')

    This is what essentially happens under the covers:
        def aFunc():
            print('42')
        aFunc = time_box(end='\n\n')(aFunc)

    Note that this is a bit more tricky: time_box(end='\n\n') portion results
    in a function being returned that takes as its first argument the separate
    aFunc specification in parens that we see at the end of the first portion.
    Note that we can also code the above as shown and get the same result.
    Also, we can code the following and get the same result:
        def aFunc():
            print('42')
        aFunc = time_box(aFunc, end='\n\n')

    What happens in the tricky case is time_box gets control and tests
    whether aFunc was specified, and if not returns a call to
    functools.partial which is the function that accepts the aFunc
    specification and then calls time_box with aFunc as the first agument
    with the end='\n\n' as the second argument as we now have something
    that time_box can decorate.

    One other complication is that we are also using the wrapt.decorator
    for the inner wrapper function which does some more smoke and mirrors to
    ensure the introspection will work as expected.
    """

    from sbt_utils.time_hdr import StartStopHeader as StartStopHeader

    """the following code that sets file to sys.stdout is needed to allow the
    test cases to use the pytest capsys built-in fixture. Having sys.stdout
    as the default parameter in the function definition does not work
    because capsys changes sys.stdout after the test case gets control,
    meaning the print statements in StartStopHeader code are not captured.
    So, we simply use None as the default and set file to sys.stdout here
    which works fine.
    """
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
