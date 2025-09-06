#!/usr/bin/env python3

import math as _math

from solid2 import *
from solid2.extensions.bosl2 import *
from solid2.extensions.bosl2.threading import *

from components.common import *


set_global_fn (111)


OVERLAP = 0.001


HOSE_THICKNESS = TRE_PERIMETERS

HOSE_THREAD_DEPTH = 3.3
HOSE_THREAD_PITCH = 6
HOSE_THREAD_DIAMETER = 43
HOSE_THREAD_SHRINK = 0.6
HOSE_THREAD_LENGTH = 5 * HOSE_THREAD_PITCH
HOSE_INNER_DIAMETER = 35
HOSE_OUTER_DIAMETER = HOSE_THREAD_DIAMETER + HOSE_THICKNESS*2


ROTATOR_INNER_DIAMETER = HOSE_INNER_DIAMETER
ROTATOR_OUTER_DIAMETER = HOSE_OUTER_DIAMETER

ROTATOR_NOTCH_DEPTH = 1.2
ROTATOR_NOTCH_HEIGHT = 3.4
ROTATOR_NOTCH_WIDTH = 5
ROTATOR_NOTCH_COUNT = 7
ROTATOR_NOTCH_GAP = 0.666

ROTATOR_CUFF_THICKNESS = FOR_PERIMETERS
ROTATOR_CUFF_HEIGHT = 11
ROTATOR_CUFF_RIM = 2
ROTATOR_GAP = 0.333

ROTATOR_MIDDLE_DIAMETER = ROTATOR_INNER_DIAMETER + ROTATOR_CUFF_THICKNESS*2 + ROTATOR_GAP*2


NOSE_BODY_THICKNESS = FOR_PERIMETERS
NOSE_BLOCK_THICKNESS = TRE_PERIMETERS

NOSE_OUTER_DIAMETER = 35
NOSE_INNER_DIAMETER = NOSE_OUTER_DIAMETER - NOSE_BODY_THICKNESS*2
NOSE_NOTCH_DIAMETER = 14
NOSE_NOTCH_HEIGHT = 2
NOSE_NOTCH_OFFSET = 15.5
NOSE_BUTTON_DIAMETER = 18
NOSE_BUTTON_HEIGHT = 3.8
NOSE_BUTTON_OFFSET = 36.5
NOSE_RAILS_LENGTH = 30
NOSE_RAILS_WIDTH = 2
NOSE_RAILS_HEIGHT = 2.5
NOSE_RAILS_OFFSET = 5.5
NOSE_CUT_GAP = 0.666

NOSE_BODY_RIM = (NOSE_NOTCH_OFFSET - NOSE_NOTCH_DIAMETER/2) / 2
NOSE_BODY_HEIGHT = NOSE_BUTTON_OFFSET + NOSE_BUTTON_DIAMETER/2 + NOSE_BODY_RIM*2


def hose_connector ():

    body = (
        cyl (
            h = HOSE_THREAD_LENGTH + HOSE_THICKNESS,
            d = HOSE_OUTER_DIAMETER,
            anchor = BOTTOM,
        )
        -
        cyl (
            h = HOSE_THICKNESS + OVERLAP*2,
            d = HOSE_INNER_DIAMETER,
            anchor = BOTTOM,
        )
        .down (OVERLAP)
    )

    profile = [
        [0.05, 1],
        [0.15, 0.8],
        [0.25, 0.1],
        [0.45, 0],
    ]

    profile = (
        [ [-x, -y * HOSE_THREAD_DEPTH / HOSE_THREAD_PITCH] for (x, y) in reversed (profile) ]
        +
        [ [x, -y * HOSE_THREAD_DEPTH / HOSE_THREAD_PITCH] for (x, y) in profile ]
    )

    thread = (
        generic_threaded_rod (
            h = HOSE_THREAD_LENGTH + OVERLAP,
            d1 = HOSE_THREAD_DIAMETER - HOSE_THREAD_SHRINK,
            d2 = HOSE_THREAD_DIAMETER,
            pitch = HOSE_THREAD_PITCH,
            profile = profile,
            internal = True,
            bevel2 = True,
            blunt_start = False,
            left_handed = True,
            anchor = BOTTOM,
        )
        .up (HOSE_THICKNESS + OVERLAP)
    )

    body -= thread

    return body


