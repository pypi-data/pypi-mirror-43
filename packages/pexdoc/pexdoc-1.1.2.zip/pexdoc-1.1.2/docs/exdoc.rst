.. exdoc.rst
.. Copyright (c) 2013-2019 Pablo Acosta-Serafini
.. See LICENSE for details
.. py:module:: pexdoc.exdoc

.. _reStructuredText: http://docutils.sourceforge.net/rst.html

############
exdoc module
############

This module can be used to automatically generate exceptions documentation
marked up in `reStructuredText <http://docutils.sourceforge.net/rst.html>`_
with help from `cog <https://nedbatchelder.com/code/cog>`_ and the
:py:mod:`pexdoc.exh` module.

The exceptions to auto-document need to be defined with either the
:py:meth:`pexdoc.exh.ExHandle.addex` function, the
:py:meth:`pexdoc.exh.ExHandle.addai` function or via contracts of the
:py:mod:`pexdoc.pcontracts` module, and "traced" before the documentation is
generated. In general tracing consists of calling the methods, functions and/or
class properties so that all the required exceptions are covered (exceptions
raised by contracts are automatically traced when the functions with the
contracts are used). A convenient way of tracing a module is to simply run its
test suite, provided that it covers the exceptions that need to be documented
(for maximum speed the unit tests that cover the exceptions may be segregated
so that only these tests need to be executed).

For example, it is desired to auto-document the exceptions of a module
``my_module.py``, which has tests in ``test_my_module.py``. Then a tracing
module ``trace_my_module.py`` can be created to leverage the already written
tests:

.. literalinclude:: ./support/trace_my_module_1.py
    :language: python
    :tab-width: 4
    :lines: 1,7,10-

The context manager :py:class:`pexdoc.exdoc.ExDocCxt` sets up the tracing
environment and returns a :py:class:`pexdoc.exdoc.ExDoc` object that can the be
used in the documentation string of each callable to extract the exceptions
documentation. In this example it is assumed that the tests are written using
`pytest <http://pytest.org/>`_, but any test framework can be used. Another way
to trace the module is to simply call all the functions, methods or class
properties that need to be documented. For example:

.. literalinclude:: ./support/trace_my_module_2.py
    :language: python
    :tab-width: 4
    :lines: 1,7,10-

And the actual module ``my_module`` code is (before auto-documentation):

.. literalinclude:: ./support/my_module.py
    :language: python
    :tab-width: 4
    :lines: 1-12,16-

A simple shell script can be written to automate the cogging of the
``my_module.py`` file:

.. literalinclude:: ./support/build-docs.sh
    :language: bash
    :tab-width: 4
    :lines: 1,6-

After the script is run and the auto-documentation generated, each callable has
a `reStructuredText`_ marked-up ``:raises:`` section:

.. literalinclude:: ./support/my_module_ref.py
    :language: python
    :tab-width: 4
    :lines: 1-12,16-

.. warning:: Due to the limited introspection capabilities of class properties,
	     only properties defined using the `property
	     <https://docs.python.org/2/library/functions.html#property>`_
             built-in function can be documented with
             :py:meth:`pexdoc.exdoc.ExDoc.get_sphinx_autodoc`. Properties
             defined by other methods can still be auto-documented with
	     :py:meth:`pexdoc.exdoc.ExDoc.get_sphinx_doc` and explicitly
             providing the method/function name.

****************
Context managers
****************

.. autoclass:: pexdoc.exdoc.ExDocCxt
        :show-inheritance:

*******
Classes
*******

.. autoclass:: pexdoc.exdoc.ExDoc
    :members: get_sphinx_autodoc, get_sphinx_doc, depth, exclude
    :show-inheritance:
