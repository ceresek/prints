#!/usr/bin/env python3

import math as _math

from solid2 import *
from solid2.extensions.bosl2 import *

from components.common import *


set_global_fn (111)


OVERLAP = 0.01


BAR_DIAMETER_SMALL = 14.5
BAR_DIAMETER_LARGE = 18.2
BAR_SINK = 7

BOWL_DEPTH = 80
BOWL_WIDTH = 120
BOWL_LENGTH = 90
BOWL_CHAMFER = 11
BOWL_THICKNESS = SIX_PERIMETERS

LID_BRIM = 16
LID_CATCH = 8
LID_SLACK = 0.3
LID_SHIELD_INNER = 8
LID_SHIELD_OUTER = 16
LID_ROUNDING = 11
LID_THICKNESS = SIX_PERIMETERS

NOTCH_SINK = 2
NOTCH_WIDTH = 11
NOTCH_DEPTH = 0.666

HOOK_ANGLE = 38
HOOK_WIDTH = 16
HOOK_SLACK = 0.25
HOOK_CATCH = 20
HOOK_THICKNESS = EIT_PERIMETERS
HOOK_CHAMFER = BAR_SINK - HOOK_THICKNESS - ONE_PERIMETER * 2


def hook (bar_diameter):

    body = (
        # Hook base body ...
        pie_slice (
            h = HOOK_WIDTH,
            d = bar_diameter + HOOK_THICKNESS * 2,
            ang = 180 + HOOK_ANGLE,
            anchor = CENTER,
        )
        .rotate ([ 0, 0, 0 - HOOK_ANGLE ])
        +
        cuboid (
            [
                BAR_SINK + bar_diameter / 2,
                bar_diameter / 2 + HOOK_THICKNESS,
                HOOK_WIDTH
            ],
            anchor = RIGHT + FRONT,
        )
        +
        cuboid (
            [
                BAR_SINK,
                HOOK_CATCH - HOOK_THICKNESS - bar_diameter / 2 + BAR_SINK,
                HOOK_WIDTH
            ],
            chamfer = BAR_SINK,
            edges = [ RIGHT + FRONT ],
            anchor = RIGHT + BACK,
        )
        .left (bar_diameter / 2)
        -
        # Pipe hole ...
        cyl (h = HOOK_WIDTH + OVERLAP * 2, d = bar_diameter)
    )

    catch_upper = (
        cuboid (
            [
                HOOK_CHAMFER + ONE_PERIMETER,
                HOOK_CATCH + OVERLAP,
                HOOK_CHAMFER + ONE_PERIMETER + OVERLAP
            ],
            chamfer = HOOK_CHAMFER,
            edges = [ LEFT + BOTTOM, FRONT + BOTTOM ],
            anchor = RIGHT + BACK + BOTTOM,
        )
        .left (bar_diameter / 2 + HOOK_THICKNESS)
        .back (bar_diameter / 2 + HOOK_THICKNESS + OVERLAP)
        .up (HOOK_WIDTH / 2 - HOOK_CHAMFER + OVERLAP)
    )

    catch_lower = catch_upper.mirror ([0, 0, 1])

    body -= catch_upper + catch_lower

    notch = (
        cuboid (
            [
                NOTCH_DEPTH * _math.sqrt (2),
                NOTCH_DEPTH * _math.sqrt (2),
                HOOK_WIDTH / 3 + HOOK_SLACK * 2
            ]
        )
        .rotate ([ 0, 0, 45 ])
        .left (bar_diameter / 2 + BAR_SINK)
        .fwd (bar_diameter / 2 + HOOK_THICKNESS - NOTCH_SINK)
    )

    body -= notch

    return body


def rail ():

    catch_upper = (
        cuboid (
            [
                HOOK_CHAMFER + ONE_PERIMETER,
                HOOK_CATCH,
                HOOK_CHAMFER + ONE_PERIMETER
            ],
            chamfer = HOOK_CHAMFER,
            edges = [ LEFT + BOTTOM, FRONT + BOTTOM ],
            anchor = RIGHT + BACK + BOTTOM,
        )
        .left (HOOK_THICKNESS)
        .up (HOOK_WIDTH / 2 - HOOK_CHAMFER + HOOK_SLACK)
    )

    catch_lower = catch_upper.mirror ([0, 0, 1])

    cover_upper = (
        cuboid (
            [
                BAR_SINK,
                HOOK_CATCH + BAR_SINK,
                BAR_SINK
            ],
            chamfer = BAR_SINK,
            edges = [ RIGHT + TOP, RIGHT + FRONT, TOP + FRONT ],
            anchor = RIGHT + BACK + BOTTOM,
        )
        .up (HOOK_WIDTH / 2 + HOOK_SLACK)
    )

    cover_lower = cover_upper.mirror ([0, 0, 1])

    body = catch_upper + catch_lower + cover_upper + cover_lower

    notch = (
        cuboid (
            [
                NOTCH_DEPTH * _math.sqrt (2),
                NOTCH_DEPTH * _math.sqrt (2),
                HOOK_WIDTH / 3
            ]
        )
        .rotate ([ 0, 0, 45 ])
        .left (BAR_SINK)
        .back (NOTCH_SINK)
    )

    body += notch

    return body.right (BAR_SINK).rotate ([90, 0, 90])


