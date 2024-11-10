#!/usr/bin/env python3

from solid2 import *
from solid2.extensions.bosl2 import *

from components.common import *


set_global_fn (111)


OVERLAP = 0.01


HANDLE_WIDTH = 8
HANDLE_HEIGHT = 11
HANDLE_LENGTH = 55
HANDLE_CHAMFER = 1

TUBE_SLACK = 0.1
TUBE_LENGTH = 66
TUBE_CHAMFER = TRE_PERIMETERS
TUBE_THICKNESS = FOR_PERIMETERS


def key (grasp):

    handle = cuboid ([ HANDLE_LENGTH, HANDLE_WIDTH, HANDLE_HEIGHT ], chamfer = HANDLE_CHAMFER, anchor = BOTTOM)
    tube = cyl (h = TUBE_LENGTH, d = grasp + TUBE_SLACK * 2 + TUBE_THICKNESS * 2, circum = True, _fn = 6, anchor = BOTTOM)
    hole = cyl (h = TUBE_LENGTH + OVERLAP * 2, d = grasp + TUBE_SLACK * 2, circum = True, _fn = 6, chamfer = 0 - TUBE_CHAMFER, anchor = BOTTOM).down (OVERLAP)

    return handle + tube - hole


key (11).save_as_scad ('key-11.scad')
key (12).save_as_scad ('key-12.scad')
