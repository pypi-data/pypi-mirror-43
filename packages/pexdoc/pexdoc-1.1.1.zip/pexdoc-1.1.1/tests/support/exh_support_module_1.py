# exh_support_module_1.py
# Copyright (c) 2013-2019 Pablo Acosta-Serafini
# See LICENSE for details
# pylint: disable=C0111,W0612

import pexdoc.exh


###
# Module functions
###
def mydecorator(func):  # noqa: D401
    """Dummy decorator."""
    return func


@mydecorator
def func16(exobj):
    exobj.add_exception("total_exception_16", TypeError, "Total exception #16")


def simple_exception():
    exobj = pexdoc.exh.get_exh_obj()
    exobj.add_exception("total_exception_16", TypeError, "Total exception #16")
