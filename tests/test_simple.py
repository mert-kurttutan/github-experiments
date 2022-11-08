
import pytest

from dummy_package import my_int


def test_simple():
    assert True, 'Totology'

    x = my_int(3)
    assert x.num == 3
