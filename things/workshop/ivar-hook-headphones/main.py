#!/usr/bin/env python3

import math as _math
import numpy as _np

from solid2 import *
from solid2.extensions.bosl2 import *

import shared.things.ivar as _ivar

from shared.dimensions import *


set_global_fn (111)


HOOK_PHONES_RISE = 6.66
HOOK_PHONES_BEND = 10
HOOK_PHONES_WIDTH = 36
HOOK_PHONES_HEIGHT = 60

HOOK_PIN_TIP = 2.22
HOOK_PIN_DEPTH = 3.33

HOOK_CATCH_DEPTH = 11

HOOK_THICKNESS = SIX_PERIMETERS


def hook (rows, shift, radius):

    total_height = max (HOOK_PHONES_HEIGHT + HOOK_THICKNESS, _ivar.PIN_RADIUS_SMALL*2 + _ivar.PIN_DISTANCE_VERTICAL * (rows-1))

    # Stand clasp.

    face_wall = cuboid ((_ivar.STAND_WIDTH, HOOK_THICKNESS, total_height), anchor = RIGHT+BACK+BOTTOM, rounding = HOOK_THICKNESS, edges = LEFT+FRONT)
    side_wall = cuboid ((HOOK_THICKNESS, _ivar.STAND_DEPTH + 2*HOOK_THICKNESS, total_height), anchor = LEFT+FRONT+BOTTOM).back (HOOK_THICKNESS)
    back_wall = cuboid ((HOOK_CATCH_DEPTH, HOOK_THICKNESS, total_height), anchor = RIGHT+FRONT+BOTTOM, rounding = HOOK_THICKNESS, edges = LEFT+BACK).fwd (_ivar.STAND_DEPTH)

    pin = cyl (h = HOOK_PIN_DEPTH + HOOK_PIN_TIP, r = _ivar.PIN_RADIUS_SMALL, chamfer2 = HOOK_PIN_TIP, anchor = BOTTOM+BACK, orient = BACK)

    right_pin = pin.left (shift + _ivar.STAND_PIN_HOLE_TO_EDGE)
    left_pin = pin.left (shift + _ivar.STAND_PIN_HOLE_TO_EDGE + _ivar.PIN_DISTANCE_HORIZONTAL)

    pins = left_pin + right_pin

    pin_list = [ pins.up (_ivar.PIN_DISTANCE_VERTICAL * row) for row in range (rows) ]
    pin_rows = union () (*pin_list)

    # Hook bend.

    bend_length = _math.sqrt (HOOK_PHONES_WIDTH**2 + HOOK_PHONES_HEIGHT**2)
    bend_radius = bend_length**2 / HOOK_PHONES_BEND / 8 + HOOK_PHONES_BEND / 2

    bend_vector_normal = _np.array ([HOOK_PHONES_HEIGHT, -HOOK_PHONES_WIDTH]) / bend_length
    bend_vector_middle = _np.array ([HOOK_PHONES_WIDTH, HOOK_PHONES_HEIGHT]) / 2
    bend_circle_center = bend_vector_normal * (bend_radius - HOOK_PHONES_BEND) + bend_vector_middle

    arc_body = (
        cuboid ((HOOK_PHONES_WIDTH, _ivar.STAND_DEPTH + 2*HOOK_THICKNESS, HOOK_PHONES_HEIGHT + HOOK_THICKNESS), anchor = LEFT+FRONT+BOTTOM) -
        cyl (h = _ivar.STAND_DEPTH + 2*HOOK_THICKNESS + 2*FUDGE, r = bend_radius, rounding = -HOOK_THICKNESS, anchor = BOTTOM, orient = BACK).move ((bend_circle_center [0], 0-FUDGE, bend_circle_center [1]))
    )

    if radius:

        # Round hook top requires rounded surface.

        surface_height = radius - _math.sqrt (4*radius**2 - (_ivar.STAND_DEPTH + 2*HOOK_THICKNESS)**2)/2

        arc_body += (
            cyl (h = HOOK_PHONES_WIDTH + HOOK_THICKNESS, r = radius, anchor = BOTTOM, orient = RIGHT)
            .up (HOOK_PHONES_HEIGHT + HOOK_THICKNESS + surface_height - radius)
            .fwd (_ivar.STAND_DEPTH/2 + HOOK_THICKNESS)
            .left (HOOK_THICKNESS)
            *
            cuboid ((HOOK_PHONES_WIDTH + HOOK_THICKNESS, _ivar.STAND_DEPTH + 2*HOOK_THICKNESS, surface_height), anchor = LEFT+FRONT+BOTTOM)
            .up (HOOK_PHONES_HEIGHT + HOOK_THICKNESS)
            .left (HOOK_THICKNESS)
        )

        # Round hook top requires round edge.

        arc_edge = (
            cyl (h = 2*HOOK_THICKNESS, r = radius, rounding = HOOK_THICKNESS, orient = RIGHT)
            .up (HOOK_PHONES_RISE + surface_height - radius)
            .fwd (_ivar.STAND_DEPTH/2 + HOOK_THICKNESS)
            *
            cuboid ((2*HOOK_THICKNESS, _ivar.STAND_DEPTH + 2*HOOK_THICKNESS, HOOK_PHONES_RISE + surface_height), anchor = FRONT+BOTTOM, rounding = HOOK_THICKNESS, except_edges = [BOTTOM]).up (HOOK_THICKNESS)
            +
            cuboid ((HOOK_THICKNESS, _ivar.STAND_DEPTH + 2*HOOK_THICKNESS, HOOK_THICKNESS), anchor = LEFT+FRONT+BOTTOM, rounding = HOOK_THICKNESS, edges = [RIGHT+FRONT+BOTTOM, RIGHT+BACK+BOTTOM])
        )

    else:

        # Flat hook top requires rounded edges.

        arc_rounder_negative = cyl (h = HOOK_PHONES_WIDTH - HOOK_THICKNESS, r = HOOK_THICKNESS, rounding = -HOOK_THICKNESS, orient = RIGHT, anchor = BOTTOM)
        arc_rounder_front = cuboid ((HOOK_PHONES_WIDTH - HOOK_THICKNESS, HOOK_THICKNESS, HOOK_THICKNESS), anchor = LEFT+BACK+BOTTOM) - arc_rounder_negative
        arc_rounder_back = cuboid ((HOOK_PHONES_WIDTH - HOOK_THICKNESS, HOOK_THICKNESS, HOOK_THICKNESS), anchor = LEFT+FRONT+BOTTOM) - arc_rounder_negative

        arc_body -= (
            arc_rounder_front.up (HOOK_PHONES_HEIGHT).fwd (HOOK_THICKNESS) +
            arc_rounder_back.up (HOOK_PHONES_HEIGHT).fwd (_ivar.STAND_DEPTH + HOOK_THICKNESS)
        )

        # Flat hook top requires flat edge.

        arc_edge = (
            cuboid ((2*HOOK_THICKNESS, _ivar.STAND_DEPTH + 2*HOOK_THICKNESS, HOOK_PHONES_RISE), anchor = FRONT+BOTTOM, rounding = HOOK_THICKNESS, except_edges = [BOTTOM]).up (HOOK_THICKNESS) +
            cuboid ((HOOK_THICKNESS, _ivar.STAND_DEPTH + 2*HOOK_THICKNESS, HOOK_THICKNESS), anchor = LEFT+FRONT+BOTTOM, rounding = HOOK_THICKNESS, edges = [RIGHT+FRONT+BOTTOM, RIGHT+BACK+BOTTOM])
        )

    arc = (arc_body + arc_edge.right (HOOK_PHONES_WIDTH).up (HOOK_PHONES_HEIGHT)).right (HOOK_THICKNESS).back (HOOK_THICKNESS).up (total_height - HOOK_PHONES_HEIGHT - HOOK_THICKNESS)

    hook = face_wall + side_wall + back_wall + pin_rows + arc

    return hook


hook (2, 0, 0).save_as_scad ('hook-two-zero.scad')
hook (2, 1, 0).save_as_scad ('hook-two-one.scad')
hook (2, 2, 0).save_as_scad ('hook-two-two.scad')
hook (3, 0, 0).save_as_scad ('hook-three-zero.scad')
hook (3, 1, 0).save_as_scad ('hook-three-one.scad')
hook (3, 2, 0).save_as_scad ('hook-three-two.scad')

hook (3, 0, 44).save_as_scad ('hook-three-zero-fourtyfour.scad')
hook (3, 1, 44).save_as_scad ('hook-three-one-fourtyfour.scad')
hook (3, 2, 44).save_as_scad ('hook-three-two-fourtyfour.scad')
