#!/usr/bin/env python3

import math

from solid import *
from solid.utils import *

from components.common import *


SEGMENTS = 111

HINGE_THICKNESS = 2.2
HINGE_LENGTH = 58
CATCH_RADIUS = 6.6
CATCH_HEIGHT = 2.2

JOIN_RADIUS = CATCH_RADIUS / 4
JOIN_OVERLAP = JOIN_RADIUS * 4
JOIN_TOLERANCE = 0.1


def hinge ():

    base_length = HINGE_LENGTH/2 + CATCH_RADIUS

    base = translate ((0, 0 - CATCH_RADIUS, 0)) (
        cube ((base_length, CATCH_RADIUS*2, HINGE_THICKNESS)))

    hinge = translate ((0, 0, 0)) (
        cylinder (r = CATCH_RADIUS, h = HINGE_THICKNESS + CATCH_HEIGHT))

    join_base = translate ((0, 0 - CATCH_RADIUS, 0)) (
        cube ((JOIN_OVERLAP, CATCH_RADIUS*2, HINGE_THICKNESS / 2)))
    join_hole = translate ((JOIN_OVERLAP/2, CATCH_RADIUS / 2, 0 - OVERLAP)) (
        cylinder (r = JOIN_RADIUS + JOIN_TOLERANCE, h = HINGE_THICKNESS))
    join_pin = translate ((JOIN_OVERLAP/2, 0 - CATCH_RADIUS / 2, 0)) (
        cylinder (r = JOIN_RADIUS, h = HINGE_THICKNESS))

    join = translate ((base_length, 0, 0)) (join_base - join_hole + join_pin)

    return base + hinge + join


scad_render_to_file (hinge (), 'hinge.scad', file_header = f'$fn = {SEGMENTS};')
