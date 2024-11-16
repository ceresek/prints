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

EMBOSS_DEPTH_ROLLER = 1.2
EMBOSS_SLACK_ROLLER = 0.3

PRESSER_DIAMETER = 44.4
PRESSER_THICKNESS = 3
PRESSER_BOTTOM_HOLE_DISTANCE = 18
PRESSER_BOTTOM_HOLE_DIAMETER = 6.2
PRESSER_BOTTOM_HOLE_DEPTH = 2
PRESSER_TOP_HOLE_DISTANCE = 12
PRESSER_TOP_HOLE_DIAMETER = 3.8
PRESSER_TOP_HOLE_DEPTH = 2
PRESSER_ARM_WIDTH = 22
PRESSER_HOLE_SLANT = 0.3

PLATE_BOTTOM_THICKNESS = 1.2
PLATE_SIDE_THICKNESS = 2.08 # 3 perimeters
PLATE_CATCH_GAP = 1
PLATE_CATCH_WIDTH = 3
PLATE_CATCH_DEPTH = 0.3
PLATE_CATCH_HEIGHT = 3
PLATE_CATCH_CHAMFER = 1.8

EMBOSS_DEPTH_PRESSER = 0.6
EMBOSS_SLACK_PRESSER = 0.38


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
    logo_stretch = (ROLLER_DIAMETER + EMBOSS_DEPTH_ROLLER * 2) / ROLLER_DIAMETER
    logo_positive = logo.scale ([logo_stretch, 1])
    logo_negative = logo_positive.offset (EMBOSS_SLACK_ROLLER)

    # Since extrusion over different diameters stretches the pattern differently,
    # we extrude both positive and negative pattern with the same diameters.
    logo_positive = cylindrical_extrude (id = ROLLER_DIAMETER - EMBOSS_DEPTH_ROLLER * 2, od = ROLLER_DIAMETER + EMBOSS_DEPTH_ROLLER * 2) (logo_positive)
    logo_negative = cylindrical_extrude (id = ROLLER_DIAMETER - EMBOSS_DEPTH_ROLLER * 2, od = ROLLER_DIAMETER + EMBOSS_DEPTH_ROLLER * 2) (logo_negative).mirror (1, 0, 0)

    roller_positive = roller () + logo_positive ()
    roller_negative = roller () - logo_negative ()

    return roller_positive.left (ROLLER_DIAMETER) + roller_negative.right (ROLLER_DIAMETER)


def patterned_pressers (logo):

    body = (
        cyl (
            h = PLATE_BOTTOM_THICKNESS + PRESSER_THICKNESS + PLATE_CATCH_HEIGHT,
            d = PRESSER_DIAMETER + PLATE_SIDE_THICKNESS * 2,
            anchor = BOTTOM,
        )
        .down (PLATE_BOTTOM_THICKNESS)
        -
        cyl (
            h = PRESSER_THICKNESS + PLATE_CATCH_HEIGHT + OVERLAP,
            d = PRESSER_DIAMETER,
            chamfer2 = 0 - PLATE_CATCH_CHAMFER,
            anchor = BOTTOM,
        )
        -
        cuboid (
            [ PRESSER_ARM_WIDTH, PRESSER_DIAMETER, PRESSER_THICKNESS + PLATE_CATCH_HEIGHT + OVERLAP ],
            anchor = BACK + BOTTOM,
        )
    )

    bars = (
        cuboid (
            [ PRESSER_DIAMETER + PLATE_SIDE_THICKNESS * 2 + OVERLAP, PLATE_CATCH_GAP, PRESSER_THICKNESS + PLATE_CATCH_HEIGHT + OVERLAP ],
            anchor = FRONT + BOTTOM,
        )
        .back (PLATE_CATCH_WIDTH / 2)
        +
        cuboid (
            [ PRESSER_DIAMETER + PLATE_SIDE_THICKNESS * 2 + OVERLAP, PLATE_CATCH_GAP, PRESSER_THICKNESS + PLATE_CATCH_HEIGHT + OVERLAP ],
            anchor = BACK + BOTTOM,
        )
        .fwd (PLATE_CATCH_WIDTH / 2)
    )

    body -= bars.rotateZ (0 + 45)
    body -= bars.rotateZ (0 - 45)

    pins = (
        cyl (
            h = PLATE_CATCH_WIDTH,
            r = PLATE_CATCH_DEPTH,
        )
        .rotateX (90)
        .left (PRESSER_DIAMETER / 2)
        .up (PRESSER_THICKNESS + PLATE_CATCH_DEPTH)
        +
        cyl (
            h = PLATE_CATCH_WIDTH,
            r = PLATE_CATCH_DEPTH,
        )
        .rotateX (90)
        .right (PRESSER_DIAMETER / 2)
        .up (PRESSER_THICKNESS + PLATE_CATCH_DEPTH)
    )

    body += pins.rotateZ (0 + 45)
    body += pins.rotateZ (0 - 45)

    body_positive = (
        body
        +
        cyl (
            h = PRESSER_TOP_HOLE_DEPTH,
            d1 = PRESSER_TOP_HOLE_DIAMETER,
            d2 = PRESSER_TOP_HOLE_DIAMETER - PRESSER_HOLE_SLANT,
            anchor = BOTTOM,
        )
        .fwd (PRESSER_TOP_HOLE_DISTANCE)
    )

    body_negative = (
        body
        +
        cyl (
            h = PRESSER_BOTTOM_HOLE_DEPTH,
            d1 = PRESSER_BOTTOM_HOLE_DIAMETER,
            d2 = PRESSER_BOTTOM_HOLE_DIAMETER - PRESSER_HOLE_SLANT,
            anchor = BOTTOM,
        )
        .left (PRESSER_BOTTOM_HOLE_DISTANCE / 2)
        +
        cyl (
            h = PRESSER_BOTTOM_HOLE_DEPTH,
            d1 = PRESSER_BOTTOM_HOLE_DIAMETER,
            d2 = PRESSER_BOTTOM_HOLE_DIAMETER - PRESSER_HOLE_SLANT,
            anchor = BOTTOM,
        )
        .right (PRESSER_BOTTOM_HOLE_DISTANCE / 2)
    )

    logo_positive = linear_extrude (EMBOSS_DEPTH_PRESSER) (logo).down (PLATE_BOTTOM_THICKNESS + EMBOSS_DEPTH_PRESSER)
    logo_negative = linear_extrude (EMBOSS_DEPTH_PRESSER) (logo.offset (EMBOSS_SLACK_ROLLER)).mirror (1, 0, 0).down (PLATE_BOTTOM_THICKNESS + OVERLAP)

    body_positive += logo_positive
    body_negative -= logo_negative

    return body_positive.left (PRESSER_DIAMETER) + body_negative.right (PRESSER_DIAMETER)


roller ().save_as_scad ('roller.scad')

logo_mifri_roller = import_ ('logo-mifri.svg').offset (0.3).back (12.34).scale (1)
patterned_rollers (logo_mifri_roller).save_as_scad ('roller-mifri.scad')

logo_mifri_presser = import_ ('logo-mifri.svg').offset (0.3).back (12.34).left (20.1).scale (0.93)
patterned_pressers (logo_mifri_presser).save_as_scad ('presser-mifri.scad')
