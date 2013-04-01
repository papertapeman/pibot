# coding: utf-8

from bus.api import ABusAddress, ABusAddressExecutor
from bus.concrete import BusAddress, BusAddressExecutor

# Registrations
ABusAddress.register(BusAddress)
ABusAddressExecutor.register(BusAddressExecutor)
