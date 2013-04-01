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


class BusAddress(object):

    def __init__(self, bus, address):
        self.bus = bus
        self.address = address

    def read_byte(self):
        return self.bus.read_byte(self.address)

    def write_byte(self, byte):
        self.bus.write_byte(self.address, byte)


class BusAddressExecuter(object):

    def __init__(self, bus_address, execution_leader):
        self.bus_address = bus_address
        self.execution_leader = execution_leader

    def execute(self, command, *params):
        self.bus_address.write_byte(self.execution_leader)
        self.bus_address.write_byte(command)
        for param in params:
            self.bus_address.write_byte(param)


# Registrations
ABusAddress.register(BusAddress)