def rotator_connector_upper ():

    body = (
        cyl (d = HOSE_OUTER_DIAMETER, h = ROTATOR_CUFF_HEIGHT, anchor = BOTTOM)
        -
        cyl (d = ROTATOR_MIDDLE_DIAMETER + ROTATOR_GAP, h = ROTATOR_CUFF_HEIGHT + OVERLAP*2, anchor = BOTTOM)
        .down (OVERLAP)
        -
        cyl (
            d1 = ROTATOR_MIDDLE_DIAMETER + ROTATOR_NOTCH_DEPTH*2 + ROTATOR_GAP,
            d2 = ROTATOR_MIDDLE_DIAMETER + ROTATOR_GAP,
            h = ROTATOR_NOTCH_HEIGHT,
            anchor = TOP,
        )
        .up (ROTATOR_CUFF_HEIGHT - ROTATOR_GAP)
    )

    return body


def rotator_connector_lower ():

    body = cyl (d = ROTATOR_MIDDLE_DIAMETER - ROTATOR_GAP, h = ROTATOR_CUFF_HEIGHT, anchor = BOTTOM)

    notch = (
        (
            cyl (
                d1 = ROTATOR_MIDDLE_DIAMETER + ROTATOR_NOTCH_DEPTH*2 - ROTATOR_GAP,
                d2 = ROTATOR_MIDDLE_DIAMETER - ROTATOR_GAP,
                h = ROTATOR_NOTCH_HEIGHT,
                anchor = BOTTOM,
            )
            *
            cuboid (
                [ROTATOR_NOTCH_WIDTH, ROTATOR_MIDDLE_DIAMETER/2 + ROTATOR_NOTCH_DEPTH, ROTATOR_NOTCH_HEIGHT],
                anchor = BACK + BOTTOM,
            )
        )
        .up (ROTATOR_CUFF_HEIGHT - ROTATOR_NOTCH_HEIGHT)
    )

    notch_list = [ notch.rotate (0, 0, index * 360 / ROTATOR_NOTCH_COUNT) for index in range (ROTATOR_NOTCH_COUNT) ]
    body += union () (*notch_list)

    cut = (
        (
            cuboid (
                [ROTATOR_NOTCH_WIDTH + ROTATOR_NOTCH_GAP*2, ROTATOR_MIDDLE_DIAMETER/2 + ROTATOR_NOTCH_DEPTH, ROTATOR_CUFF_HEIGHT - ROTATOR_CUFF_RIM + OVERLAP],
                anchor = BACK + BOTTOM,
            )
            -
            cuboid (
                [ROTATOR_NOTCH_WIDTH, ROTATOR_MIDDLE_DIAMETER/2 + ROTATOR_NOTCH_DEPTH + OVERLAP, ROTATOR_CUFF_HEIGHT - ROTATOR_CUFF_RIM + OVERLAP*2],
                anchor = BACK + BOTTOM,
            )
        )
        .up (ROTATOR_CUFF_RIM)
    )

    cut_list = [ cut.rotate (0, 0, index * 360 / ROTATOR_NOTCH_COUNT) for index in range (ROTATOR_NOTCH_COUNT) ]
    body -= union () (*cut_list)

    body -= cyl (d = HOSE_INNER_DIAMETER, h = ROTATOR_CUFF_HEIGHT + OVERLAP*2, anchor = BOTTOM).down (OVERLAP)

    return body


