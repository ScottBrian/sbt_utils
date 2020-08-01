=========
sbt-utils
=========

With **@time_box**, you can decorate a function to be sandwiched between start
time and end time messages like this:

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

.. image:: https://img.shields.io/badge/security-bandit-yellow.svg
    :target: https://github.com/PyCQA/bandit
    :alt: Security Status

.. image:: https://readthedocs.org/projects/pip/badge/?version=stable
    :target: https://pip.pypa.io/en/stable/?badge=stable
    :alt: Documentation Status


The flower_box.py module contains:

1. print_flower_boxmsg function - takes one of more lines of text as input
   and prints them inside a flower box (asterisks) as a visual aid for finding
   the text on the console or in a log.
   
The time_hdr.py module contains:

1. StartStopHeader class - has two functions that will repectively print
   a starting time message in a flower box, and an ending time and elapsed
   wall clock time message in a flower box.
2. time_box decorator - wraps a function and uses the StartStopHeader to
   print the starting and ending time headers.





Installation
============

Linux:

``pip install sbt_utils``


Usage examples:
===============

flower_box example
------------------

print a single line message in a flower box
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

>>> from sbt_utils.flower_box import print_flower_box_msg
>>> print_flower_box_msg('This is my test message')
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

* 1.0.0
    * Initial release

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


