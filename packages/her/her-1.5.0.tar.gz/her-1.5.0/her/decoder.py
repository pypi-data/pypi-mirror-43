# This file is a part of HER
#
# Copyright (c) 2019 The HER Authors (see AUTHORS)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
her.decoder
~~~~~~~~~~~
It contains the decoder functions.

It could be used to decode HER and convert it into
a dictionary.
"""

import ast

from typing import Any, Dict


def _get_type(value: str) -> Any:
    """
    Get the HER type of the string.

    :param value: The string value.
    :type value: str
    :return: The real value.
    :rtype: Any
    """

    # Converting boolean to Python boolean representation
    if value.lower() in ["false", "true"]:
        value = value.title()

    # Converting NULL or None to Python NoneType
    if value.lower() in ["null", "none"]:
        value = "None"

    real_value = ast.literal_eval(value)  # Get the real value

    # Type checking
    if type(real_value) in [bool, float, int, list, type(None), str]:
        return real_value  # Return the real value

    raise TypeError("Unexpected type, got %s" % type(real_value).__name__)  # No type detected


def decode(representation: str) -> Dict[str, Any]:
    """
    It parses the string and convert it
    into a dictionary.

    :param representation: A list of the lines of the string.
    :type representation: list
    """

    # String checking
    if not isinstance(representation, str):
        raise TypeError("The passed argument must be a string")

    values = {}  # The dictionary that will be returned
    current_section = ""  # The current section

    lines = [line.strip().rstrip() for line in representation.split("\n")]  # Get the lines & trim space

    for line in lines:

        # Comment checking
        if line.startswith("#"):
            continue

        # Section/category checking
        elif line.startswith("- ") & line.endswith(" -"):

            # Get the current section
            current_section = line[2:-2]
            values[current_section] = {}

        # Array declaration checking
        elif line.startswith(">> "):

            # Array validation
            if line.split(" =", 1)[0][-2:] == "[]":
                values[current_section][
                    line.split("[] =", 1)[0][3:-2]] = []

        # Declaration checking
        elif line.startswith("* "):

            # Array element checking
            if line.split(" =", 1)[0][-2:] == "[]":

                # Element appending
                values[current_section][line.split(" =")[0][2:-2]].append(
                    _get_type(line.split(" = ", 1)[1]))
            else:

                # Element assignment
                values[current_section][line.split(" =")[0][2:]] = _get_type(line.split(" = ", 1)[1])

    return values
