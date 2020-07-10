=========
sbt-utils
=========

The sbt-utils package contains a function wrapper that will print the start
time in a header flower box, invoke the function, and then print the stop time
and elapsed time in a trailing flower box.

>>> aFunc2()
***********************************************
* Starting aFunc2 on Tue May 12 2020 20:35:06 *
***********************************************
2 * 3 = 6
*********************************************
* Ending aFunc2 on Tue May 12 2020 20:35:07 *
* Elapsed time: 0:00:01.000196              *
*********************************************

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

.. image:: https://img.shields.io/badge/security-bandit-yellow.svg
    :target: https://github.com/PyCQA/bandit
    :alt: Security Status


The flower_box.py module contains one importable item:

1. print_flower_boxmsg function - takes one of more lines of text as input
   and prints them inside a flower box (asterisks) as a visual aid for finding
   the text on the console or in a log.
   
The time_hdr.py module contains two importable items:

1. StartStopHeader class - has two functions that will repectively print
   a starting time message in a flower box, and an ending time and elapsed
   wall clock time message in a flower box.
2. time_box decorator - wraps a function and uses the StartStopHeader to
   print the starting and ending time headers.





Installation
============

The sbt-utils project will hopefully be placed in pypi in the near future

Linux:

``pip install sbt-utils``


Usage examples:
===============

flower_box example
------------------

print a single line message in a flower box
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

>>> from sbt_utils.flower_box import print_flower_box_msg
>>> msg_list = ['This is my test message']
>>> print_flower_box_msg(msg_list)
***************************
* This is my test message *
***************************

print a two line message in a flower box
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

>>> from sbt_utils.flower_box import print_flower_box_msg
>>> msg_list = ['This is my first line test message', '   and my second line']
>>> print_flower_box_msg(msg_list)
**************************************
* This is my first line test message *
*    and my second line              *
**************************************

time_box decorator example:
---------------------------

wrap a function with time_box
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

>>> from sbt_utils.time_hdr import time_box
>>> import time

>>> @time_box
... def aFunc2():
...      print('2 * 3 =', 2*3)
...      time.sleep(1)

>>> aFunc2()
***********************************************
* Starting aFunc2 on Tue May 12 2020 20:35:06 *
***********************************************
2 * 3 = 6
*********************************************
* Ending aFunc2 on Tue May 12 2020 20:35:07 *
* Elapsed time: 0:00:01.000196              *
*********************************************

Development setup
=================

See tox.ini

Release History
===============

* 0.0.1
    * Work in progress

Meta
====

Scott Tuttle

Distributed under the MIT license. See ``LICENSE`` for more information.


Contributing
============

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request


