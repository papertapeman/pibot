# coding: utf-8

from abc import ABCMeta, abstractmethod


class Bus(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def read_byte(self, address):
        "Read a byte from the given address."

    @abstractmethod
    def write_byte(self, address, byte):
        "Write a byte to the given address."


class BusAddress(object):

    """
    Perform operations on a bus address.
    """

    def __init__(self, bus, address):
        self.bus = bus
        self.address = address

    def read_byte(self):
        return self.bus.read_byte(self.address)

    def write_byte(self, byte):
        self.bus.write_byte(self.address, byte)
