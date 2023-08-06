.. pinspect.rst
.. Copyright (c) 2013-2019 Pablo Acosta-Serafini
.. See LICENSE for details
.. py:module:: pexdoc.pinspect

###############
pinspect module
###############

This module supplements Python's introspection capabilities. The
class :py:class:`pexdoc.pinspect.Callables` "traces" modules and produces a
database of callables (functions, classes, methods and class properties)
and their attributes (callable type, file name, starting line number).
Enclosed functions and classes are supported. For example:

.. literalinclude:: ./support/pinspect_example_1.py
    :language: python
    :tab-width: 4
    :lines: 1,6-

with

.. literalinclude:: ./support/python2_module.py
    :language: python
    :tab-width: 4
    :lines: 1,6-

and

.. literalinclude:: ./support/python3_module.py
    :language: python
    :tab-width: 4
    :lines: 1,6-

gives:

.. code-block:: python

	>>> from __future__ import print_function
	>>> import docs.support.pinspect_example_1, pexdoc.pinspect, sys
	>>> cobj = pexdoc.pinspect.Callables(
	...     [sys.modules['docs.support.pinspect_example_1'].__file__]
	... )
	>>> print(cobj)
	Modules:
	   docs.support.pinspect_example_1
	Classes:
	   docs.support.pinspect_example_1.my_func.MyClass
	docs.support.pinspect_example_1.my_func: func (10-29)
	docs.support.pinspect_example_1.my_func.MyClass: class (13-29)
	docs.support.pinspect_example_1.my_func.MyClass.__init__: meth (21-23)
	docs.support.pinspect_example_1.my_func.MyClass._get_value: meth (24-26)
	docs.support.pinspect_example_1.my_func.MyClass.value: prop (27-29)
	docs.support.pinspect_example_1.print_name: func (30-31)

The numbers in parenthesis indicate the line number in which the callable
starts and ends within the file it is defined in.

*********
Functions
*********

.. autofunction:: pexdoc.pinspect.get_function_args
.. autofunction:: pexdoc.pinspect.get_module_name
.. autofunction:: pexdoc.pinspect.is_object_module
.. autofunction:: pexdoc.pinspect.is_special_method
.. autofunction:: pexdoc.pinspect.private_props

*******
Classes
*******

.. autoclass:: pexdoc.pinspect.Callables
	:members: load, refresh, save, trace, callables_db,
                  reverse_callables_db, __add__, __copy__,
                  __eq__, __iadd__, __nonzero__, __repr__, __str__
	:show-inheritance:
