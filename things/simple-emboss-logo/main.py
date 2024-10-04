#!/usr/bin/env python3

import math as _math

from solid2 import *
from solid2.extensions.bosl2 import *


set_global_fn (111)


OVERLAP = 0.01

ROLLER_HOLE_SIZE = 12
ROLLER_HOLE_DEPTH = 11
ROLLER_HOLE_CHAMFER = 1

ROLLER_HEIGHT = 60
ROLLER_ROUNDING = 1
ROLLER_DIAMETER = 30.3

EMBOSS_DEPTH = 1.2
EMBOSS_SLACK = 0.3


def roller ():

    body = (
        cyl (
            h = ROLLER_HEIGHT,
            d = ROLLER_DIAMETER,
            rounding = ROLLER_ROUNDING,
            anchor = CENTER,
        )
        -
        cuboid (
            [ROLLER_HOLE_SIZE, ROLLER_HOLE_SIZE, ROLLER_HOLE_DEPTH + OVERLAP],
            chamfer = 0 - ROLLER_HOLE_CHAMFER,
            edges = TOP,
            anchor = TOP,
        )
        .up (ROLLER_HEIGHT / 2 + OVERLAP)
        -
        cuboid (
            [ROLLER_HOLE_SIZE, ROLLER_HOLE_SIZE, ROLLER_HOLE_DEPTH + OVERLAP],
            chamfer = 0 - ROLLER_HOLE_CHAMFER,
            edges = BOTTOM,
            anchor = BOTTOM,
        )
        .down (ROLLER_HEIGHT / 2 + OVERLAP)
    )

    return body


def patterned_rollers (logo):

    # Extrusion preserves the pattern at outer diameter.
    # We need to preserve the pattern at roller surface.
    # Hence we stretch to compensage.
    logo_stretch = (ROLLER_DIAMETER + EMBOSS_DEPTH * 2) / ROLLER_DIAMETER
    logo_positive = logo.scale ([logo_stretch, 1])
    logo_negative = logo_positive.offset (EMBOSS_SLACK)

    # Since extrusion over different diameters stretches the pattern differently,
    # we extrude both positive and negative pattern with the same diameters.
    logo_positive = cylindrical_extrude (id = ROLLER_DIAMETER - EMBOSS_DEPTH * 2, od = ROLLER_DIAMETER + EMBOSS_DEPTH * 2) (logo_positive)
    logo_negative = cylindrical_extrude (id = ROLLER_DIAMETER - EMBOSS_DEPTH * 2, od = ROLLER_DIAMETER + EMBOSS_DEPTH * 2) (logo_negative).mirror (1, 0, 0)

    roller_positive = roller () + logo_positive ()
    roller_negative = roller () - logo_negative ()

    return roller_positive.left (ROLLER_DIAMETER) + roller_negative.right (ROLLER_DIAMETER)


def logo_mifri ():

    logo = import_ ('logo-mifri.svg').scale (1).offset (0.3).back (12)

    return logo


roller ().save_as_scad ('roller.scad')

patterned_rollers (logo_mifri ()).save_as_scad ('roller-mifri.scad')
