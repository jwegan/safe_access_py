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

if __name__ == '__main__':
  unittest.main()
