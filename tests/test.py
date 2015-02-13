#!/usr/bin/env python
#
# Copyright (c) 2012-2015, John Egan
# All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# ---
# Author: John Egan <me@jwegan.com>

import unittest

from safe_access import safe_access


class SafeAccessTestCase(unittest.TestCase):

    def setUp(self):
        super(SafeAccessTestCase, self).setUp()

        class A(object):
            pass

        self.a = A()
        self.a.b = dict()
        self.a.b["abc"] = ['x', 'y', 'z']
        a2 = A()
        a2.val = 99
        self.a.b["['.']"] = a2

    def test_access_value(self):
        ret = safe_access(base_obj=self.a, path='a.b["abc"][1]', default_value=7)
        self.assertEquals('y', ret)

    def test_key_with_control_characters(self):
        ret = safe_access(base_obj=self.a, path="""a.b["['.']"].val""")
        self.assertEquals(99, ret)

    def test_default_value_works(self):
        ret = safe_access(base_obj=self.a, path='a.b["abc"][404]', default_value=7)
        self.assertEquals(7, ret)

    def test_access_non_existant_attribute(self):
        ret = safe_access(base_obj=self.a, path='a.bad_attribute')
        self.assertEquals(None, ret)

    def test_variable_substitution(self):
        myvar = "abc"
        ret = safe_access(base_obj=self.a, path='a.b[myvar][1]', default_value=7, myvar=myvar)
        self.assertEquals('y', ret)

    def test_wildcard_on_dict(self):
        self.a.b["def"] = dict()
        ret = safe_access(base_obj=self.a, path='a.b[*][1]')
        self.assertEquals(['y'], ret)

    def test_wildcard_on_attribute(self):
        class B(object):
            pass

        self.a.x = B()
        self.a.x.y = 5
        ret = safe_access(base_obj=self.a, path='a.*.y')
        self.assertEquals([5], ret)

    def test_wildcard_on_multiple_values(self):
        self.a.b["def"] = ['a', 'b', 'c']
        ret = safe_access(base_obj=self.a, path='a.b[*][1]')
        self.assertEquals(set(['y', 'b']), set(ret))

    def test_wildcard_at_the_end_of_path(self):
        ret = safe_access(base_obj=self.a, path='a.b["abc"][*]')
        self.assertEquals(set(['x', 'y', 'z']), set(ret))


if __name__ == '__main__':
    unittest.main()
