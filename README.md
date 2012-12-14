safe_access_py
==============

Tired of always checking hasattr, len, or if a key is in a dictionary? Safe access allows
you to safely drill down multiple levels into any python object without having to worry about
AttributeErrors, KeyErrors, or IndexErrors.

Limitations:

1) Does not support function calls at this time


```python
from safe_access import safe_access
class A(object):
  pass

a = A()
a.b = dict()
a.b["abc"] = ['x', 'y', 'z']

# Access valid path
print safe_access(base_obj=a, path='a.b["abc"][1]', default_value=7)
# returns 'y'

# Access valid path with variable substitution
myvar = 1
print safe_access(base_obj=a, path='a.b["abc"][myvar]', default_value=7, myvar=myvar)
# returns 'y'

# Access that causes index out of range, but returns default value of 7
print safe_access(base_obj=a, path='a.b["abc"][404]', default_value=7)
# returns 7

# Access non-existant attribute
print safe_access(base_obj=a, path='a.bad_attribute')
# returns None
```
