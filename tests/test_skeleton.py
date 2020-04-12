# -*- coding: utf-8 -*-

import pytest
from friends_of_tracking.skeleton import fib

__author__ = "Vinay Warrier"
__copyright__ = "Vinay Warrier"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
