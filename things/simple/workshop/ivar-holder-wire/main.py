#!/usr/bin/env python3

import math as _math

from solid2 import *
from solid2.extensions.bosl2 import *

from components.common import *

from helpers import ivar


set_global_fn (111)


OVERLAP = 0.001

BODY_HEIGHT = ivar.PIN_DISTANCE_VERTICAL + ivar.PIN_RADIUS_SMALL * 2
BODY_CHAMFER = 2

PIN_GAP = 0.33
PIN_TIP = 2.22
PIN_DEPTH = 3.33

CATCH_SLACK = 0.2
CATCH_CATCH = 5.5
CATCH_CHAMFER = 0.3
CATCH_THICKNESS = 5.5

CATCH_OVERHANG = 66
CATCH_WIDTH = ivar.PIN_RADIUS_SMALL * _math.sin (_math.radians (CATCH_OVERHANG)) * 2

WIRE_DIAMETER_ONE = 4.66
WIRE_DIAMETER_TWO = 6.66

WIRE_HOLE_CHAMFER = 1
WIRE_HOLE_WIDTH = 8
WIRE_HOLE_DEPTH = 16
WIRE_SLOT_CHAMFER = 0.8
WIRE_SLOT_DEPTH = 8
WIRE_GAP = 2.88


def wire (diameter):

    body = (
        (
            cyl (
                h = BODY_HEIGHT - WIRE_HOLE_DEPTH + OVERLAP * 2,
                d = diameter,
                chamfer2 = 0 - WIRE_HOLE_CHAMFER,
                anchor = BOTTOM,
            )
            +
            cuboid (
                [
                    diameter,
                    BODY_HEIGHT + OVERLAP * 2,
                    WIRE_SLOT_DEPTH + OVERLAP
                ],
                edges = [TOP + LEFT, TOP + RIGHT],
                chamfer = 0 - WIRE_SLOT_CHAMFER,
                anchor = FRONT + TOP,
                orient = FWD,
            )
            .fwd (WIRE_SLOT_DEPTH)
        )
        .fwd (ivar.STAND_PIN_HOLE_TO_EDGE - WIRE_SLOT_DEPTH + OVERLAP)
        .down (OVERLAP)
    )

    return body


def comb (hole_size_list):

    slot_length = ivar.STAND_RUNG_LENGTH / 2 - CATCH_THICKNESS - CATCH_CATCH - WIRE_GAP

    wire_list = []
    wire_index = 0
    wire_position = 0 - WIRE_GAP / 2 - hole_size_list [0] / 2
    while wire_position < slot_length - hole_size_list [wire_index]:
        wire_position += WIRE_GAP / 2 + hole_size_list [wire_index] / 2
        wire_list.append (wire (hole_size_list [wire_index]).left (wire_position))
        wire_position += hole_size_list [wire_index] / 2 + WIRE_GAP / 2
        wire_index = (wire_index + 1) % len (hole_size_list)
    wire_hole = union () (wire_list)

    wire_slot = (
        (
            cuboid (
                [
                    slot_length,
                    WIRE_HOLE_WIDTH,
                    WIRE_HOLE_DEPTH / 2 + OVERLAP
                ],
                edges = [TOP + LEFT, TOP + FRONT, TOP + BACK],
                chamfer = 0 - WIRE_SLOT_CHAMFER,
                anchor = BOTTOM + RIGHT,
            )
            .up (BODY_HEIGHT - WIRE_HOLE_DEPTH / 2)
            +
            cuboid (
                [
                    slot_length,
                    WIRE_HOLE_WIDTH,
                    WIRE_HOLE_DEPTH / 2 + OVERLAP
                ],
                edges = [BOTTOM + LEFT, BOTTOM + FRONT, BOTTOM + BACK],
                chamfer = WIRE_SLOT_CHAMFER,
                anchor = BOTTOM + RIGHT,
            )
            .up (BODY_HEIGHT - WIRE_HOLE_DEPTH)
        )
        .right (OVERLAP)
    )

    return wire_hole + wire_slot


def catch ():

    pin_body = (
        (
            cyl (
                h = PIN_TIP + PIN_DEPTH + OVERLAP,
                r = ivar.PIN_RADIUS_SMALL,
                chamfer2 = PIN_TIP,
                anchor = BOTTOM,
                orient = LEFT,
            )
            &
            cuboid (
                [
                    PIN_TIP + PIN_DEPTH + OVERLAP,
                    CATCH_WIDTH,
                    ivar.PIN_RADIUS_SMALL * 2
                ],
                anchor = RIGHT,
            )
        )
        .right (OVERLAP)
        .up (ivar.PIN_RADIUS_SMALL)
    )

    pin_twin = pin_body + pin_body.up (ivar.PIN_DISTANCE_VERTICAL)

    bar_body = (
        cuboid (
            [CATCH_THICKNESS, CATCH_WIDTH, BODY_HEIGHT],
            edges = [RIGHT + FRONT, RIGHT + BACK, TOP + RIGHT],
            chamfer = CATCH_CHAMFER,
            anchor = LEFT + BOTTOM,
        )
        +
        cuboid (
            [CATCH_THICKNESS + CATCH_CATCH, CATCH_WIDTH, CATCH_CATCH + OVERLAP],
            edges = [RIGHT + TOP, RIGHT + FRONT, RIGHT + BACK],
            chamfer = CATCH_CHAMFER,
            anchor = LEFT + BOTTOM,
        )
    )

    return pin_twin + bar_body


def holder (hole_size_list):

    catch_hole = (
        (
            cuboid (
                [
                    CATCH_THICKNESS + CATCH_SLACK + OVERLAP,
                    CATCH_WIDTH + CATCH_SLACK,
                    BODY_HEIGHT + OVERLAP * 2
                ],
                anchor = LEFT + BOTTOM,
            )
            +
            cuboid (
                [
                    CATCH_THICKNESS + CATCH_CATCH + CATCH_SLACK + OVERLAP,
                    CATCH_WIDTH + CATCH_SLACK * 2,
                    CATCH_CATCH + OVERLAP
                ],
                anchor = LEFT + BOTTOM,
            )
        )
        .down (OVERLAP)
        .left (OVERLAP)
        .left (ivar.STAND_RUNG_LENGTH / 2)
    )

    body = (
        cuboid (
            [ivar.STAND_RUNG_LENGTH / 2, ivar.STAND_PIN_HOLE_TO_EDGE * 2, BODY_HEIGHT],
            edges = [LEFT+BACK, LEFT+FRONT, FRONT+TOP, BACK+TOP, FRONT+BOTTOM, BACK+BOTTOM],
            chamfer = BODY_CHAMFER,
            anchor = RIGHT + BOTTOM,
        )
    )

    half = body - catch_hole - comb (hole_size_list)
    full = half + half.mirrorX ()

    return full


catch ().save_as_scad ('catch.scad')

holder ([WIRE_DIAMETER_ONE]).save_as_scad ('holder_one.scad')
holder ([WIRE_DIAMETER_TWO]).save_as_scad ('holder_two.scad')
holder ([WIRE_DIAMETER_TWO, WIRE_DIAMETER_ONE]).save_as_scad ('holder_one_two.scad')
holder ([WIRE_DIAMETER_TWO, WIRE_DIAMETER_ONE, WIRE_DIAMETER_ONE]).save_as_scad ('holder_one_one_two.scad')
