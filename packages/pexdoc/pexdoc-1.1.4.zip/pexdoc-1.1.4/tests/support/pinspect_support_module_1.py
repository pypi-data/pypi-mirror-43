# pinspect_support_module_1.py
# Copyright (c) 2013-2019 Pablo Acosta-Serafini
# See LICENSE for details
# pylint: disable=C0103,C0111,C0411,C0412,C0413,R0201,R0205,R0903,W0212,W0621

from __future__ import print_function
import sys
import pexdoc.exh
import pexdoc.pcontracts
import tests.support.pinspect_support_module_2


def module_enclosing_func(offset):  # noqa: D202
    """Test function to see if module-level enclosures are detected."""

    def module_closure_func(value):
        """Actual closure function."""
        return offset + value

    return module_closure_func


def class_enclosing_func():
    """Test function to see if classes within enclosures are detected."""
    import tests.support.pinspect_support_module_3

    class ClosureClass(object):
        """Actual closure class."""

        def __init__(self):  # noqa: D401
            """Constructor method."""
            self.obj = None

        def get_obj(self):
            """Getter method."""
            return self.obj

        def set_obj(self, obj):
            """Setter method."""
            self.obj = obj

        def sub_enclosure_method(self):  # noqa: D202
            """Test method to see if class of classes are detected."""

            class SubClosureClass(object):
                """Actual sub-closure class."""

                def __init__(self):  # noqa: D401
                    """Constructor method."""
                    self.subobj = None

            return SubClosureClass

        mobj = sys.modules["tests.support.pinspect_support_module_2"]
        obj = property(
            mobj.getter_func_for_closure_class,
            set_obj,
            tests.support.pinspect_support_module_3.deleter,
        )

    return ClosureClass


class ClassWithPropertyDefinedViaLambdaAndEnclosure(object):
    """Class with lambda for property function and enclosed function to define prop."""

    def __init__(self):  # noqa: D107
        self._clsvar = None

    clsvar = property(
        lambda self: self._clsvar + 10,
        tests.support.pinspect_support_module_2.setter_enclosing_func(5),
        doc="Class variable property",
    )


def dummy_decorator(func):  # noqa: D401
    """Dummy property decorator, to test if chained decorators are handled correctly."""
    return func


def simple_property_generator():  # noqa: D401,D202
    """Function to test if properties done via enclosed functions properly detected."""

    def fget(self):
        """Actual getter function."""
        return self._value

    return property(fget)


class ClassWithPropertyDefinedViaFunction(object):
    """Class to test if properties defined via property function handled correctly."""

    def __init__(self):  # noqa: D107
        self._state = None

    @pexdoc.pcontracts.contract(state=int)
    @dummy_decorator
    def _setter_func(self, state):
        """Setter method with property defined via property() function."""
        exobj = (
            pexdoc.exh.get_exh_obj()
            if pexdoc.exh.get_exh_obj()
            else pexdoc.exh.ExHandle()
        )
        exobj.add_exception(
            exname="dummy_exception_1", extype=ValueError, exmsg="Dummy message 1"
        )
        exobj.add_exception(
            exname="dummy_exception_2", extype=TypeError, exmsg="Dummy message 2"
        )
        self._state = state

    def _getter_func(self):
        """Getter method with property defined via property() function."""
        return self._state

    def _deleter_func(self):  # noqa: D401
        """Deleter method with property defined via property() function."""
        print("Cannot delete attribute")

    state = property(_getter_func, _setter_func, _deleter_func, doc="State attribute")


import math


class ClassWithPropertyDefinedViaDecorators(object):
    """Class to test if properties defined via decorator functions handled correctly."""

    def __init__(self):  # noqa: D107
        self._value = None

    def __call__(self):  # noqa: D102
        self._value = 2 * self._value if self._value else self._value

    @property
    def temp(self):
        """Getter method defined with decorator."""
        return math.sqrt(self._value)

    @temp.setter
    @pexdoc.pcontracts.contract(value=int)
    def temp(self, value):
        """Setter method defined with decorator."""
        self._value = value

    @temp.deleter
    def temp(self):  # noqa: D401
        """Deleter method defined with decorator."""
        print("Cannot delete attribute")

    encprop = simple_property_generator()


import tests.support.pinspect_support_module_4


def class_namespace_test_enclosing_func():
    """Test namespace support for enclosed class properties."""
    # pylint: disable=C0301

    class NamespaceTestClosureClass(object):  # noqa: D200,D210,D400
        r""" Actual class
        """  # This is to test a comment after a multi-line docstring

        def __init__(self, value):
            _, _, _ = (5, 3, 7)

            self._value = value

        nameprop = (
            tests.support.pinspect_support_module_4.another_property_action_enclosing_function()
        )

    return NamespaceTestClosureClass
