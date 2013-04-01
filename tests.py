#!/usr/bin/env python
# coding: utf-8

from unittest import TestCase, main as test_main
from doublex.pyDoubles import mock, expect_call
from hamcrest import assert_that, equal_to
from api import Bus, BusAddress


# from http://stackoverflow.com/a/9759329
def concreter(abclass):
    """
    >>> c = concreter(Abstract)
    >>> c.__name__
    'dummy_concrete_Abstract'
    >>> c().bar()
    bar
    """
    if not "__abstractmethods__" in abclass.__dict__:
        return abclass
    new_dict = abclass.__dict__.copy()
    for abstractmethod in abclass.__dict__["__abstractmethods__"]:
        #replace each abc method or property with an identity function:
        new_dict[abstractmethod] = lambda x, *args, **kw: (x, args, kw)
    #creates a new class, with the overriden ABCs:
    return type("dummy_concrete_%s" % abclass.__name__, (abclass,), new_dict)


class TestBusAddress(TestCase):

    def setUp(self):
        self.mock_bus = mock(concreter(Bus))
        self.sut = BusAddress(self.mock_bus, 0x00)

    def test_read_byte(self):
        BYTE_READ = 0x00
        expect_call(self.mock_bus.read_byte).returning(BYTE_READ)
        assert_that(self.sut.read_byte(),
                    equal_to(BYTE_READ))

if __name__ == '__main__':
    test_main()
