#!/usr/bin/env python3

import math as _math

from solid import *
from solid.utils import *

from components.common import *


SEGMENTS = 33


# Constants

ROOF_ANGLE = 45
ROOF_THICKNESS = 3

APRON_GLUE = 1/2
APRON_SLANT = 1
APRON_HEIGHT = 20


def roof (column_width):

    side = cube ((column_width + 2*ROOF_THICKNESS, ROOF_THICKNESS, column_width))
    side = rotate ((- ROOF_ANGLE, 0, 0)) (side)

    apron = cube ((column_width + 2*ROOF_THICKNESS, ROOF_THICKNESS, APRON_HEIGHT + OVERLAP))
    apron = multmatrix (((1, 0, 0, 0), (0, 1, 0, 0), (0, APRON_SLANT, 1, 0), (0, 0, 0, 1))) (apron)

    glue = cube ((column_width + 2*ROOF_THICKNESS, ROOF_THICKNESS * APRON_GLUE, APRON_HEIGHT + OVERLAP))

    apron += glue
    apron = translate ((0, 0, - APRON_HEIGHT)) (apron)

    side += apron
    side = translate ((- column_width/2 - ROOF_THICKNESS, - ROOF_THICKNESS, 0)) (side)

    SIDE_CUT_OVERLAP = 80
    SIDE_CUT_HEIGHT = column_width + SIDE_CUT_OVERLAP
    SIDE_CUT_WIDTH = (column_width/2 + SIDE_CUT_OVERLAP) * sqrt (2)
    SIDE_CUT_SHIFT = SIDE_CUT_WIDTH / sqrt (2) - column_width/2

    cut = rotate ((0, 0, 315)) (cube ((SIDE_CUT_WIDTH, SIDE_CUT_WIDTH, SIDE_CUT_HEIGHT)))
    cut = translate ((- SIDE_CUT_WIDTH / sqrt(2), - SIDE_CUT_SHIFT, - SIDE_CUT_OVERLAP)) (cut)

    fourth = side * cut
    fourth = translate ((0, - column_width/2, 0)) (fourth)

    whole_list = [ rotate ((0, 0, 90 * segment)) (fourth) for segment in range (4) ]
    whole_object = union () (*whole_list)

    return whole_object


# Main

scad_render_to_file (roof (77), 'roof-77.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (roof (78), 'roof-78.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (roof (79), 'roof-79.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (roof (80), 'roof-80.scad', file_header = f'$fn = {SEGMENTS};')
