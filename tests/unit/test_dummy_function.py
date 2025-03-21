import pytest


from dummy_function import doubler


def test_doubler():

    input = "mystring"
    expected_output = input * 2

    assert doubler(input) == expected_output
