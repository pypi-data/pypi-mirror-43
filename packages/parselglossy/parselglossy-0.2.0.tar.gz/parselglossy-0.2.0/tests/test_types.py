#
# parselglossy -- Generic input parsing library, speaking in tongues
# Copyright (C) 2019 Roberto Di Remigio, Radovan Bast, and contributors.
#
# This file is part of parselglossy.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# For information on the complete list of contributors to the
# parselglossy library, see: <http://parselglossy.readthedocs.io/>
#

from parselglossy.validate import type_matches
import pytest


def test_type_matches():

    # str
    assert type_matches('a string', 'str')
    assert not type_matches(1.0, 'str')

    # float and int
    assert type_matches(1.0, 'float')
    assert type_matches(1.0e-8, 'float')
    assert type_matches(1, 'int')
    assert not type_matches(1, 'float')

    # complex
    assert type_matches(1.0 + 1.0j, 'complex')

    # bool
    assert type_matches(True, 'bool')
    assert type_matches(False, 'bool')
    assert not type_matches(0, 'bool')

    # lists
    assert type_matches([1, 2, 3], 'List[int]')
    assert not type_matches((1, 2, 3), 'List[int]')
    assert not type_matches([1, 2, 3], 'List[float]')
    assert type_matches([1.0, 2.0, 3.0], 'List[float]')
    assert not type_matches([1.0, 2.0, 3], 'List[float]')

    # unexpected type input
    with pytest.raises(ValueError):
        assert type_matches('example', 'weird')
        assert type_matches('example', 'List[strange]')
