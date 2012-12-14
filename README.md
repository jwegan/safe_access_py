safe_access_py
==============

Drill down into any python object without having to worry about AttributeErrors, KeyErrors, or IndexErrors

```python
from safe_access import safe_access
class A(object):
  pass

a = A()
a.b = dict()
a.b["abc"] = ['x', 'y', 'z']

# Access valid path
print safe_access(path='a.b["abc"][1]',  base_obj=a, default_value=7)
# returns 'y'

# Access that causes index out of range, but returns default value of 7
print safe_access(path='a.b["abc"][404]',  base_obj=a, default_value=7)
# returns 7

# Access non-existant attribute
print safe_access(path='a.bad_attribute',  base_obj=a)
# returns None
```
