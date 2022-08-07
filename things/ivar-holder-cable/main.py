#!/usr/bin/env python3

import math

from solid import *
from solid.utils import *

from helpers import ivar

SEGMENTS = 33

X = 0
Y = 1
Z = 2
OVERLAP = 0.001


PIN_THICKNESS = 0.86

BODY_THICKNESS = 0.86

POWER_WIRE_ONE_X = 5
POWER_WIRE_ONE_Y = 2.5
POWER_WIRE_TWO_X = 5.5
POWER_WIRE_TWO_Y = 3

NET_WIRE_ONE_RADIUS = 6.5
NET_WIRE_TWO_RADIUS = 8.5


def pin (radius, thickness, length, taper_up, taper_down):
    column = left (thickness/2) (cube ((thickness, radius, length)))
    one = rotate ((0, 0, +120)) (column)
    two = rotate ((0, 0, -120)) (column)
    middle = cylinder (h = length, r = thickness/2)
    body = union () (column, one, two, middle)
    if taper_up:
        taper = cylinder (h = length, r1 = length + radius/2, r2 = radius/2)
        body *= taper
    if taper_down:
        taper = cylinder (h = length, r1 = radius/2, r2 = length + radius/2)
        body *= taper
    return body


def wire (width, height, length):
    one = translate ((+ (width - height)/2, height/2, -length/2)) (cylinder (r = height/2, h = length))
    two = translate ((- (width - height)/2, height/2, -length/2)) (cylinder (r = height/2, h = length))
    tre = translate ((0, height/4, 0)) (cube ((width, height/2, length), center = True))
    return hull () (one, two, tre)


def holder_pins (radius):

    pin_any = forward (OVERLAP) (rotate ((90, 0, 0)) (pin (radius, PIN_THICKNESS, ivar.PIN_LENGTH + OVERLAP, True, False)))
    pin_left = left (ivar.PIN_DISTANCE_HORIZONTAL/2) (pin_any)
    pin_right = right (ivar.PIN_DISTANCE_HORIZONTAL/2) (pin_any)

    return pin_left + pin_right


def holder_single (wire_width = POWER_WIRE_ONE_X, wire_height = POWER_WIRE_ONE_Y, radius = ivar.PIN_RADIUS_SMALL):

    pins = holder_pins (radius)

    body = forward (BODY_THICKNESS/2) (cube ((ivar.PIN_DISTANCE_HORIZONTAL + 2 * radius, BODY_THICKNESS, 2 * radius), center = True))

    hook_outer = wire (wire_width + 2 * BODY_THICKNESS, wire_height + BODY_THICKNESS, 2 * radius)
    hook_inner = back (OVERLAP) (wire (wire_width, wire_height + OVERLAP, 2 * radius + 2 * OVERLAP))
    hook_total = hook_outer - hook_inner

    total = pins + (body - hook_inner) + hook_total

    return total


def holder_double (wire_width = POWER_WIRE_ONE_X, wire_height = POWER_WIRE_ONE_Y, radius = ivar.PIN_RADIUS_SMALL):

    pins = holder_pins (radius)

    body = forward (BODY_THICKNESS/2) (cube ((ivar.PIN_DISTANCE_HORIZONTAL + 2 * radius, BODY_THICKNESS, 2 * radius), center = True))

    hook_outer = wire (wire_width + 2 * BODY_THICKNESS, wire_height + BODY_THICKNESS, 2 * radius)
    hook_inner = back (OVERLAP) (wire (wire_width, wire_height + OVERLAP, 2 * radius + 2 * OVERLAP))
    hook_total = hook_outer - hook_inner

    hook_inner_left = left (ivar.PIN_DISTANCE_HORIZONTAL/5) (hook_inner)
    hook_total_left = left (ivar.PIN_DISTANCE_HORIZONTAL/5) (hook_total)
    hook_inner_right = right (ivar.PIN_DISTANCE_HORIZONTAL/5) (hook_inner)
    hook_total_right = right (ivar.PIN_DISTANCE_HORIZONTAL/5) (hook_total)

    total = pins + (body - hook_inner_left - hook_inner_right) + hook_total_left + hook_total_right

    return total


scad_render_to_file (holder_single (POWER_WIRE_ONE_X, POWER_WIRE_ONE_Y, ivar.PIN_RADIUS_SMALL), 'holder_power_one_single.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (holder_single (POWER_WIRE_TWO_X, POWER_WIRE_TWO_Y, ivar.PIN_RADIUS_LARGE), 'holder_power_two_single.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (holder_double (POWER_WIRE_ONE_X, POWER_WIRE_ONE_Y, ivar.PIN_RADIUS_SMALL), 'holder_power_one_double.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (holder_single (NET_WIRE_ONE_RADIUS, NET_WIRE_ONE_RADIUS), 'holder_net_one_single.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (holder_single (NET_WIRE_TWO_RADIUS, NET_WIRE_TWO_RADIUS), 'holder_net_two_single.scad', file_header = f'$fn = {SEGMENTS};')
