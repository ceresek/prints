#!/usr/bin/env python3

import math

from solid import *
from solid.utils import *


# Not really sure what is happening in the export.
# Possibly 90 DPI and 25.4 mm to in.
RESCALE = 90/25.4

SEGMENTS = 33

X = 0
Y = 1
Z = 2
OVERLAP = 0.001


STRIPE_THICKNESS = 1

PIN_HEAD_THICKNESS = 2
PIN_HEAD_DISTANCE = 2
PIN_HEAD_WIDTH = 7
PIN_HEAD_HEIGHT = 3
PIN_STALK_WIDTH = 3
PIN_STALK_HEIGHT = 3

PIN_POSITION = [50, 105, 0]

HOOK_HEAD_DISTANCE = 11
HOOK_HEAD_RADIUS = 3.5 / 2

HOOK_LEFT_POSITION = [31, 27, 0]
HOOK_RIGHT_POSITION = [69, 27, 0]

stripe = scale (RESCALE) (linear_extrude (STRIPE_THICKNESS / RESCALE) (import_dxf ('stripe-wide.dxf')))
stripe = scale (RESCALE) (linear_extrude (STRIPE_THICKNESS / RESCALE) (import_dxf ('stripe-narrow.dxf')))
stripe = scale (RESCALE) (linear_extrude (STRIPE_THICKNESS / RESCALE) (import_dxf ('stripe-hooked.dxf')))

pin_stalk = up (STRIPE_THICKNESS + PIN_HEAD_DISTANCE/2 - OVERLAP) (translate (PIN_POSITION) (cube ([PIN_STALK_WIDTH, PIN_STALK_HEIGHT, PIN_HEAD_DISTANCE + 2*OVERLAP], center = True)))
pin_head = up (STRIPE_THICKNESS + PIN_HEAD_DISTANCE) (translate (PIN_POSITION) (cube ([PIN_HEAD_WIDTH, PIN_HEAD_HEIGHT, PIN_HEAD_THICKNESS], center = True)))

hook_stalk_left = translate (HOOK_LEFT_POSITION) (cylinder (r = HOOK_HEAD_RADIUS, h = HOOK_HEAD_DISTANCE + STRIPE_THICKNESS))
hook_stalk_right = translate (HOOK_RIGHT_POSITION) (cylinder (r = HOOK_HEAD_RADIUS, h = HOOK_HEAD_DISTANCE + STRIPE_THICKNESS))

result = stripe + pin_stalk + pin_head + hook_stalk_left + hook_stalk_right

scad_render_to_file (result, 'stripe.scad', file_header = f'$fn = {SEGMENTS};')
