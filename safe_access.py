import ast


def safe_access(base_obj, path, default_value=None, **kwargs):
  """Drill down into an object without having to worry about AttributeErrors,
  KeyErrors, or IndexErrors.

  Keywords arguments:
  base_obj -- the base object from which to start drilling down. From the example above,
              this would be a.
  path -- a string representing the python expression to access the value you want.
          ex: "a.b[12]["dict_key"].value_i_want"
  default_value -- the value to return if the path could not be fully traversed
  **kwargs -- variables used as dictionary keys or list indexes in the path expression.
              ex: myvar would need to be in kwargs if you use path="a.b.[myvar]"
  """

  # Strip variable name of base_obj from path
  _, remaining_path = _pop_from_path(path)
  cur_obj = base_obj

  while remaining_path:
    part, remaining_path = _pop_from_path(remaining_path)

    if part[0] == '[' and part[len(part) - 1] == ']':
      # Determine if key/index is a variable or a literal
      part = part[1:-1]
      index = kwargs[part] if part[0].isalpha() else ast.literal_eval(part)
      try:
        cur_obj = cur_obj[index]
      except:
        return default_value
    elif part[0] == '.':
      attr_name = part[1:]
      if not hasattr(cur_obj, attr_name):
        return default_value
      cur_obj = getattr(cur_obj, attr_name)
    else:
      raise Exception("Invalid path specification")
  return cur_obj


def _pop_from_path(remaining_path):
  if not remaining_path:
    return None, None

  end_index = len(remaining_path)
  for index, c in enumerate(remaining_path[1:]):
    if c == '.' or c == '[':
      end_index = index + 1
      break
  return remaining_path[:end_index], remaining_path[end_index:]
