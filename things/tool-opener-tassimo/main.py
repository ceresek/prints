#!/usr/bin/env python3

import math as _math

from solid2 import *
from solid2.extensions.bosl2 import *


set_global_fn (111)


OVERLAP = 0.001

CENTER_OUTER_DIAMETER = 13.8
CENTER_INNER_DIAMETER = 11
CENTER_OUTER_DEPTH = 4
CENTER_INNER_DEPTH = 6

CUTTER_RADIUS = 28
CUTTER_DEPTH = 4

EDGE_ANGLE = 30
EDGE_TEETH = 8
EDGE_THICKNESS = 0.42 # 1 perimeter
BLADE_THICKNESS = 1.67 # 4 perimeters

ARM_LENGTH = 55
ARM_WIDTH = 16
ARM_CHAMFER = 0.3
ARM_THICKNESS = 3

THUMB_DIAMETER = 22

STRIPE_WIDTH = 2
STRIPE_COUNT = 7
STRIPE_THICKNESS = 0.4 # 2 layers


def _tooth (inner_radius, outer_radius, depth, edge_angle, body_angle):

    tooth_width = outer_radius - inner_radius
    edge_height = tooth_width / _math.tan (_math.radians (abs (edge_angle)))

    if (edge_angle > 0):
        # Positive angle means sharp outer edge.
        tooth_path = [[inner_radius, 0], [outer_radius, 0], [outer_radius, depth], [outer_radius - EDGE_THICKNESS, depth], [inner_radius, depth - edge_height]]
    else:
        # Negative angle means sharp inner edge.
        tooth_path = [[inner_radius, 0], [outer_radius, 0], [outer_radius, depth - edge_height], [inner_radius + EDGE_THICKNESS, depth], [inner_radius, depth]]

    tooth_base = rotate_sweep (tooth_path, body_angle / 2)

    slant_length = outer_radius * _math.sin (_math.radians (body_angle) / 2)

    tooth_upper = tooth_base.skew (szy = 0 - edge_height / slant_length)
    tooth_lower = tooth_upper.mirror ([ 0, 1, 0])

    tooth_body = (tooth_upper + tooth_lower) * cuboid ([outer_radius, outer_radius, depth], anchor = LEFT + BOTTOM)

    return tooth_body


def _teeth (inner_radius, outer_radius, depth, edge_angle, count):

    tooth = _tooth (inner_radius, outer_radius, depth, edge_angle, 360 / count)
    teeth = tooth.zrot_copies (n = count)

    return teeth


def _opener ():

    arm = (
        cyl (
            d = THUMB_DIAMETER, h = ARM_THICKNESS,
            chamfer = ARM_CHAMFER,
            anchor = TOP,
        )
        +
        cuboid (
            [ ARM_LENGTH, ARM_WIDTH, ARM_THICKNESS ],
            edges = [ FRONT + BOTTOM, FRONT + TOP, BACK + BOTTOM, BACK + TOP ],
            chamfer = ARM_CHAMFER,
            anchor = TOP,
        )
        .right (ARM_LENGTH / 2)
        +
        cyl (
            d = ARM_WIDTH, h = ARM_THICKNESS,
            chamfer = ARM_CHAMFER,
            anchor = TOP,
        )
        .right (ARM_LENGTH)
    )

    middle = (
        cyl (
            d = CENTER_INNER_DIAMETER, h = CENTER_INNER_DEPTH - BLADE_THICKNESS,
            anchor = BOTTOM,
        )
        +
        cyl (
            d1 = CENTER_INNER_DIAMETER,
            d2 = CENTER_INNER_DIAMETER - 2 * BLADE_THICKNESS + 2 * EDGE_THICKNESS,
            h = BLADE_THICKNESS,
            anchor = BOTTOM,
        )
        .up (CENTER_INNER_DEPTH - BLADE_THICKNESS)
        -
        cyl (
            d = CENTER_INNER_DIAMETER - 2 * BLADE_THICKNESS, h = CENTER_INNER_DEPTH + OVERLAP,
            anchor = BOTTOM,
        )
    )

    teeth = _teeth (
        CENTER_OUTER_DIAMETER / 2,
        CENTER_OUTER_DIAMETER / 2 + BLADE_THICKNESS,
        CENTER_OUTER_DEPTH,
        0 - EDGE_ANGLE,
        EDGE_TEETH,
    )

    CUTTER_ANGLE = _math.degrees (_math.atan ((ARM_WIDTH / 2 - ARM_CHAMFER) / CUTTER_RADIUS)) * 2

    cutter = _tooth (CUTTER_RADIUS - BLADE_THICKNESS, CUTTER_RADIUS, CUTTER_DEPTH, EDGE_ANGLE, CUTTER_ANGLE)

    stripes = (
        cuboid ([STRIPE_WIDTH, ARM_WIDTH + 2 * OVERLAP, STRIPE_THICKNESS + OVERLAP], anchor = BOTTOM)
        .skew (sxy = 1)
        .xcopies (n = STRIPE_COUNT, spacing = 0 - STRIPE_WIDTH * 2, sp = [ARM_LENGTH + ARM_WIDTH / 2 - STRIPE_WIDTH * 3/2, 0, 0])
        .down (ARM_THICKNESS + OVERLAP)
    )

    return arm + middle + teeth + cutter - stripes


_opener ().save_as_scad ('opener.scad')
