# coding: utf8
from __future__ import unicode_literals, print_function, division


def test_Pager():
    from clld.web.util.pager import Pager

    pager = Pager(None, range(100), page=4, url_maker=lambda p: 'page %s' % p)
    assert pager.render()
