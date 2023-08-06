"""
Test module.

[[[cog
import os, sys
sys.path.append(os.environ['TRACER_DIR'])
import trace_my_module_1
exobj = trace_my_module_1.trace_module(no_print=True)
]]]
[[[end]]]
"""
# my_module.py
# Copyright (c) 2013-2019 Pablo Acosta-Serafini
# See LICENSE for details
# pylint: disable=C0111,R0205,R0903,W0105

import pexdoc


def func(name):
    r"""
    Print your name.

    :param name: Name to print
    :type  name: string

    .. [[[cog cog.out(exobj.get_sphinx_autodoc(width=69))]]]
    .. [[[end]]]

    """
    # Raise condition evaluated in same call as exception addition
    pexdoc.addex(TypeError, "Argument `name` is not valid", not isinstance(name, str))
    return "My name is {0}".format(name)


class MyClass(object):
    """Store a value."""

    def __init__(self, value=None):  # noqa
        self._value = None if not value else value

    def _get_value(self):
        # Raise condition not evaluated in same call as
        # exception additions
        exobj = pexdoc.addex(RuntimeError, "Attribute `value` not set")
        exobj(not self._value)
        return self._value

    def _set_value(self, value):
        exobj = pexdoc.addex(RuntimeError, "Argument `value` is not valid")
        exobj(not isinstance(value, int))
        self._value = value

    value = property(_get_value, _set_value)
    r"""
    Set or return a value

    :type:  integer
    :rtype: integer or None

    .. [[[cog cog.out(exobj.get_sphinx_autodoc(width=69))]]]
    .. [[[end]]]
    """
