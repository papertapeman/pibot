#!/usr/bin/env python

import smbus

# CONSTANTS
DIGITAL_INPUT     = 0x00
DIGITAL_OUTPUT    = 0x01
#ANALOG_INPUT      = 0x05 # TODO: currently unused

CMD_BEGIN         = 0xFE
CMD_VERSION       = 0x24
CMD_MODE          = 0x40
CMD_DIGITAL_WRITE = 0x41
CMD_DIGITAL_READ  = 0x42
CMD_MOTOR_FORWARD = 0x50
CMD_MOTOR_REVERSE = 0x51
CMD_MOTOR_STOP    = 0x52
CMD_MOTOR_CURRENT = 0x53
CMD_SWITCH_READ   = 0x54

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

def pin_mode_digital_out(pin):
    execute(CMD_MODE, pin, DIGITAL_OUTPUT)

def pin_mode_digital_in(pin):
    execute(CMD_MODE, pin, DIGITAL_INPUT)

def pin_digital_write(pin, value):
    execute(CMD_DIGITAL_WRITE, pin, value)

def pin_digital_read(pin):
    execute(CMD_DIGITAL_READ, pin)
    return read()

def motor_forward(num, pwm):
    execute(CMD_MOTOR_FORWARD, num, pwm)

def motor_forward_pc(num, percentage):
    pwm = int(percentage * 2.5)
    motor_forward(num, pwm)

def motor_reverse(num, pwm):
    execute(CMD_MOTOR_REVERSE, num, pwm)

def motor_reverse_pc(num, percentage):
    pwm = int(percentage * 2.5)
    motor_reverse(num, pwm)

def motor_stop(num):
    execute(CMD_MOTOR_STOP, num)

def motor_current(mA):
    current_max = 2 # 2A for the board
    val = int(((mA/1000.0) / current_max) * 250)
    execute(CMD_MOTOR_CURRENT, val)

def switch_read():
    execute(CMD_SWITCH_READ)
    return read()

def switch_read_bits():
    ret = switch_read()
    return [bool(ret & pow(2, bit)) for bit in xrange(0, 4)]


def proto_lights():
    pin_mode_digital_out(1)
    pin_mode_digital_out(2)
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
    pin_mode_digital_in(4)
    while True:
        print "Digital read of pin 4: %d" % pin_digital_read(4)
        raw_input()

def proto_motors():
    motor_current(400)

    while True:
        motor_forward_pc(1, 100)
        motor_forward_pc(2, 100)
        raw_input()
        motor_stop(1)
        motor_stop(2)
        raw_input()
        motor_reverse_pc(1, 100)
        motor_reverse_pc(2, 100)
        raw_input()
        motor_stop(1)
        motor_stop(2)
        raw_input()

def proto_motor_stepping():
    motor_current(400)

    while True:
        for pc in xrange(0, 100, 10):
            motor_forward_pc(1, pc)
            motor_forward_pc(2, pc)
            raw_input()

        motor_stop(1)
        motor_stop(2)
        raw_input()

        for pc in xrange(100, 0, -10):
            motor_forward_pc(1, pc)
            motor_forward_pc(2, pc)
            raw_input()

        motor_stop(1)
        motor_stop(2)
        raw_input()

def proto_switch_read():
    while True:
        print "Switch value: %s" % switch_read()
        print "Bits: %s" % switch_read_bits()

        raw_input()

if __name__ == '__main__':
    print "Firmware Version: %d" % version()
    print "Ready to go........."
    raw_input()

    proto_switch_read()
