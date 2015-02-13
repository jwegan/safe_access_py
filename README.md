Safe Access
==============

Tired of always checking hasattr, len, or if a key is in a dictionary? safe_access allows
you to safely drill down multiple levels into any python object without having to worry about
AttributeErrors, KeyErrors, or IndexErrors. Oh, and it supports wildcards.

Limitations:

1) Does not support function calls at this time
2) Does not support escaped quotations
3) Does not support variable references withing tuple literals


```python
import safe_access
class A(object):
  pass

a = A()
a.b = {"abc": ['x', 'y', 'z'], "def": [1, 2, 3]}

# Access valid path
print safe_access(a, 'a.b["abc"][1]', default_value=7)
# returns 'y'

# Access valid path with variable substitution
myvar = 1
print safe_access(a, 'a.b["abc"][myvar]', default_value=7, myvar=myvar)
# returns 'y'

# Access that causes index out of range, but returns default value of 7
print safe_access(a, 'a.b["abc"][404]', default_value=7)
# returns 7

# Access non-existant attribute
print safe_access(a, 'a.bad_attribute')
# returns None

# Access wildcard
print safe_access(a, 'a.b[*][0]')
# returns ['x', 1]
```