def nose_connector ():

    body = cyl (h = NOSE_BODY_HEIGHT, d = NOSE_OUTER_DIAMETER, anchor = BOTTOM)

    cut = (
        (
            cuboid ([NOSE_BUTTON_DIAMETER + NOSE_CUT_GAP*2, NOSE_OUTER_DIAMETER, NOSE_BUTTON_OFFSET - NOSE_BODY_RIM], anchor = BACK + BOTTOM)
            -
            cuboid ([NOSE_BUTTON_DIAMETER, NOSE_OUTER_DIAMETER + OVERLAP*2, NOSE_BUTTON_OFFSET - NOSE_BODY_RIM + OVERLAP*2], anchor = BACK + BOTTOM)
            .down (OVERLAP)
            .back (OVERLAP)
        )
        .up (NOSE_BODY_RIM)
        +
        (
            cyl (d = NOSE_BUTTON_DIAMETER + NOSE_CUT_GAP*2, h = NOSE_OUTER_DIAMETER, anchor = BOTTOM, orient = FWD, circum = True, spin = 30, _fn = 6)
            -
            cyl (d = NOSE_BUTTON_DIAMETER, h = NOSE_OUTER_DIAMETER + OVERLAP*2, anchor = BOTTOM, orient = FWD, circum = True, spin = 30, _fn = 6)
            .back (OVERLAP)
            -
            cuboid ([NOSE_OUTER_DIAMETER, NOSE_OUTER_DIAMETER, NOSE_OUTER_DIAMETER], anchor = BACK + TOP)
            .down (OVERLAP)
        )
        .up (NOSE_BUTTON_OFFSET)
    )

    body -= cut

    button = (
        (
            cyl (d = NOSE_BUTTON_DIAMETER, h = NOSE_OUTER_DIAMETER/2 + NOSE_BUTTON_HEIGHT, anchor = BOTTOM, orient = FWD)
            * cyl (d = NOSE_OUTER_DIAMETER + NOSE_BUTTON_HEIGHT, h = NOSE_BODY_HEIGHT)
        )
        .up (NOSE_BUTTON_OFFSET)
    )

    body += button

    notch = (
        (
            cyl (d = NOSE_NOTCH_DIAMETER, h = NOSE_OUTER_DIAMETER/2 + NOSE_NOTCH_HEIGHT, anchor = BOTTOM, orient = FWD)
            * cyl (d = NOSE_OUTER_DIAMETER + NOSE_NOTCH_HEIGHT, h = NOSE_BODY_HEIGHT)
        )
        .skew (syz = -NOSE_NOTCH_HEIGHT/NOSE_NOTCH_DIAMETER)
        .up (NOSE_NOTCH_OFFSET)
    )

    body += notch

    rail = (
        cuboid (
            [NOSE_RAILS_WIDTH, NOSE_OUTER_DIAMETER/2 + NOSE_RAILS_HEIGHT, NOSE_RAILS_LENGTH],
            rounding = NOSE_RAILS_WIDTH/2,
            edges = [ FRONT, TOP+LEFT, BOTTOM+LEFT, TOP+RIGHT, BOTTOM+RIGHT ],
            anchor = BACK + BOTTOM,
        )
        .up (NOSE_RAILS_OFFSET)
    )

    body += rail.rotateZ (+90) + rail.rotateZ (-90)

    body -= cyl (h = NOSE_BODY_HEIGHT + OVERLAP*2, d = NOSE_INNER_DIAMETER, anchor = BOTTOM).down (OVERLAP)

    central_sink_depth = NOSE_NOTCH_HEIGHT * (NOSE_BUTTON_OFFSET + NOSE_BUTTON_DIAMETER/2 / _math.cos (_math.pi / 6) - NOSE_BODY_RIM) / (NOSE_NOTCH_OFFSET + NOSE_NOTCH_DIAMETER/2 - NOSE_BODY_RIM)
    rounded_sink_depth = NOSE_OUTER_DIAMETER/2 - _math.sqrt (NOSE_OUTER_DIAMETER**2/4 - NOSE_BUTTON_DIAMETER**2/4)
    total_sink_depth = central_sink_depth + rounded_sink_depth

    block = (
        (
            cuboid (
                [ NOSE_OUTER_DIAMETER, total_sink_depth + NOSE_BLOCK_THICKNESS, NOSE_BODY_HEIGHT ],
                chamfer = total_sink_depth,
                edges = [ TOP + BACK ],
                anchor = FRONT + BOTTOM,
            )
            .fwd (NOSE_OUTER_DIAMETER/2)
            -
            cuboid (
                [ NOSE_OUTER_DIAMETER, total_sink_depth, NOSE_BODY_HEIGHT - NOSE_BLOCK_THICKNESS * (1 + _math.sqrt (2)) ],
                chamfer = total_sink_depth,
                edges = [ TOP + BACK ],
                anchor = FRONT + BOTTOM,
            )
            .fwd (NOSE_OUTER_DIAMETER/2)
            .up (NOSE_BLOCK_THICKNESS)
        )
        *
        cyl (h = NOSE_BODY_HEIGHT, d = NOSE_OUTER_DIAMETER, anchor = BOTTOM)
    )

    body += block

    return body


def combo_hose_nose_upper ():

    hose = hose_connector ()
    rotator_upper = rotator_connector_upper ()

    combo = rotator_upper.down (ROTATOR_CUFF_HEIGHT) + hose

    return combo


def combo_hose_nose_lower ():

    nose = nose_connector ()
    rotator_lower = rotator_connector_lower ()

    joint_height = max (HOSE_OUTER_DIAMETER - NOSE_OUTER_DIAMETER, HOSE_INNER_DIAMETER - NOSE_INNER_DIAMETER) / 2
    joint = (
        cyl (d1 = NOSE_OUTER_DIAMETER, d2 = HOSE_OUTER_DIAMETER, h = joint_height, anchor = BOTTOM)
        -
        cyl (d1 = NOSE_INNER_DIAMETER, d2 = HOSE_INNER_DIAMETER, h = joint_height + OVERLAP*2, anchor = BOTTOM)
        .down (OVERLAP)
    )

    combo = (nose.down (NOSE_BODY_HEIGHT) + joint).down (joint_height) + rotator_lower

    return combo


combo_hose_nose_upper ().save_as_scad ('hose_nose_upper.scad')
combo_hose_nose_lower ().save_as_scad ('hose_nose_lower.scad')
