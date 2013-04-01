# coding: utf-8
from abc import ABCMeta, abstractmethod


class ABus(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def read_byte(self, address):
        "Read a byte from the given address."

    @abstractmethod
    def write_byte(self, address, byte):
        "Write a byte to the given address."


class ABusAddress(object):

    """
    Perform operations on a defined bus address.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def read_byte(self):
        pass

    @abstractmethod
    def write_byte(self, byte):
        pass


class ABusAddressExecutor(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, command, *params):
        pass
