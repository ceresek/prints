#!/usr/bin/env python3

import math as _math

from solid import *
from solid.utils import *

from components.common import *

from helpers import ivar


SEGMENTS = 111

HOOK_CHAIN_GAP = 8
HOOK_CHAIN_RISE = 16
HOOK_CHAIN_DEPTH = 11
HOOK_CHAIN_RADIUS = 6

HOOK_PIN_TIP = 2.22
HOOK_PIN_DEPTH = 6.66
HOOK_CATCH_DEPTH = 11

HOOK_THICKNESS = 2.54


SPOOL_EDGE = 8
SPOOL_ANGLE = 45
SPOOL_RADIUS = 8
SPOOL_LENGTH = 131
SPOOL_THICKNESS = 1.7


SPIRAL_SLOPE = 45
SPIRAL_WINGS = 3


def spiral (radius, width, height, threads, direction, offset):
    # Compute twist to have given slope.
    circumference = 2 * _math.pi * radius
    revolutions = height / circumference / _math.tan (_math.radians (SPIRAL_SLOPE))
    # Generate spiral.
    step = 180 / threads
    beams = [ rotate ((0, 0, step * thread + offset)) (square ([radius * 2, width], center = True)) for thread in range (threads) ]
    footprint = union () (*beams)
    result = linear_extrude (height, convexity = 8, twist = _math.copysign (360 * revolutions, direction), slices = height * 3) (footprint)
    # Whatever.
    return result


def hook (rows, shift):

    total_height = max (HOOK_CHAIN_DEPTH, ivar.PIN_RADIUS_SMALL*2 + ivar.PIN_DISTANCE_VERTICAL * (rows-1))

    front_wall = translate ((-ivar.STAND_WIDTH, -HOOK_THICKNESS, 0)) (cube ((ivar.STAND_WIDTH + HOOK_THICKNESS, HOOK_THICKNESS, total_height)))
    side_wall = translate ((0, -HOOK_THICKNESS, 0)) (cube ((HOOK_THICKNESS, ivar.STAND_DEPTH + 2*HOOK_THICKNESS, total_height)))
    back_wall = translate ((-HOOK_CATCH_DEPTH, ivar.STAND_DEPTH, 0)) (cube ((HOOK_CATCH_DEPTH + HOOK_THICKNESS, HOOK_THICKNESS, total_height)))

    pin = rotate ((-90, 0, 0)) (
        union () (
            down (OVERLAP) (cylinder (ivar.PIN_RADIUS_SMALL, HOOK_PIN_DEPTH + 2*OVERLAP)),
            up (HOOK_PIN_DEPTH) (cylinder (r1 = ivar.PIN_RADIUS_SMALL, r2 = ivar.PIN_RADIUS_SMALL - HOOK_PIN_TIP, h = HOOK_PIN_TIP))))

    right_pin = translate ((-ivar.STAND_PIN_HOLE_TO_EDGE - shift, -OVERLAP, ivar.PIN_RADIUS_SMALL)) (pin)
    left_pin = translate ((-ivar.PIN_DISTANCE_HORIZONTAL, 0, 0)) (right_pin)

    pins = left_pin + right_pin

    pin_list = [ translate ((0, 0, ivar.PIN_DISTANCE_VERTICAL * row)) (pins) for row in range (rows) ]
    pin_rows = union () (*pin_list)

    front_base = translate ((-ivar.STAND_WIDTH, -HOOK_THICKNESS, 0)) (cube ((ivar.STAND_WIDTH + HOOK_THICKNESS, HOOK_THICKNESS, HOOK_CHAIN_DEPTH)))
    rise_base = translate ((HOOK_THICKNESS - HOOK_CHAIN_RADIUS, -HOOK_THICKNESS -HOOK_CHAIN_GAP, 0)) (cylinder (HOOK_CHAIN_RADIUS, HOOK_CHAIN_DEPTH))
    rise_pin = translate ((HOOK_THICKNESS - HOOK_CHAIN_RADIUS, -HOOK_THICKNESS -HOOK_CHAIN_GAP, HOOK_CHAIN_DEPTH - OVERLAP)) (cylinder (HOOK_CHAIN_RADIUS, HOOK_CHAIN_RISE + OVERLAP))

    hook = hull () (front_base, rise_base) + front_wall + side_wall + back_wall + pin_rows + rise_pin

    return hook


def spool ():

    rotated_height = SPOOL_EDGE / _math.cos (_math.radians (SPOOL_ANGLE))
    rotated_thickness = SPOOL_THICKNESS / _math.sin (_math.radians (SPOOL_ANGLE))

    bottom_outer = cylinder (r1 = SPOOL_RADIUS + SPOOL_EDGE, r2 = SPOOL_RADIUS, h = rotated_height)
    bottom_inner = translate ((0, 0, -OVERLAP)) (cylinder (r1 = SPOOL_RADIUS + SPOOL_EDGE - rotated_thickness, r2 = SPOOL_RADIUS - rotated_thickness, h = rotated_height + 2*OVERLAP))

    bottom = translate ((0, 0, -rotated_height)) (bottom_outer - bottom_inner)

    top = translate ((0, 0, SPOOL_LENGTH)) (mirror ((0, 0, 1)) (bottom))

    circumference = 2 * _math.pi * SPOOL_RADIUS
    revolutions = SPOOL_LENGTH / circumference / _math.tan (_math.radians (SPIRAL_SLOPE))
    offset = revolutions * 180

    body_left = spiral (SPOOL_RADIUS, SPOOL_THICKNESS, SPOOL_LENGTH, SPIRAL_WINGS, +1, +offset)
    body_right = spiral (SPOOL_RADIUS, SPOOL_THICKNESS, SPOOL_LENGTH, SPIRAL_WINGS, -1, -offset)

    body_hole = translate ((0, 0, -OVERLAP)) (cylinder (SPOOL_RADIUS - SPOOL_THICKNESS, SPOOL_LENGTH + 2*OVERLAP))

    body = body_left + body_right - body_hole

    return bottom + body + top


scad_render_to_file (hook (1, 0), 'hook-one-zero.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (hook (1, 1), 'hook-one-one.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (hook (1, 2), 'hook-one-two.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (hook (2, 0), 'hook-two-zero.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (hook (2, 1), 'hook-two-one.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (hook (2, 2), 'hook-two-two.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (spool (), 'spool.scad', file_header = f'$fn = {SEGMENTS};')
