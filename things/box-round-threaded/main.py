#!/usr/bin/env python3

import numpy as _np

from solid2 import *
from solid2.extensions.bosl2 import *
from solid2.extensions.bosl2.threading import *


set_global_fn (111)


OVERLAP = 0.001

# Height and diameter are external.
BOX_HEIGHT = 22
BOX_DIAMETER = 77
BOX_THICKNESS_FLOOR = 1.20 # 6 layers with 0.2 mm height
BOX_THICKNESS_WALLS = 3.30 # 8 lines with 0.4 mm nozzle
BOX_THICKNESS_MINOR = 0.86 # 2 lines with 0.4 mm nozzle

BOX_CHAMFER = 1
BOX_THREADS = 4
BOX_SEGMENTS = 16

BOX_LID_SPLIT = 1/2

THREAD_LEAD = 2
THREAD_BEVEL = 0.5
THREAD_HEIGHT = 6
THREAD_PITCH = 2
THREAD_SLACK = 0.388
THREAD_DEPTH = BOX_THICKNESS_WALLS - 2*BOX_THICKNESS_MINOR - THREAD_SLACK/2
THREAD_MIDDLE = BOX_DIAMETER - BOX_THICKNESS_WALLS
THREAD_DIAMETERS = _np.array ([THREAD_MIDDLE - THREAD_DEPTH/2, THREAD_MIDDLE, THREAD_MIDDLE + THREAD_DEPTH/2])

PAW_SCALE = 0.5
PAW_DEPTH = 0.2 # 1 layer with 0.2 mm height
PAW_OUTLINE = 0.86 # 2 lines with 0.4 mm nozzle


def box ():

    outside_height = BOX_HEIGHT * BOX_LID_SPLIT
    inside_height = outside_height - BOX_THICKNESS_FLOOR

    box = (
        cyl (
            h = outside_height, d = BOX_DIAMETER, circum = True,
            chamfer1 = BOX_CHAMFER, _fn = BOX_SEGMENTS,
            anchor = BOTTOM,
        ) +
        threaded_rod (
            h = THREAD_HEIGHT,
            d = THREAD_DIAMETERS - THREAD_SLACK/2,
            pitch = THREAD_PITCH,
            starts = BOX_THREADS,
            blunt_start1 = False,
            end_len2 = THREAD_LEAD,
            bevel2 = THREAD_BEVEL,
            anchor = BOTTOM,
        )
        .up (outside_height) -
        cyl (
            h = inside_height + THREAD_HEIGHT + OVERLAP, d = BOX_DIAMETER - BOX_THICKNESS_WALLS * 2,
            rounding1 = BOX_CHAMFER,
            anchor = BOTTOM,
        )
        .up (BOX_THICKNESS_FLOOR)
    )

    return box


def lid ():

    outside_height = BOX_HEIGHT * (1 - BOX_LID_SPLIT)
    inside_height = outside_height - BOX_THICKNESS_FLOOR

    lid = (
        cyl (
            h = outside_height, d = BOX_DIAMETER, circum = True,
            chamfer1 = BOX_CHAMFER, _fn = BOX_SEGMENTS,
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
        .up (outside_height + OVERLAP) -
        cyl (
            h = inside_height + OVERLAP, d = BOX_DIAMETER - BOX_THICKNESS_WALLS * 2,
            rounding1 = BOX_CHAMFER,
            anchor = BOTTOM,
        )
        .up (BOX_THICKNESS_FLOOR)
    )

    paw_full = import_ ('paw.svg').scale (0.5)
    paw_line_outer = paw_full.offset (PAW_OUTLINE/2).linear_extrude (PAW_DEPTH + OVERLAP).down (OVERLAP)
    paw_line_inner = paw_full.offset (-PAW_OUTLINE/2).linear_extrude (PAW_DEPTH + 2*OVERLAP).down (2*OVERLAP)
    paw_line = paw_line_outer - paw_line_inner

    return lid - paw_line


box ().save_as_scad ('box.scad')
lid ().save_as_scad ('lid.scad')
