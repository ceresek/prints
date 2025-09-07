#!/usr/bin/env python3

import math as _math

from solid2 import *
from solid2.extensions.bosl2 import *


set_global_fn (111)


OVERLAP = 0.008

RADIO_DIAMETER = 63.2
RADIO_CIRCUMFERENCE = 112

SCREEN_POSITION = -18

LEG_SMALL_POSITION = -4
LEG_SMALL_DIAMETER = 9
LEG_SMALL_HEIGHT = 4

LEG_SMALL_SHIFT_ONE = 0
LEG_SMALL_SHIFT_TWO = 3

LEG_LARGE_POSITION = 30
LEG_LARGE_DIAMETER = 12.8
LEG_LARGE_HEIGHT = 7

CLASP_WIDTH = 17.5
CLASP_LENGTH = 55
CLASP_THICKNESS = 5.555

RING_THICKNESS = 3.333
RING_WIDTH = LEG_LARGE_DIAMETER + 2 * RING_THICKNESS


def holder (leg_small_shift):

    WHOLE_CIRCUMFERENCE = _math.pi * RADIO_DIAMETER
    WEDGE_ANGLE = 360 * (1 - RADIO_CIRCUMFERENCE / WHOLE_CIRCUMFERENCE)
    SCREEN_ANGLE = 360 * SCREEN_POSITION / WHOLE_CIRCUMFERENCE
    LEG_SMALL_ANGLE = 360 * LEG_SMALL_POSITION / WHOLE_CIRCUMFERENCE
    LEG_LARGE_ANGLE = 360 * LEG_LARGE_POSITION / WHOLE_CIRCUMFERENCE

    ring = (
        cyl (
            d = RADIO_DIAMETER + 2 * RING_THICKNESS,
            h = RING_WIDTH,
            chamfer = RING_THICKNESS / 2,
            anchor = BOTTOM,
        )
        -
        cyl (
            d = RADIO_DIAMETER,
            h = RING_WIDTH + 2 * OVERLAP,
            anchor = BOTTOM,
        )
        .down (OVERLAP)
    )

    wedge = (
        pie_slice (
            d = RADIO_DIAMETER + 2 * RING_THICKNESS + 2 * OVERLAP,
            h = RING_WIDTH + 2 * OVERLAP,
            ang = WEDGE_ANGLE,
            anchor = BOTTOM,
        )
        .down (OVERLAP)
        .zrot (0 - SCREEN_ANGLE)
        +
        cube (RING_WIDTH + 2 * OVERLAP, anchor = LEFT + FRONT + BOTTOM)
        .down (OVERLAP)
        .fwd (RING_THICKNESS)
        .zrot (45)
        .right (RADIO_DIAMETER / 2 + RING_THICKNESS / 2)
        .zrot (0 - SCREEN_ANGLE)
        +
        cube (RING_WIDTH + 2 * OVERLAP, anchor = RIGHT + FRONT + BOTTOM)
        .down (OVERLAP)
        .fwd (RING_THICKNESS)
        .zrot (0 - 45)
        .left (RADIO_DIAMETER / 2 + RING_THICKNESS / 2)
        .zrot (180 + WEDGE_ANGLE - SCREEN_ANGLE)
    )

    leg_small_hole = (
        xcyl (
            d = LEG_SMALL_DIAMETER,
            h = RADIO_DIAMETER / 2 + LEG_SMALL_HEIGHT,
            anchor = LEFT,
        )
        .up (RING_WIDTH / 2 + leg_small_shift)
        .zrot (0 - LEG_SMALL_ANGLE)
    )

    leg_large_hole = (
        xcyl (
            d = LEG_LARGE_DIAMETER,
            h = RADIO_DIAMETER / 2 + LEG_LARGE_HEIGHT,
            anchor = LEFT,
        )
        .up (RING_WIDTH / 2)
        .zrot (0 - LEG_LARGE_ANGLE)
    )

    clasp = (
        cuboid (
            [2 * CLASP_THICKNESS + CLASP_LENGTH, CLASP_WIDTH + 2 * CLASP_THICKNESS, RING_WIDTH],
            chamfer = RING_THICKNESS / 2,
            _except = LEFT,
            anchor = LEFT + BOTTOM,
        )
        .right (RADIO_DIAMETER / 2 - CLASP_THICKNESS)
        -
        cuboid (
            [CLASP_LENGTH + OVERLAP, CLASP_WIDTH, RING_WIDTH + 2 * OVERLAP],
            anchor = LEFT + BOTTOM,
        )
        .down (OVERLAP)
        .right (RADIO_DIAMETER / 2 + CLASP_THICKNESS)
        -
        cyl (
            d = RADIO_DIAMETER,
            h = RING_WIDTH + 2 * OVERLAP,
            anchor = BOTTOM,
        )
        .down (OVERLAP)
    )

    return ring - wedge + clasp - leg_small_hole - leg_large_hole


holder (LEG_SMALL_SHIFT_ONE).save_as_scad ('holder_one.scad')
holder (LEG_SMALL_SHIFT_TWO).save_as_scad ('holder_two.scad')
