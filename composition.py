# coding: utf-8

from bus.api import ABus, ABusAddress, ABusAddressExecutor
from bus import BusAddress, BusAddressExecutor


# Registrations
ABusAddress.register(BusAddress)
ABusAddressExecutor.register(BusAddressExecutor)


def real():
    import smbus
    first_bus = smbus.SMBus(0)
    ABus.register(smbus.SMBus)
    ADDRESS = 0x4A  # sourced from `i2cdetect -y 0`

    CMD_LEADER = 0xFE

    addr = BusAddress(first_bus, ADDRESS)
    return addr.read_byte, BusAddressExecutor(addr, CMD_LEADER).execute


def fake():
    return lambda: 0, lambda *stuff: None
