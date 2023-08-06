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
her.encoder
~~~~~~~~~~~
It contains the encoder functions.

It could be used to encode a dictionary and convert it into
an HER text.
"""

from typing import Any, Dict


def encode(dictionary: Dict[str, Any]) -> str:
    """
    It parses and convert the dictionary
    into an HER text.

    :param dictionary: The dictionary you want to convert.
    :type dictionary: dict
    """

    # Dictionary checking
    if not isinstance(dictionary, dict):
        raise TypeError("The passed argument must be a dictionary")

    values = []  # A list of all HER variables

    for key, value in dictionary.items():
        values.append("- " + key + " -")  # Initialize the category

        for sub_key, sub_value in value.items():  # Loop on the category values

            # List checking & appending
            if isinstance(sub_key, list):
                values.append("    >> " + str(sub_key) + "[]")

                for tunnel_value in sub_value:
                    values.append(
                        "    * " + str(
                            sub_key) + "[] = " + str(
                            repr(tunnel_value)))
            else:
                values.append(
                    "    * " + str(
                        sub_key) + " = " + str(
                        repr(sub_value)))

    return "\n".join(values)
