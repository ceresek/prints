#!/usr/bin/env python3

import math as _math

from solid2 import *
from solid2.extensions.bosl2 import *

from components.common import *

from helpers import ivar


set_global_fn (111)


OVERLAP = 0.001

HOOK_POLE_DIAMETER = 12.3
HOOK_POLE_LENGTH = 33
HOOK_POLE_ANGLE = 45
HOOK_POLE_SINK = 18
HOOK_POLE_RISE = 6.66

HOOK_CHAIN_GAP = 8
HOOK_CHAIN_RISE = 16
HOOK_CHAIN_DEPTH = 11
HOOK_CHAIN_RADIUS = 6

HOOK_PIN_TIP = 2.22
HOOK_PIN_DEPTH_IN = 2.22
HOOK_PIN_DEPTH_OUT = 6.66

HOOK_CATCH_DEPTH = 11

HOOK_THICKNESS = SIX_PERIMETERS


SPOOL_EDGE = 8
SPOOL_ANGLE = 45
SPOOL_RADIUS = 8
SPOOL_LENGTH = 131
SPOOL_THICKNESS = FOR_PERIMETERS


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


def spool ():

    rotated_height = SPOOL_EDGE / _math.cos (_math.radians (SPOOL_ANGLE))
    rotated_thickness = SPOOL_THICKNESS / _math.sin (_math.radians (SPOOL_ANGLE))

    bottom_outer = cyl (r1 = SPOOL_RADIUS + SPOOL_EDGE, r2 = SPOOL_RADIUS, h = rotated_height, anchor = TOP)
    bottom_inner = cyl (r1 = SPOOL_RADIUS + SPOOL_EDGE - rotated_thickness, r2 = SPOOL_RADIUS - rotated_thickness, h = rotated_height + 2*OVERLAP, anchor = TOP).up (OVERLAP)

    bottom = bottom_outer - bottom_inner

    top = bottom.mirror ([0, 0, 1]).up (SPOOL_LENGTH)

    circumference = 2 * _math.pi * SPOOL_RADIUS
    revolutions = SPOOL_LENGTH / circumference / _math.tan (_math.radians (SPIRAL_SLOPE))
    offset = revolutions * 180

    body_right = spiral (SPOOL_RADIUS, SPOOL_THICKNESS, SPOOL_LENGTH, SPIRAL_WINGS, -1, -offset)
    body_left = spiral (SPOOL_RADIUS, SPOOL_THICKNESS, SPOOL_LENGTH, SPIRAL_WINGS, +1, +offset)
    body_hole = cyl (r = SPOOL_RADIUS - SPOOL_THICKNESS, h = SPOOL_LENGTH + 2*OVERLAP, anchor = BOTTOM)

    body = body_left + body_right - body_hole

    return bottom + body + top


def clasp (rows, shift):

    total_height = max (HOOK_CHAIN_DEPTH + HOOK_THICKNESS, ivar.PIN_RADIUS_SMALL*2 + ivar.PIN_DISTANCE_VERTICAL * (rows-1))

    face_wall = cuboid ((ivar.STAND_WIDTH, HOOK_THICKNESS, total_height), anchor = RIGHT+BACK+BOTTOM)
    side_wall = cuboid ((HOOK_THICKNESS, ivar.STAND_DEPTH + 2*HOOK_THICKNESS, total_height), anchor = LEFT+FRONT+BOTTOM).fwd (HOOK_THICKNESS)
    back_wall = cuboid ((HOOK_CATCH_DEPTH, HOOK_THICKNESS, total_height), anchor = RIGHT+FRONT+BOTTOM).back (ivar.STAND_DEPTH)

    right_pin = cyl (h = HOOK_PIN_DEPTH_IN + HOOK_PIN_TIP, r = ivar.PIN_RADIUS_SMALL, chamfer2 = HOOK_PIN_TIP, anchor = BOTTOM+BACK, orient = BACK).left (shift + ivar.STAND_PIN_HOLE_TO_EDGE)
    left_pin = cyl (h = HOOK_PIN_DEPTH_OUT + HOOK_PIN_TIP, r = ivar.PIN_RADIUS_SMALL, chamfer2 = HOOK_PIN_TIP, anchor = BOTTOM+BACK, orient = BACK).left (shift + ivar.STAND_PIN_HOLE_TO_EDGE + ivar.PIN_DISTANCE_HORIZONTAL)

    pins = left_pin + right_pin

    pin_list = [ pins.up (ivar.PIN_DISTANCE_VERTICAL * row) for row in range (rows) ]
    pin_rows = union () (*pin_list)

    return face_wall + side_wall + back_wall + pin_rows


def hook_chain (rows, shift):

    front_base = cuboid ([ivar.STAND_WIDTH + HOOK_THICKNESS, HOOK_THICKNESS, HOOK_CHAIN_DEPTH], anchor = RIGHT+BACK+BOTTOM, rounding = HOOK_THICKNESS, edges = LEFT+FRONT).right (HOOK_THICKNESS)
    rise_base = cyl (r = HOOK_CHAIN_RADIUS, h = HOOK_CHAIN_DEPTH, anchor = BOTTOM).left (HOOK_CHAIN_RADIUS - HOOK_THICKNESS).fwd (HOOK_THICKNESS + HOOK_CHAIN_GAP)
    rise_pin = cyl (r = HOOK_CHAIN_RADIUS, h = HOOK_CHAIN_RISE + OVERLAP, anchor = BOTTOM).left (HOOK_CHAIN_RADIUS - HOOK_THICKNESS).fwd (HOOK_THICKNESS + HOOK_CHAIN_GAP).up (HOOK_CHAIN_DEPTH - OVERLAP)

    hook = clasp (rows, shift) + hull () (front_base, rise_base) + rise_pin

    return hook


