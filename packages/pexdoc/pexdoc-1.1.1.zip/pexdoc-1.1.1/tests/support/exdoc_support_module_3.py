# exdoc_support_module_3.py
# Copyright (c) 2013-2019 Pablo Acosta-Serafini
# See LICENSE for details
# pylint: disable=C0111,R0205,R0903,W0212

import pexdoc.exh


def simple_property_generator():  # noqa: D202
    """Test if properties done via enclosed functions are properly detected."""

    def fget(self):
        """Actual getter function."""
        self._exobj.add_exception(
            exname="illegal_value", extype=TypeError, exmsg="Cannot get value"
        )
        return self._value

    return property(fget)


class Class1(object):
    """First (of 2) class that has a property action function defined by a factory."""

    def __init__(self):  # noqa
        self._exobj = (
            pexdoc.exh.get_exh_obj()
            if pexdoc.exh.get_exh_obj()
            else pexdoc.exh.ExHandle()
        )
        self._value = None

    value1 = simple_property_generator()


class Class2(object):
    """Second (of 2) class that has a property action function defined by a factory."""

    def __init__(self):  # noqa
        self._exobj = (
            pexdoc.exh.get_exh_obj()
            if pexdoc.exh.get_exh_obj()
            else pexdoc.exh.ExHandle()
        )
        self._value = None

    value2 = simple_property_generator()
