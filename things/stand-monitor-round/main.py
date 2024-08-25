#!/usr/bin/env python3

import math as _math

from solid2 import *
from solid2.extensions.bosl2 import *


set_global_fn (111)


OVERLAP = 0.001

STAND_THICKNESS = 22
STAND_DIAMETER = 233
STAND_HEIGHT = 123

MANE_THICKNESS = 11

PAW_SCALE = 0.1
PAW_DEPTH = 0.18
PAW_HEIGHT = 12

PAW_COUNT_RING = 16

SLICER_TOOTH_WIDTH = 7
SLICER_TOOTH_DEPTH = 2
SLICER_TOOTH_SLANT = 0.5
SLICER_THICKNESS = 0.3
SLICER_SHIFT = 13

CUP_HEIGHT = 95
CUP_DIAMETER = 80
CUP_THICKNESS = 3.37 # 8 perimeters


def stand ():

    body = (
        cyl (
            d = STAND_DIAMETER,
            h = STAND_HEIGHT,
            anchor = BOTTOM,
        )
        -
        cyl (
            d = STAND_DIAMETER - 2 * STAND_THICKNESS,
            h = STAND_HEIGHT + 2 * OVERLAP,
            anchor = BOTTOM,
        )
        .down (OVERLAP)
        +
        cuboid (
            [MANE_THICKNESS, STAND_DIAMETER / 2, STAND_HEIGHT],
            anchor = LEFT + FRONT + BOTTOM,
        )
        .left (STAND_DIAMETER / 2)
        +
        cuboid (
            [MANE_THICKNESS, STAND_DIAMETER / 2, STAND_HEIGHT],
            anchor = RIGHT + FRONT + BOTTOM,
        )
        .right (STAND_DIAMETER / 2)
    )

    paw = import_ ('paw.svg').scale (PAW_SCALE)
    paw_flat = linear_extrude (height = 2 * PAW_DEPTH) (paw).down (PAW_DEPTH).rotate ([90, 0, 90])
    paw_round = cylindrical_extrude (id = STAND_DIAMETER - 2 * PAW_DEPTH, od = STAND_DIAMETER + 2 * PAW_DEPTH) (paw)

    PAW_RING_ANGLE = 180 / PAW_COUNT_RING

    paw_ring_angles = [ PAW_RING_ANGLE * index - 90 for index in range (0, PAW_COUNT_RING + 1) ]

    paw_ring = (
        zrot_copies (paw_ring_angles) (paw_round)
        .up (PAW_HEIGHT)
    )

    STAND_CIRCUMFERENCE = _math.pi * STAND_DIAMETER
    PAW_SPACING = STAND_CIRCUMFERENCE / PAW_COUNT_RING / 2
    PAW_COUNT_LINE = _math.floor (STAND_DIAMETER / PAW_SPACING / 2)

    paw_line_left = ycopies (spacing = PAW_SPACING, n = PAW_COUNT_LINE, sp = [0 - STAND_DIAMETER / 2, 0, PAW_HEIGHT]) (paw_flat)
    paw_line_right = ycopies (spacing = PAW_SPACING, n = PAW_COUNT_LINE, sp = [0 + STAND_DIAMETER / 2, 0, PAW_HEIGHT]) (paw_flat)

    return body - paw_ring - paw_line_left - paw_line_right


def slicer ():

    wall = sphere (d = SLICER_THICKNESS) + sphere (d = SLICER_THICKNESS).up (STAND_HEIGHT)

    tooth_path = [
        [0 - SLICER_TOOTH_SLANT, 0 - SLICER_TOOTH_DEPTH],
        [SLICER_TOOTH_WIDTH * 1 + SLICER_TOOTH_SLANT, 0 - SLICER_TOOTH_DEPTH], [SLICER_TOOTH_WIDTH * 1 - SLICER_TOOTH_SLANT, 0 + SLICER_TOOTH_DEPTH],
        [SLICER_TOOTH_WIDTH * 2 + SLICER_TOOTH_SLANT, 0 + SLICER_TOOTH_DEPTH], [SLICER_TOOTH_WIDTH * 2 - SLICER_TOOTH_SLANT, 0 - SLICER_TOOTH_DEPTH],
    ]
    tooth_list = [ wall.translate (x, y, 0) for x, y in tooth_path ]
    tooth_body = chain_hull () (*tooth_list)

    teeth_half_list = [ tooth_body.right (2 * index * SLICER_TOOTH_WIDTH) for index in range (round (STAND_DIAMETER / SLICER_TOOTH_WIDTH / 4) + 1) ]
    teeth_half_line = union () (*teeth_half_list)
    teeth_full_line = teeth_half_line + teeth_half_line.mirror ([1, 0, 0])

    return teeth_full_line


def cup ():

    # Make the cup about as segmented as the stand.
    FN = round (111 * CUP_DIAMETER / STAND_DIAMETER)

    body = (
        cyl (
            d = CUP_DIAMETER,
            h = CUP_HEIGHT,
            rounding2 = CUP_THICKNESS / 2,
            anchor = BOTTOM,
            _fn = FN,
        )
        -
        cyl (
            d = CUP_DIAMETER - 2 * CUP_THICKNESS,
            h = CUP_HEIGHT - CUP_THICKNESS + OVERLAP,
            rounding1 = CUP_THICKNESS / 2,
            rounding2 = - CUP_THICKNESS / 2,
            anchor = BOTTOM,
            _fn = FN,
        )
        .up (CUP_THICKNESS)
    )

    paw = import_ ('paw.svg').scale (PAW_SCALE)
    paw_round = cylindrical_extrude (id = CUP_DIAMETER - 2 * PAW_DEPTH, od = CUP_DIAMETER + 2 * PAW_DEPTH) (paw)

    PAW_COUNT_CUP = round (PAW_COUNT_RING * 2 * CUP_DIAMETER / STAND_DIAMETER)

    paw_ring = (
        zrot_copies (n = PAW_COUNT_CUP) (paw_round)
        .up (PAW_HEIGHT)
    )

    return body - paw_ring


a_stand = stand ()
a_slicer = slicer ()

a_stand.save_as_scad ('stand.scad')
a_slicer.save_as_scad ('slicer.scad')

(a_stand - a_slicer.back (SLICER_SHIFT)).save_as_scad ('sliced.scad')

cup ().save_as_scad ('cup.scad')
