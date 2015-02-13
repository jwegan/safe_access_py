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

import ast


SINGLE_QUOTE = '\x27'
DOUBLE_QUOTE = '\x22'


def safe_access(base_obj, path, default_value=None, **kwargs):
    """Drill down into an object without having to worry about AttributeErrors,
    KeyErrors, or IndexErrors.

    Keywords arguments:
    base_obj -- the base object from which to start drilling down. From the example above,
                            this would be a.
    path -- a string representing the python expression to access the value you want.
                    ex: "a.b[12]['dict_key'].value_i_want"
    default_value -- the value to return if the path could not be fully traversed
    **kwargs -- variables used as dictionary keys or list indexes in the path expression.
                            ex: myvar would need to be in kwargs if you use path="a.b.[myvar]"

    Notes: Dictionary keys or list indexes must be one of the following.
        1) String - the first character after the left square bracket should be a quote.
            Triple quotes, and escaping quotes is not supported. (i.e. a['abc\'def'] will not work)
        2) Variable - can be passed in as keyword args and then referenced in path.
            ex: a.b.[myvar] where myvar is passed in as a kwarg
        3) Literal - any python literal including tuples, or None. Variable references within
            a literal are not supported.
        4) Wildcards - * will search all keys/items and return a list of all objects safe_access was able to
            succesfully drill down into.
    """

    # Strip variable name of base_obj from path
    _, remaining_path = _pop_from_path(path)
    current_objects = [base_obj]
    used_wildcard = False

    while remaining_path and current_objects:
        raw_part, remaining_path = _pop_from_path(remaining_path)
        prev_objects = current_objects
        current_objects = list()

        for obj in prev_objects:
            # Handle square brackets accessor
            if raw_part[0] == '[' and raw_part[-1] == ']':
                part = raw_part[1:-1]
                used_wildcard = used_wildcard or (part[0] == '*' and len(part) == 1)
                tmp_objects = list()

                # Deal with non-wildcard case
                if part[0] != '*' or len(part) > 1:
                    key = kwargs[part] if part[0].isalpha() else ast.literal_eval(part)
                    try:
                        tmp_objects.append(obj[key])
                    except:
                        continue

                # Deal with wildcard cases
                # First try sequence protocol because iterating over a list of ints
                # can throw off the map protocol
                if not tmp_objects:
                    try:
                        for index in xrange(len(obj)):
                            tmp_objects.append(obj[index])
                    except:
                        tmp_objects = list()

                # Then try map protocol
                if not tmp_objects:
                    try:
                        for key in obj:
                            tmp_objects.append(obj[key])
                    except:
                        tmp_objects = list()
                current_objects.extend(tmp_objects)

            # Handle dot accessor
            elif raw_part[0] == '.':
                part = raw_part[1:]
                used_wildcard = used_wildcard or (part[0] == '*' and len(part) == 1)
                for attr in ([part] if part != '*' else [a for a in dir(obj) if not a.startswith("__")]):
                    if hasattr(obj, attr):
                        current_objects.append(getattr(obj, attr))

            # Else unknown acessor
            else:
                raise Exception("Invalid path specification near: %s" % part)

    # Return list if wildcard used, otherwise return the value
    if not current_objects:
        return default_value
    elif current_objects and used_wildcard:
        return current_objects
    else:
        return current_objects[0]


def _pop_from_path(remaining_path):
    if not remaining_path:
        return None, None

    end_index = len(remaining_path)
    str_terminator = None
    for index, c in enumerate(remaining_path[1:]):
        if index == 0 and (c == SINGLE_QUOTE or c == DOUBLE_QUOTE):
            str_terminator = c
        elif c == str_terminator:
            str_terminator = None
        elif not str_terminator and (c == '.' or c == '['):
            end_index = index + 1
            break

    if str_terminator:
        raise Exception("Invalid path specification: end quote not found")
    return remaining_path[:end_index], remaining_path[end_index:]
