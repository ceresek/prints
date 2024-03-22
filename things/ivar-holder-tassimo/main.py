#!/usr/bin/env python3

import math as _math

from solid2 import *

from helpers.ivar import *


set_global_fn (33)


OVERLAP = 0.001

CLASP_WIDTH = 8
CLASP_THICKNESS = 3.3

HOOK_EDGE_DISTANCE = 10
HOOK_HOOK_DISTANCE = 53
EDGE_EDGE_DISTANCE = HOOK_EDGE_DISTANCE + HOOK_HOOK_DISTANCE + HOOK_EDGE_DISTANCE

HOOK_BASE_RADIUS = 10 / 2
HOOK_WIDE_RADIUS = HOOK_BASE_RADIUS + 0.33
HOOK_TIPS_RADIUS = 3.33

HOOK_LENGTH_BOTTOM = 2
HOOK_LENGTH_MIDDLE = 1
HOOK_LENGTH_TOP = 2
HOOK_LENGTH = HOOK_LENGTH_BOTTOM + HOOK_LENGTH_MIDDLE + HOOK_LENGTH_TOP

CATCH_BEND = 0.666
CATCH_SPACE = 0.666
CATCH_LENGTH = 10
CATCH_DISTANCE = EDGE_EDGE_DISTANCE / 2 - CATCH_LENGTH / 2


def hook ():

    hook = (
        cylinder (HOOK_LENGTH_BOTTOM, r1 = HOOK_BASE_RADIUS, r2 = HOOK_WIDE_RADIUS) +
        cylinder (HOOK_LENGTH_MIDDLE, r = HOOK_WIDE_RADIUS).up (HOOK_LENGTH_BOTTOM) +
        cylinder (HOOK_LENGTH_TOP, r1 = HOOK_WIDE_RADIUS, r2 = HOOK_TIPS_RADIUS).up (HOOK_LENGTH_BOTTOM + HOOK_LENGTH_MIDDLE)
    ) * (
        cube (HOOK_WIDE_RADIUS * 2, CLASP_WIDTH, HOOK_LENGTH)
            .left (HOOK_WIDE_RADIUS)
            .back (CLASP_WIDTH / 2)
    )

    return hook


def clasp_base (shelf_height):

    catch_slope_cross_height = CATCH_BEND + CATCH_SPACE + CLASP_THICKNESS

    catch_slope_cross_length = _math.sqrt (catch_slope_cross_height**2 + CATCH_DISTANCE**2)
    catch_slope_real_length = _math.sqrt (catch_slope_cross_length**2 - CLASP_THICKNESS**2)

    catch_slope_cross_angle = _math.asin (catch_slope_cross_height / catch_slope_cross_length)
    catch_slope_delta_angle = _math.asin (CLASP_THICKNESS / catch_slope_cross_length)
    catch_slope_real_angle = catch_slope_cross_angle - catch_slope_delta_angle

    clasp = (
        (
            cube (CLASP_THICKNESS + EDGE_EDGE_DISTANCE, CLASP_WIDTH, CLASP_THICKNESS)
                .left (CLASP_THICKNESS)
                .down (CLASP_THICKNESS) +
            cube (CLASP_THICKNESS, CLASP_WIDTH, CLASP_THICKNESS + shelf_height + CATCH_SPACE + CLASP_THICKNESS)
                .left (CLASP_THICKNESS)
                .down (CLASP_THICKNESS) +
            cube (catch_slope_real_length, CLASP_WIDTH, CLASP_THICKNESS)
                .down (CLASP_THICKNESS)
                .rotate (0, _math.degrees (catch_slope_real_angle), 0)
                .up (CLASP_THICKNESS + shelf_height + CATCH_SPACE)
        )
        .back (CLASP_WIDTH / 2)
    )

    hooks = (
        (
            hook ().right (HOOK_EDGE_DISTANCE) +
            hook ().right (HOOK_EDGE_DISTANCE + HOOK_HOOK_DISTANCE)
        )
        .rotate (180, 0, 0)
        .down (CLASP_THICKNESS)
    )

    return clasp + hooks


def holder_single (shelf_height):

    holder = (
        clasp_base (shelf_height) +
        cube (CATCH_LENGTH, CLASP_WIDTH, CLASP_THICKNESS)
            .right (CATCH_DISTANCE)
            .up (shelf_height - CATCH_BEND)
            .back (CLASP_WIDTH/2)
    )

    return holder


def holder_double (shelf_height):

    holder = (
        clasp_base (shelf_height) +
        cube (EDGE_EDGE_DISTANCE - CATCH_DISTANCE, CLASP_WIDTH, CLASP_THICKNESS)
            .right (CATCH_DISTANCE)
            .up (shelf_height - CATCH_BEND)
            .back (CLASP_WIDTH/2) +
        hook ()
            .right (EDGE_EDGE_DISTANCE - HOOK_EDGE_DISTANCE)
            .up (shelf_height + CLASP_THICKNESS - CATCH_BEND)
    )

    return holder


# Main

holder_single (SHELF_HEIGHT).save_as_scad ('holder_single.scad')
holder_double (SHELF_HEIGHT).save_as_scad ('holder_double.scad')
