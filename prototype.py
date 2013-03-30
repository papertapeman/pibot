#!/usr/bin/env python

import smbus
import time

bus = smbus.SMBus(0)
address = 0x4a # sourced from `i2cdetect -y 0`

# TODO: digital input = 0x00, digital output = 0x01, analog input = 0x05
DIGITAL_INPUT = 0x00
DIGITAL_OUTPUT = 0x01
ANALOG_INPUT = 0x05

CMD_BEGIN = 0xFE
CMD_VERSION = 0x24
CMD_DO = 0x40
CMD_DW = 0x41

def write(value):
    #print "Writing 0x%02x" % value
    bus.write_byte_data(address, 0, value)

def read():
    return bus.read_byte_data(address, 1)

def execute(command, *params):
    print [CMD_BEGIN, command] + list(params)
    write(CMD_BEGIN)
    write(command)
    for byte in params:
        write(byte)

def version():
    execute(CMD_VERSION)

def pin_do(pin):
    execute(CMD_DO, pin, DIGITAL_OUTPUT)

def pin_dw(pin, value):
    execute(CMD_DW, pin, value)

if __name__ == '__main__':
    version()
    print read()
    raw_input()

    pin_do(1)
    pin_do(2)
    raw_input()

    p1_val = False
    p2_val = True
    while True:
        pin_dw(0x01, p1_val)
        pin_dw(0x02, p2_val)
        raw_input()
        p1_val = not p1_val
        p2_val = not p2_val
