import ast


def safe_access(path, base_obj, default_value=None):
  """Drill down into an object without having to worry about AttributeErrors,
  KeyErrors, or IndexErrors.

  Keywords arguments:
  path -- a string representing the python expression to access the value you want.
          ex: "a.b[12]["dict_key"].value_i_want
  base_obj -- the base object from which to start drilling down. From the example above,
              this would be a.
  default_value -- the value to return if the path could not be fully traversed
  """

  # Strip variable name of base_obj from path
  _, remaining_path = _pop_from_path(path)
  cur_obj = base_obj

  while remaining_path:
    part, remaining_path = _pop_from_path(remaining_path)

    if part[0] == '[' and part[len(part) - 1] == ']':
      # Note: Need try/except for index access for the same reason python builtin hasattr
      #       uses try/except for safe attribute access
      index = ast.literal_eval(part[1:-1])
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
