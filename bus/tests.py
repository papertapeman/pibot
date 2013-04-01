#!/usr/bin/env python
# coding: utf-8

from unittest import TestCase, main as test_main
from doublex import Mock, verify
from hamcrest import assert_that, equal_to
from api import ABus, ABusAddress
from concrete import BusAddress, BusAddressExecuter


class TestBusAddress(TestCase):

    def setUp(self):
        self.address = 0x00

    def test_read_byte(self):
        # Arrange
        BYTE_TO_READ = 0x00
        with Mock(ABus) as mock_bus:
            mock_bus.read_byte(self.address).returns(BYTE_TO_READ)

        # Act
        bus_address = BusAddress(mock_bus, self.address)

        # Assert
        assert_that(bus_address.read_byte(),
                    equal_to(BYTE_TO_READ))

        assert_that(mock_bus, verify())

    def test_write_byte(self):
        # Arrange
        BYTE_TO_WRITE = 0x00
        with Mock(ABus) as mock_bus:
            mock_bus.write_byte(self.address, BYTE_TO_WRITE)

        bus_address = BusAddress(mock_bus, self.address)

        # Act
        bus_address.write_byte(BYTE_TO_WRITE)

        # Assert
        assert_that(mock_bus, verify())


class TestBusExecute(TestCase):

    def setUp(self):
        self.execution_leader = "exec"

    def test_execute(self):
        # Arrange
        COMMAND = "cmd"
        PARAMS = ("p1", "p2")
        with Mock(ABusAddress) as mock_bus_address:
            mock_bus_address.write_byte(self.execution_leader)
            mock_bus_address.write_byte(COMMAND)
            for param in PARAMS:
                mock_bus_address.write_byte(param)

        bus_address_executer = BusAddressExecuter(mock_bus_address, self.execution_leader)

        # Act
        bus_address_executer.execute(COMMAND, *PARAMS)

        # Assert
        assert_that(mock_bus_address, verify())


if __name__ == '__main__':
    test_main()
