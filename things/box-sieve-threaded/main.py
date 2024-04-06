#!/usr/bin/env python3

import numpy as _np
import math as _math

from solid2 import *
from solid2.extensions.bosl2 import *
from solid2.extensions.bosl2.threading import *


set_global_fn (111)


OVERLAP = 0.001

# Switch for faster rendering.
ROUNDED = True

# Height and diameter are external.
BOX_HEIGHT = 180
BOX_DIAMETER = 123
BOX_THICKNESS_FLOOR = 1.20 # 6 layers with 0.2 mm height
BOX_THICKNESS_WALLS = 2.49 # 6 lines with 0.4 mm nozzle

BOX_CHAMFER = 1
BOX_THREADS = 4

BOX_LID_SPLIT = 16

HOLE_DIAMETER = 5
HOLE_SPACING = HOLE_DIAMETER + 1.67 # 4 lines with 0.4 mm nozzle

SLIT_WIDTH = 3.30 # 8 lines with 0.4 mm nozzle
SLIT_SPACING = SLIT_WIDTH + 3.30 # 8 lines with 0.4 mm nozzle

THREAD_LEAD = 3
THREAD_BEVEL = 0.5
THREAD_HEIGHT = 7
THREAD_PITCH = 2
THREAD_SLACK = 0.444
THREAD_DEPTH = 1.444
THREAD_MIDDLE = BOX_DIAMETER - 2*BOX_THICKNESS_WALLS
THREAD_DIAMETERS = _np.array ([THREAD_MIDDLE - THREAD_DEPTH/2, THREAD_MIDDLE, THREAD_MIDDLE + THREAD_DEPTH/2])

PAW_SCALE = 0.5
PAW_DEPTH = 0.2


def box ():

    outside_height = BOX_HEIGHT - BOX_LID_SPLIT

    box = (
        threaded_rod (
            h = THREAD_HEIGHT + OVERLAP,
            d = THREAD_DIAMETERS - THREAD_SLACK/2,
            pitch = THREAD_PITCH,
            starts = BOX_THREADS,
            blunt_start2 = False,
            end_len1 = THREAD_LEAD,
            bevel1 = THREAD_BEVEL,
            anchor = BOTTOM,
        ) +
        cyl (
            h = outside_height, d = BOX_DIAMETER, circum = True,
            chamfer1 = BOX_THICKNESS_WALLS,
            anchor = BOTTOM,
        )
        .up (THREAD_HEIGHT) -
        cyl (
            h = THREAD_HEIGHT + OVERLAP, d = BOX_DIAMETER - BOX_THICKNESS_WALLS * 4,
            rounding1 = BOX_CHAMFER * ROUNDED,
            rounding2 = 0 - BOX_THICKNESS_WALLS/2 * ROUNDED,
            anchor = BOTTOM,
        )
        .up (BOX_THICKNESS_FLOOR) -
        cyl (
            h = outside_height + OVERLAP, d = BOX_DIAMETER - BOX_THICKNESS_WALLS * 2,
            rounding1 = BOX_THICKNESS_WALLS/2 * ROUNDED,
            anchor = BOTTOM,
        )
        .up (THREAD_HEIGHT + BOX_THICKNESS_FLOOR)
    )

    paw_line = import_ ('paw.svg').scale (0.77)
    paw_full = cylindrical_extrude (id = BOX_DIAMETER - PAW_DEPTH, od = BOX_DIAMETER + PAW_DEPTH) (paw_line).up (BOX_HEIGHT/2 + THREAD_HEIGHT)

    return box - paw_full


def holes_round ():

    hole = (
        cyl (
            h = BOX_THICKNESS_FLOOR + OVERLAP * 2, d = HOLE_DIAMETER,
            anchor = BOTTOM,
        )
        .down (OVERLAP)
    )

    hole_count = _math.floor ((BOX_DIAMETER / 2 - BOX_THICKNESS_WALLS * 2 - HOLE_DIAMETER) / HOLE_SPACING) + 1

    hole_line = union () (*[ hole.right (index * HOLE_SPACING).rotate ([0, 0, 60]) for index in range (hole_count) ])
    hole_frag = union () (*[ hole_line.left (index * HOLE_SPACING) for index in range (hole_count) ])
    hole_full = union () (*[ hole_frag.rotate ([0, 0, index * 60]) for index in range (6) ])

    return hole_full


def holes_slits ():

    slit_radius = BOX_DIAMETER / 2 - BOX_THICKNESS_WALLS * 2 - SLIT_SPACING
    slit_steps = _math.floor (slit_radius / SLIT_SPACING) + 1

    slit_list = []

    for index in range (slit_steps):
        slit_position = index * SLIT_SPACING
        slit_length = _math.sqrt (slit_radius ** 2 - slit_position ** 2) * 2
        slit = (
            cuboid (
                [ SLIT_WIDTH, slit_length, BOX_THICKNESS_FLOOR + OVERLAP * 2],
                rounding = SLIT_WIDTH/2, edges = [ FRONT+LEFT, FRONT+RIGHT, BACK+LEFT, BACK+RIGHT ],
                anchor = BOTTOM,
            )
            .down (OVERLAP)
        )
        slit_list.append (slit.left (slit_position))
        slit_list.append (slit.right (slit_position))

    return union () (*slit_list)


def lid ():

    lid = (
        cyl (
            h = BOX_LID_SPLIT + BOX_THICKNESS_WALLS, d = BOX_DIAMETER, circum = True,
            chamfer1 = BOX_CHAMFER,
            anchor = BOTTOM,
        ) -
        threaded_rod (
            h = THREAD_HEIGHT + OVERLAP,
            d = THREAD_DIAMETERS + THREAD_SLACK/2,
            pitch = THREAD_PITCH,
            starts = BOX_THREADS,
            internal = True,
            blunt_start1 = False,
            end_len2 = THREAD_LEAD,
            anchor = BOTTOM,
            orient = BOTTOM,
        )
        .up (BOX_LID_SPLIT + OVERLAP) -
        cyl (
            h = BOX_LID_SPLIT + BOX_THICKNESS_WALLS - BOX_THICKNESS_FLOOR + OVERLAP, d = BOX_DIAMETER - BOX_THICKNESS_WALLS * 2,
            chamfer2 = 0 - BOX_THICKNESS_WALLS,
            rounding1 = BOX_CHAMFER * ROUNDED,
            anchor = BOTTOM,
        )
        .up (BOX_THICKNESS_FLOOR)
    )

    return lid


box_round = box () - holes_round ()
box_slits = box () - holes_slits ()

box_round.save_as_scad ('box-round.scad')
box_slits.save_as_scad ('box-slits.scad')
lid ().save_as_scad ('lid.scad')
