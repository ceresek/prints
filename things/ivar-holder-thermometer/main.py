#!/usr/bin/env python3

import math

from solid import *
from solid.utils import *

from helpers import ivar


SEGMENTS = 33

X = 0
Y = 1
Z = 2
OVERLAP = 0.001


PIN_RADIUS = ivar.PIN_RADIUS_SMALL
PIN_THICKNESS = 0.86

BODY_THICKNESS = 0.86

HOOK_RADIUS = 5/2
HOOK_LENGTH = 3
HOOK_SHEAR = 0.666


def pin (radius, thickness, length, taper_up, taper_down):
    column = left (thickness/2) (cube ([thickness, radius, length]))
    one = rotate ((0, 0, +120)) (column)
    two = rotate ((0, 0, -120)) (column)
    middle = cylinder (h = length, r = thickness/2)
    body = union () (column, one, two, middle)
    if taper_up:
        taper = cylinder (h = length, r1 = length + radius/2, r2 = radius/2)
        body *= taper
    if taper_down:
        taper = cylinder (h = length, r1 = radius/2, r2 = length + radius/2)
        body *= taper
    return body


pin_any = up (BODY_THICKNESS) (pin (PIN_RADIUS, PIN_THICKNESS, ivar.PIN_LENGTH, True, False))
pin_left = left (ivar.PIN_DISTANCE_HORIZONTAL/2) (pin_any)
pin_right = right (ivar.PIN_DISTANCE_HORIZONTAL/2) (pin_any)

body = up (BODY_THICKNESS/2) (cube ([ivar.PIN_DISTANCE_HORIZONTAL + 2*PIN_RADIUS, 2*PIN_RADIUS, BODY_THICKNESS], center = True))

hook = multmatrix (((1, 0, 0, 0), (0, 1, HOOK_SHEAR, 0), (0, 0, 1, 0), (0, 0, 0, 1))) (down (HOOK_LENGTH) (cylinder (h = HOOK_LENGTH, r = HOOK_RADIUS)))

total = pin_left + pin_right + body + hook

scad_render_to_file (total, 'total.scad', file_header = f'$fn = {SEGMENTS};')