def bowl ():

    body = (
        cuboid (
            [
                BOWL_WIDTH,
                BOWL_LENGTH,
                BOWL_DEPTH
            ],
            edges = [ LEFT + FRONT, RIGHT + FRONT, LEFT + BOTTOM, FRONT + BOTTOM, RIGHT + BOTTOM ],
            chamfer = BOWL_CHAMFER,
            anchor = BACK + TOP,
        )
        -
        cuboid (
            [
                BOWL_WIDTH - BOWL_THICKNESS * 2,
                BOWL_LENGTH - BOWL_THICKNESS * 2,
                BOWL_DEPTH - BOWL_THICKNESS + OVERLAP
            ],
            edges = [ LEFT + FRONT, RIGHT + FRONT, LEFT + BOTTOM, FRONT + BOTTOM, RIGHT + BOTTOM ],
            chamfer = BOWL_CHAMFER - BOWL_THICKNESS / _math.sqrt (2),
            anchor = BACK + TOP,
        )
        .fwd (BOWL_THICKNESS)
        .up (OVERLAP)
    )

    notch = (
        cuboid (
            [
                NOTCH_WIDTH,
                NOTCH_DEPTH * _math.sqrt (2),
                NOTCH_DEPTH * _math.sqrt (2)
            ]
        )
        .rotate ([ 45, 0, 0])
        .down (LID_CATCH - NOTCH_SINK)
    )

    notch_front = notch.back (BOWL_LENGTH)
    notch_left = notch.left (BOWL_WIDTH / 2 - HOOK_WIDTH / 2 - BAR_SINK)
    notch_right = notch.right (BOWL_WIDTH / 2 - HOOK_WIDTH / 2 - BAR_SINK)

    body += notch_front + notch_left + notch_right

    rail_tmp = rail ().down (LID_CATCH)
    rail_left = rail_tmp.left (BOWL_WIDTH / 2 - HOOK_WIDTH / 2 - BAR_SINK)
    rail_right = rail_left.mirror ([1, 0, 0])

    body += rail_left + rail_right

    return body


