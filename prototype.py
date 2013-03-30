#!/usr/bin/env python

import smbus
import time

# CONSTANTS
DIGITAL_INPUT     = 0x00
DIGITAL_OUTPUT    = 0x01
ANALOG_INPUT      = 0x05

CMD_BEGIN         = 0xFE
CMD_VERSION       = 0x24
CMD_MODE          = 0x40
CMD_DIGITAL_WRITE = 0x41
CMD_DIGITAL_READ  = 0x42

# GLOBALS
BUS = smbus.SMBus(0)
ADDRESS = 0x4A # sourced from `i2cdetect -y 0`

def write(value):
    BUS.write_byte(ADDRESS, value)

def read():
    return BUS.read_byte(ADDRESS)

def debug(stuff):
    print "DEBUG: %s" % stuff

def debug_bytes(byte_list):
    debug(["0x%02x" % x for x in byte_list]) 

def execute(command, *params):
    debug_bytes([CMD_BEGIN, command] + list(params))
    write(CMD_BEGIN)
    write(command)
    for byte in params:
        write(byte)

def version():
    execute(CMD_VERSION)
    return read()

def pin_digital_out(pin):
    execute(CMD_MODE, pin, DIGITAL_OUTPUT)

def pin_digital_in(pin):
    execute(CMD_MODE, pin, DIGITAL_INPUT)

def pin_digital_write(pin, value):
    execute(CMD_DIGITAL_WRITE, pin, value)

def pin_digital_read(pin):
    execute(CMD_DIGITAL_READ, pin)
    return read()


def proto_lights():
    pin_digital_out(1)
    pin_digital_out(2)
    raw_input()

    p1_val = False
    p2_val = True
    while True:
        pin_digital_write(0x01, p1_val)
        pin_digital_write(0x02, p2_val)
        raw_input()
        p1_val = not p1_val
        p2_val = not p2_val

def proto_read():
    pin_digital_in(4)
    while True:
        print "Digital read of pin 4: %d" % pin_digital_read(4)
        raw_input()

if __name__ == '__main__':
    print "Firmware Version: %d" % version()
    print "Ready to go........."
    raw_input()

    proto_lights()
