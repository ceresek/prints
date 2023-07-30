#!/usr/bin/env python3

import math

from solid import *
from solid.utils import *


SEGMENTS = 33

X = 0
Y = 1
Z = 2
OVERLAP = 0.001


# BRIM_SIZE = 11
# BRIM_OVERLAP = 3
# BRIM_THICKNESS = 0.15

PIN_THICKNESS = 1
PIN_RADIUS = 5/2
PIN_THICKNESS = 1
PIN_LENGTH = 11
PIN_DISTANCE = 160
PIN_SPACE_INSIDE = 30
PIN_SPACE_OUTSIDE = 25

PIN_EDGE_DISTANCE = (PIN_RADIUS + PIN_THICKNESS/2) / math.sqrt (2)

HOLDER_MAXIMUM_LENGTH = PIN_SPACE_INSIDE + PIN_DISTANCE + PIN_SPACE_OUTSIDE

HOLDER_THICKNESS = 3
HOLDER_OVERLAP_FACTOR = 2

THORN_THICKNESS = 2
THORN_RADIUS = 8/2
THORN_LENGTH = 50
THORN_SPACING = 36

THORN_EDGE_DISTANCE = (THORN_RADIUS + THORN_THICKNESS/2) / math.sqrt (2)


def paw ():
    paw = scale (1/3) (linear_extrude (3) (import_dxf ('paw.dxf')))
    return paw


def pin (radius, thickness, length, taper_up, taper_down):
    column = up (length/2) (cube ([2*radius, thickness, length], center = True))
    one = rotate ([0, 0, +45]) (column)
    two = rotate ([0, 0, -45]) (column)
    body = union () (one, two)
    if taper_up:
        taper = cylinder (h = length, r1 = length + radius/2, r2 = radius/2)
        body *= taper
        # body_to_edge = (radius + thickness/2) / math.sqrt (2)
        # trim_to_edge = (radius/2 + thickness/2) / math.sqrt (2)
        # brim = translate ([0, body_to_edge - BRIM_THICKNESS/2, length - trim_to_edge + BRIM_SIZE/2 - BRIM_OVERLAP]) (rotate ([90, 0, 0]) (cube ([BRIM_SIZE, BRIM_SIZE, BRIM_THICKNESS], center = True)))
        # body += brim
    if taper_down:
        taper = cylinder (h = length, r1 = radius/2, r2 = length + radius/2)
        body *= taper
        # body_to_edge = (radius + thickness/2) / math.sqrt (2)
        # trim_to_edge = (radius/2 + thickness/2) / math.sqrt (2)
        # brim = translate ([0, body_to_edge - BRIM_THICKNESS/2, trim_to_edge - BRIM_SIZE/2 + BRIM_OVERLAP]) (rotate ([90, 0, 0]) (cube ([BRIM_SIZE, BRIM_SIZE, BRIM_THICKNESS], center = True)))
        # body += brim
    return body


def holding_pins ():

    holding_pin = back (PIN_EDGE_DISTANCE) (down (PIN_LENGTH) (pin (PIN_RADIUS, PIN_THICKNESS, PIN_LENGTH, False, True)))
    holding_pin_inside = right (PIN_SPACE_INSIDE) (holding_pin)
    holding_pin_outside = right (PIN_SPACE_INSIDE + PIN_DISTANCE) (holding_pin)
    holding_pins = union () (holding_pin_inside, holding_pin_outside)

    return holding_pins


def left_holder_zig ():

    thorn = back (THORN_EDGE_DISTANCE) (pin (THORN_RADIUS, THORN_THICKNESS, THORN_LENGTH, True, False))
    thorn_count = math.floor (HOLDER_MAXIMUM_LENGTH / THORN_SPACING + 1/2)
    thorn_positions = [ index * THORN_SPACING + THORN_SPACING/2 for index in range (thorn_count) ]
    thorn_objects = [ right (position) (thorn) for position in thorn_positions ]
    thorns = union () (*thorn_objects)

    body = right (THORN_SPACING/2 - THORN_RADIUS) (back (2*THORN_EDGE_DISTANCE*HOLDER_OVERLAP_FACTOR) (cube ([(thorn_count-1) * THORN_SPACING + 2*THORN_RADIUS, 2*THORN_EDGE_DISTANCE*HOLDER_OVERLAP_FACTOR, HOLDER_THICKNESS])))

    pattern_element = back (2*THORN_EDGE_DISTANCE) (up (HOLDER_THICKNESS - 1/2) (paw ()))
    pattern_objects = [ right (position + THORN_SPACING/2) (pattern_element) for position in thorn_positions ]
    pattern = union () (*pattern_objects)
    body -= pattern

    holder = union () (holding_pins (), thorns, body)
    
    return holder


def left_holder_zag ():

    thorn = back (THORN_EDGE_DISTANCE) (pin (THORN_RADIUS, THORN_THICKNESS, THORN_LENGTH, True, False))
    thorn_count = math.floor (HOLDER_MAXIMUM_LENGTH / THORN_SPACING - 1/2)
    thorn_positions = [ index * THORN_SPACING + THORN_SPACING for index in range (thorn_count) ]
    thorn_objects = [ right (position) (thorn) for position in thorn_positions ]
    thorns = union () (*thorn_objects)

    body = right (PIN_SPACE_INSIDE - PIN_RADIUS) (back (2*THORN_EDGE_DISTANCE*HOLDER_OVERLAP_FACTOR) (cube ([PIN_DISTANCE + 2*PIN_RADIUS, 2*THORN_EDGE_DISTANCE*HOLDER_OVERLAP_FACTOR, HOLDER_THICKNESS])))

    pattern_element = back (2*THORN_EDGE_DISTANCE) (up (HOLDER_THICKNESS - 1/2) (paw ()))
    pattern_objects = [ right (position + THORN_SPACING/2) (pattern_element) for position in thorn_positions ]
    pattern = union () (*pattern_objects)
    body -= pattern

    holder = union () (holding_pins (), thorns, body)
    
    return holder


def right_holder_zig ():

    return mirror ([1, 0, 0]) (left_holder_zig ())


def right_holder_zag ():

    return mirror ([1, 0, 0]) (left_holder_zag ())


scad_render_to_file (left_holder_zig (), 'left_zig.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (left_holder_zag (), 'left_zag.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (right_holder_zig (), 'right_zig.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (right_holder_zag (), 'right_zag.scad', file_header = f'$fn = {SEGMENTS};')
