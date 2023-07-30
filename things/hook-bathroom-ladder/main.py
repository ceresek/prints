#!/usr/bin/env python3

from solid import *
from solid.utils import *

from components.common import *


SEGMENTS = 111

HOOK_WIDTH = 8
HOOK_ANGLE_ONE = 200
HOOK_ANGLE_TWO = 180
HOOK_RADIUS_ONE = 10
HOOK_RADIUS_TWO = 20
HOOK_LENGTH = 40
HOOK_THICKNESS = 4.4


def hook_arc (radius, angle):

    outer = cylinder (r = radius + HOOK_THICKNESS, h = HOOK_WIDTH)
    inner = translate ((0, 0, -OVERLAP)) (cylinder (r = radius, h = HOOK_WIDTH + 2*OVERLAP))
    cut = translate ((0-radius-HOOK_THICKNESS-OVERLAP,0,0)) (cube ((2*radius+2*HOOK_THICKNESS+2*OVERLAP, radius+HOOK_THICKNESS+OVERLAP, HOOK_WIDTH)))
    rot = rotate ((0, 0, 180 - angle)) (cut)
    end = rotate ((0, 0, 180 - angle)) (translate ((radius + HOOK_THICKNESS/2, 0, 0)) (cylinder (HOOK_THICKNESS/2, HOOK_WIDTH)))

    return (outer - inner) * (cut + rot) + end


def hook ():

    arc_one = translate ((HOOK_RADIUS_ONE + HOOK_THICKNESS/2, HOOK_LENGTH/2, -HOOK_WIDTH/2)) (hook_arc (HOOK_RADIUS_ONE, HOOK_ANGLE_ONE))
    arc_two = translate ((0-HOOK_RADIUS_TWO - HOOK_THICKNESS/2, -HOOK_LENGTH/2, -HOOK_WIDTH/2)) (rotate ((0, 0, 180)) (hook_arc (HOOK_RADIUS_TWO, HOOK_ANGLE_TWO)))
    body = cube ((HOOK_THICKNESS, HOOK_LENGTH + 2*OVERLAP, HOOK_WIDTH), center = True)

    return arc_one + arc_two + body


scad_render_to_file (hook (), 'hook.scad', file_header = f'$fn = {SEGMENTS};')