def lid ():

    body = (
        cuboid (
            [
                BOWL_WIDTH + LID_SLACK * 2 + LID_THICKNESS * 2,
                BOWL_LENGTH + LID_SLACK * 2 + LID_THICKNESS * 2,
                LID_CATCH + LID_THICKNESS
            ],
            edges = [ LEFT + FRONT, RIGHT + FRONT ],
            chamfer = BOWL_CHAMFER + (LID_SLACK + LID_THICKNESS) / _math.sqrt (2),
            anchor = BOTTOM,
        )
        -
        cuboid (
            [
                BOWL_WIDTH + LID_SLACK * 2,
                BOWL_LENGTH + LID_SLACK * 2,
                LID_CATCH + OVERLAP
            ],
            edges = [ LEFT + FRONT, RIGHT + FRONT ],
            chamfer = BOWL_CHAMFER + LID_SLACK / _math.sqrt (2),
            anchor = BOTTOM,
        )
        .up (LID_THICKNESS)
        +
        cuboid (
            [
                BOWL_WIDTH - BOWL_THICKNESS * 2 - LID_SLACK * 2,
                BOWL_LENGTH - LID_THICKNESS * 2 - LID_SLACK * 2,
                LID_SHIELD_OUTER + LID_THICKNESS
            ],
            edges = [ LEFT + FRONT, RIGHT + FRONT ],
            chamfer = BOWL_CHAMFER - (BOWL_THICKNESS + LID_SLACK) / _math.sqrt (2),
            anchor = BOTTOM,
        )
        -
        cuboid (
            [
                BOWL_WIDTH - BOWL_THICKNESS * 2 - LID_SLACK * 2 - LID_THICKNESS * 2,
                BOWL_LENGTH - LID_THICKNESS * 2 - LID_SLACK * 2 - LID_THICKNESS * 2,
                LID_SHIELD_OUTER + OVERLAP
            ],
            edges = [ LEFT + FRONT, RIGHT + FRONT ],
            chamfer = BOWL_CHAMFER - (BOWL_THICKNESS + LID_SLACK + LID_THICKNESS) / _math.sqrt (2),
            anchor = BOTTOM,
        )
        .up (LID_THICKNESS)
    )

    guard = (
        fillet (
            l = BOWL_WIDTH - BOWL_THICKNESS * 2 - LID_SLACK * 2,
            r = LID_BRIM - LID_THICKNESS * 2,
        )
        .rotate ([ 90, 0, 0 - 90 ])
        .fwd (BOWL_LENGTH / 2 - BOWL_THICKNESS - LID_SLACK - LID_THICKNESS)
        +
        fillet (
            l = BOWL_WIDTH - BOWL_THICKNESS * 2 - LID_SLACK * 2 - BOWL_CHAMFER * 2 + LID_THICKNESS,
            r = LID_BRIM - LID_THICKNESS * 2,
        )
        .rotate ([ 0 - 90, 180, 0 - 90 ])
        .back (BOWL_LENGTH / 2 - BOWL_THICKNESS - LID_SLACK - LID_THICKNESS)
        +
        fillet (
            l = BOWL_LENGTH - BOWL_THICKNESS * 2 - LID_SLACK * 2 - BOWL_CHAMFER,
            r = LID_BRIM - LID_THICKNESS * 2,
        )
        .rotate ([ 90, 0, 0 ])
        .left (BOWL_WIDTH / 2 - BOWL_THICKNESS - LID_SLACK - LID_THICKNESS)
        .fwd (BOWL_CHAMFER / 2 - LID_THICKNESS / 2)
        +
        fillet (
            l = BOWL_LENGTH - BOWL_THICKNESS * 2 - LID_SLACK * 2 - BOWL_CHAMFER,
            r = LID_BRIM - LID_THICKNESS * 2,
        )
        .rotate ([ 90, 0, 180 ])
        .right (BOWL_WIDTH / 2 - BOWL_THICKNESS - LID_SLACK - LID_THICKNESS)
        .fwd (BOWL_CHAMFER / 2 - LID_THICKNESS / 2)
        +
        fillet (
            l = BOWL_CHAMFER * _math.sqrt (2) - BOWL_THICKNESS - LID_SLACK - LID_THICKNESS,
            r = LID_BRIM - LID_THICKNESS * 2,
        )
        .rotate ([ 90, 0, 45 ])
        .left (BOWL_WIDTH / 2 - BOWL_THICKNESS - LID_SLACK - LID_THICKNESS - (BOWL_CHAMFER - (BOWL_THICKNESS + LID_SLACK + LID_THICKNESS) / _math.sqrt (2)) / 2)
        .back (BOWL_LENGTH / 2 - BOWL_THICKNESS - LID_SLACK - LID_THICKNESS - (BOWL_CHAMFER - (BOWL_THICKNESS + LID_SLACK + LID_THICKNESS) / _math.sqrt (2)) / 2)
        +
        fillet (
            l = BOWL_CHAMFER * _math.sqrt (2) - BOWL_THICKNESS - LID_SLACK - LID_THICKNESS,
            r = LID_BRIM - LID_THICKNESS * 2,
        )
        .rotate ([ 90, 0, 135 ])
        .right (BOWL_WIDTH / 2 - BOWL_THICKNESS - LID_SLACK - LID_THICKNESS - (BOWL_CHAMFER - (BOWL_THICKNESS + LID_SLACK + LID_THICKNESS) / _math.sqrt (2)) / 2)
        .back (BOWL_LENGTH / 2 - BOWL_THICKNESS - LID_SLACK - LID_THICKNESS - (BOWL_CHAMFER - (BOWL_THICKNESS + LID_SLACK + LID_THICKNESS) / _math.sqrt (2)) / 2)
    )

    guard = guard.up (LID_THICKNESS)

    body += guard

    notch = (
        cuboid (
            [
                NOTCH_WIDTH + LID_SLACK * 2,
                NOTCH_DEPTH * _math.sqrt (2),
                NOTCH_DEPTH * _math.sqrt (2)
            ]
        )
        .rotate ([ 45, 0, 0 ])
        .up (LID_THICKNESS + LID_CATCH - NOTCH_SINK)
    )

    notch_front = notch.back (BOWL_LENGTH / 2 + LID_SLACK)
    notch_left = notch.fwd (BOWL_LENGTH / 2 + LID_SLACK).left (BOWL_WIDTH / 2 - HOOK_WIDTH / 2 - BAR_SINK)
    notch_right = notch.fwd (BOWL_LENGTH / 2 + LID_SLACK).right (BOWL_WIDTH / 2 - HOOK_WIDTH / 2 - BAR_SINK)

    body -= notch_front + notch_left + notch_right

    shield = (
        cuboid (
            [
                BOWL_WIDTH - LID_BRIM * 2 + LID_THICKNESS * 2,
                BOWL_LENGTH - LID_BRIM * 2 + LID_THICKNESS * 2,
                LID_THICKNESS + LID_SHIELD_INNER
            ],
            edges = [ LEFT + FRONT, RIGHT + FRONT ],
            rounding = LID_ROUNDING + LID_THICKNESS,
            anchor = BOTTOM,
        )
    )

    body += shield

    hole = (
        cuboid (
            [
                BOWL_WIDTH - LID_BRIM * 2,
                BOWL_LENGTH - LID_BRIM * 2,
                LID_THICKNESS + LID_SHIELD_INNER + OVERLAP * 2
            ],
            edges = [ LEFT + FRONT, RIGHT + FRONT ],
            rounding = LID_ROUNDING,
            anchor = BOTTOM,
        )
        .down (OVERLAP)
    )

    body -= hole

    return body


hook (BAR_DIAMETER_SMALL).save_as_scad ('hook-small.scad')
hook (BAR_DIAMETER_LARGE).save_as_scad ('hook-large.scad')
bowl ().save_as_scad ('bowl.scad')
lid ().save_as_scad ('lid.scad')
