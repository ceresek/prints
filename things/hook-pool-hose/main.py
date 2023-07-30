#!/usr/bin/env python3

from solid import *
from solid.utils import *

from components.common import *


SEGMENTS = 111

HOOK_WIDTH = 11
HOOK_ANGLE_ONE = 200
HOOK_ANGLE_TWO = 200
HOOK_RADIUS_ONE = 44/2
HOOK_RADIUS_TWO = 39/2
HOOK_LENGTH_BASE = 66
HOOK_LENGTH_SKIP = 66
HOOK_SEGMENTS = 2
HOOK_THICKNESS = 4.11


def hook_arc (radius, angle):

    outer = cylinder (r = radius + HOOK_THICKNESS, h = HOOK_WIDTH)
    inner = translate ((0, 0, -OVERLAP)) (cylinder (r = radius, h = HOOK_WIDTH + 2*OVERLAP))
    cut = translate ((0-radius-HOOK_THICKNESS-OVERLAP,0,0)) (cube ((2*radius+2*HOOK_THICKNESS+2*OVERLAP, radius+HOOK_THICKNESS+OVERLAP, HOOK_WIDTH)))
    rot = rotate ((0, 0, 180 - angle)) (cut)
    end = rotate ((0, 0, 180 - angle)) (translate ((radius + HOOK_THICKNESS/2, 0, 0)) (cylinder (HOOK_THICKNESS/2, HOOK_WIDTH)))

    return (outer - inner) * (cut + rot) + end


def hook ():

    arc_one = translate ((HOOK_RADIUS_ONE + HOOK_THICKNESS/2, HOOK_LENGTH_BASE/2, -HOOK_WIDTH/2)) (hook_arc (HOOK_RADIUS_ONE, HOOK_ANGLE_ONE))

    arc_two_original = translate ((0-HOOK_RADIUS_TWO - HOOK_THICKNESS/2, -HOOK_LENGTH_BASE/2, -HOOK_WIDTH/2)) (rotate ((0, 0, 180)) (hook_arc (HOOK_RADIUS_TWO, HOOK_ANGLE_TWO)))
    arc_two_segments = [ translate ((0, -index*HOOK_LENGTH_SKIP, 0)) (arc_two_original) for index in range (HOOK_SEGMENTS) ]
    arc_two_pack = union () (*arc_two_segments)

    body = translate ((-HOOK_THICKNESS/2,-HOOK_LENGTH_BASE/2-(HOOK_SEGMENTS-1)*HOOK_LENGTH_SKIP-OVERLAP, -HOOK_WIDTH/2)) (
        cube ((HOOK_THICKNESS, HOOK_LENGTH_BASE + (HOOK_SEGMENTS-1)*HOOK_LENGTH_SKIP + 2*OVERLAP, HOOK_WIDTH)))

    return arc_one + arc_two_pack + body


scad_render_to_file (hook (), 'hook.scad', file_header = f'$fn = {SEGMENTS};')
