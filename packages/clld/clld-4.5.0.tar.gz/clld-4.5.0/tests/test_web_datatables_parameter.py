# coding: utf8
from __future__ import unicode_literals, print_function, division, absolute_import

from clld.db.models import common

from testutils import handle_dt


def test_Parameters(env):
    from clld.web.datatables.parameter import Parameters

    handle_dt(env['request'], Parameters, common.Parameter)
