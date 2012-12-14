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

  def test_access_value(self):
    ret = safe_access(path='a.b["abc"][1]',  base_obj=self.a, default_value=7)
    self.assertEquals('y', ret)

  def test_default_value_works(self):
    ret = safe_access(path='a.b["abc"][404]',  base_obj=self.a, default_value=7)
    self.assertEquals(7, ret)

  def test_access_non_existant_attribute(self):
    ret = safe_access(path='a.bad_attribute',  base_obj=self.a)
    self.assertEquals(None, ret)

if __name__ == '__main__':
  unittest.main()