def hook_pole (rows, shift):

    hook_height = ivar.PIN_RADIUS_SMALL*2 + ivar.PIN_DISTANCE_VERTICAL * (rows-1)

    pole_angled_width = HOOK_POLE_DIAMETER * _math.sin (_math.radians (HOOK_POLE_ANGLE))
    pole_angled_height = HOOK_POLE_DIAMETER * _math.cos (_math.radians (HOOK_POLE_ANGLE))

    lower_wall_base = (
        cuboid ([ivar.STAND_WIDTH + HOOK_THICKNESS, HOOK_THICKNESS, hook_height + HOOK_POLE_RISE - HOOK_POLE_SINK], anchor = RIGHT+BACK+BOTTOM)
        .right (HOOK_THICKNESS)
    )

    lower_pole_base = (
        (
            cyl (d = HOOK_POLE_DIAMETER + 2*HOOK_THICKNESS, h = HOOK_POLE_LENGTH + HOOK_THICKNESS, anchor = BOTTOM)
            -
            cuboid (
                [
                    HOOK_POLE_DIAMETER/2 + HOOK_THICKNESS + OVERLAP,
                    HOOK_POLE_DIAMETER + 2*HOOK_THICKNESS,
                    HOOK_POLE_LENGTH + HOOK_THICKNESS
                ],
                anchor = BOTTOM+RIGHT,
            )
            +
            cuboid (
                [
                    HOOK_POLE_RISE,
                    HOOK_POLE_DIAMETER + 2*HOOK_THICKNESS,
                    HOOK_POLE_LENGTH + HOOK_THICKNESS
                ],
                anchor = BOTTOM+RIGHT,
            )
        )
        .rotate (0, 90, 0 - HOOK_POLE_ANGLE)
        .left (ivar.STAND_WIDTH - pole_angled_width/2 - HOOK_THICKNESS)
        .back (HOOK_THICKNESS + pole_angled_height/2)
        .up (hook_height - HOOK_POLE_SINK)
    )

    lower_base = hull () (lower_wall_base, lower_pole_base)

    upper_wall_base = (
        cuboid ([HOOK_THICKNESS, HOOK_THICKNESS, HOOK_POLE_SINK], anchor = RIGHT+BACK+TOP)
        .right (HOOK_THICKNESS)
        .up (hook_height)
    )

    upper_pole_base = (
        cuboid (
            [
                HOOK_POLE_RISE,
                HOOK_THICKNESS,
                HOOK_POLE_LENGTH + HOOK_THICKNESS
            ],
            anchor = BOTTOM+RIGHT+FRONT,
        )
        .back (HOOK_POLE_DIAMETER/2)
        .rotate (0, 90, 0 - HOOK_POLE_ANGLE)
        .left (ivar.STAND_WIDTH - pole_angled_width/2 - HOOK_THICKNESS)
        .back (HOOK_THICKNESS + pole_angled_height/2)
        .up (hook_height - HOOK_POLE_SINK)
    )

    upper_base = hull () (upper_wall_base, upper_pole_base)

    pole = (
        (
            cyl (d = HOOK_POLE_DIAMETER, h = HOOK_POLE_LENGTH + OVERLAP, anchor = BOTTOM)
            +
            cuboid (
                [
                    HOOK_POLE_RISE + OVERLAP,
                    HOOK_POLE_DIAMETER,
                    HOOK_POLE_LENGTH + HOOK_THICKNESS
                ],
                anchor = BOTTOM+RIGHT,
            )
        )
        .up (HOOK_THICKNESS)
        .rotate (0, 90, 0 - HOOK_POLE_ANGLE)
        .left (ivar.STAND_WIDTH - pole_angled_width/2 - HOOK_THICKNESS)
        .back (HOOK_THICKNESS + pole_angled_height/2)
        .up (hook_height - HOOK_POLE_SINK)
    )

    hook = clasp (rows, shift) + upper_base + lower_base - pole

    return hook


spool ().save_as_scad ('spool.scad')

hook_chain (1, 0).save_as_scad ('hook-chain-one-zero.scad')
hook_chain (1, 1).save_as_scad ('hook-chain-one-one.scad')
hook_chain (1, 2).save_as_scad ('hook-chain-one-two.scad')
hook_chain (2, 0).save_as_scad ('hook-chain-two-zero.scad')
hook_chain (2, 1).save_as_scad ('hook-chain-two-one.scad')
hook_chain (2, 2).save_as_scad ('hook-chain-two-two.scad')

hook_pole (2, 0).save_as_scad ('hook-pole-two-zero.scad')
hook_pole (2, 1).save_as_scad ('hook-pole-two-one.scad')
hook_pole (2, 2).save_as_scad ('hook-pole-two-two.scad')
hook_pole (3, 0).save_as_scad ('hook-pole-three-zero.scad')
hook_pole (3, 1).save_as_scad ('hook-pole-three-one.scad')
hook_pole (3, 2).save_as_scad ('hook-pole-three-two.scad')
