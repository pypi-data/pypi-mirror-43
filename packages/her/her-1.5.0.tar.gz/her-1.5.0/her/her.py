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
her.core.her
~~~~~~~~~~~~
It contains all objects that represents
an HER file.
"""

from typing import Any, Dict, Optional

from .decoder import decode
from .encoder import encode


class HER:
    r"""
    The HER class is used to avoid multiple
    calls of the encode & decode functions.
    It uses properties, so it updates all its
    attributes every single time you assign a new
    value to an attribute.

    Example::

        x = her.HER()
        x.value = {"foo": {"lol": 1}}
        print(repr(x.representation)) # Output: '- foo -\n    * lol = 1'

    You can also pass a parameter (dict or str)::

        x = her.HER('- foo -\n    * lol = 1')
        print(x.value) # Output: {"foo": {"lol": 1}}

        y = her.HER({"foo": {"lol": 1}})
        print(repr(x.representation)) # Output: '- foo -\n    * lol = 1'
    """

    _representation: str
    _value: Dict[str, Any]

    def __init__(self, value: Optional[Any] = None):
        """
        Initialize the class. You can pass an optional
        parameter (str or dict, it depends on which value
        you want to initialize first) or just nothing.

        :param value: A string or a dictionary, it depends on which value you want to initialize first
        :type value: str or dict
        """

        # Nonetype checking
        if value is not None:

            # String checking & assignment
            if isinstance(value, str):
                self.representation = value

            # Dictionary checking & assignment
            elif isinstance(value, Dict):
                self.value = value

            # No recognized type, throw an exception
            else:
                raise TypeError("No dictionary or string passed")

    @property
    def representation(self) -> str:
        """
        The string which represents the set
        value using HER standards.

        :return: The representation.
        :rtype: str
        """
        return self._representation

    @representation.setter
    def representation(self, representation: str):
        """
        The "representation" attribute setter. It
        updates the "value" attribute automatically.

        :param representation: The representation
        :type representation: str
        """

        # String checking
        if not isinstance(representation, str):
            raise TypeError("The passed value must be a string.")

        self._value = decode(representation)  # Decode the new value & update the representation attribute
        self._representation = representation  # Update the representation attribute

    @property
    def value(self) -> Dict[str, Any]:
        """
        The value which represents the content
        of the HER string as a dictionary.

        :return: The value.
        :rtype: dict
        """
        return self._value

    @value.setter
    def value(self, value: Dict[str, Any]):
        """
        The "value" attribute setter. It updates
        the "representation" attribute automatically.

        :param value: The HER value
        :type value: dict
        """

        # Dictionary checking
        if not isinstance(value, dict):
            raise TypeError("The passed value must be a dictionary.")

        self._representation = encode(value)  # Encode the new value & update the representation attribute
        self._value = value  # Update the value attribute
