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

import re
from setuptools import setup, find_packages


def markdown_to_reST(text):
    '''This is not a general purpose converter. Only converts this readme'''
    # Convert parameters to italics and prepend a newline
    text = re.sub(pattern=r"\n       (\w+) - (.+)\n",
                  repl=r"\n\n       *\g<1>* - \g<2>\n",
                  string=text)

    # Parse [http://url](text), and just leave the url
    text = re.sub(pattern=r"\[([^\]]+)\]\([^)]+\)",
                  repl=r"\g<1>",
                  string=text)

    # Disable formatting of numbered lists
    text = re.sub(pattern=r"\n(\d+). ",
                  repl=r"\n\\\g<1>. ",
                  string=text)

    # Strip ```
    text = re.sub(pattern=r"```",
                  repl=r"",
                  string=text)
    return "\n" + text


setup(
    name='safe_access',
    version='1.1',
    description='Tool to make drilling into Python objects easy & painless',
    long_description=markdown_to_reST(open("README.md").read()),
    license='MPL 2.0',
    author='John Egan',
    author_email='me@jwegan.com',
    url='https://github.com/jwegan/safe_access_py',
    zip_safe=True,
    packages=find_packages(exclude=['ez_setup', 'packages', 'tests*']),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Topic :: Utilities",
    ],
)
