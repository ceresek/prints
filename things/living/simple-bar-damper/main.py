#!/usr/bin/env python3

import math as _math

from solid2 import *
from solid2.extensions.bosl2 import *


set_global_fn (111)


OVERLAP = 0.01


DAMPER_THICKNESS_NORMAL = 1.67 # 4 perimeters
DAMPER_THICKNESS_STRONG = 3.30 # 8 perimeters

UPPER_WIDTH = 26
UPPER_LENGTH = 20
UPPER_CHAMFER = 1
UPPER_DIAMETER = 39
UPPER_THICKNESS = 5.5

LOWER_WIDTH = 30
LOWER_LENGTH = 20
LOWER_CHAMFER = 0
LOWER_DIAMETER = 39
LOWER_THICKNESS = 3.5


def damper (width, length, chamfer, diameter, thickness):

    arc = (
        cyl (
            h = width + DAMPER_THICKNESS_NORMAL * 2,
            d = diameter,
            anchor = CENTER,
        )
        -
        cyl (
            h = width + DAMPER_THICKNESS_NORMAL * 2 + OVERLAP * 2,
            d = diameter - DAMPER_THICKNESS_STRONG * 2,
            anchor = CENTER,
        )
        .down (OVERLAP)
        -
        cuboid (
            [
                diameter,
                diameter,
                width + DAMPER_THICKNESS_NORMAL * 2 + OVERLAP * 2
            ],
            edges = [ BACK + LEFT, BACK + RIGHT ],
            anchor = BACK,
        )
        .fwd (DAMPER_THICKNESS_STRONG - DAMPER_THICKNESS_NORMAL)
        .down (OVERLAP)
        -
        cuboid (
            [
                diameter - DAMPER_THICKNESS_STRONG * 2 + DAMPER_THICKNESS_NORMAL * 2,
                diameter,
                width + DAMPER_THICKNESS_NORMAL * 2 + OVERLAP * 2
            ],
            edges = [ BACK + LEFT, BACK + RIGHT ],
            chamfer = DAMPER_THICKNESS_STRONG - DAMPER_THICKNESS_NORMAL,
            anchor = BACK,
        )
        .down (OVERLAP)
    )

    leg = (
        cuboid (
            [
                thickness + DAMPER_THICKNESS_NORMAL * 2,
                length,
                width + DAMPER_THICKNESS_NORMAL * 2
            ],
            anchor = BACK,
        )
        -
        cuboid (
            [
                thickness,
                length + OVERLAP * 2,
                width
            ],
            _except = [ FRONT, BACK ],
            chamfer = chamfer,
            anchor = BACK,
        )
        .back (OVERLAP)
    )

    leg_left = leg.left (diameter / 2 + thickness / 2)
    leg_right = leg.right (diameter / 2 + thickness / 2)

    body = arc + leg_left + leg_right

    return body


damper (UPPER_WIDTH, UPPER_LENGTH, UPPER_CHAMFER, UPPER_DIAMETER, UPPER_THICKNESS).save_as_scad ('upper.scad')
damper (LOWER_WIDTH, LOWER_LENGTH, LOWER_CHAMFER, LOWER_DIAMETER, LOWER_THICKNESS).save_as_scad ('lower.scad')
