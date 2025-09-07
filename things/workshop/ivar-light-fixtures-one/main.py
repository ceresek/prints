#!/usr/bin/env python3

import math

from solid import *
from solid.utils import *

from helpers import ivar


SEGMENTS = 111

X = 0
Y = 1
Z = 2
OVERLAP = 0.001


PIN_THICKNESS = 1
PIN_RADIUS = ivar.PIN_RADIUS_LARGE
PIN_HAT = 5

HOLDER_SHELF_WIDTH = 16
HOLDER_WIRE_SIZE = 6

BODY_THICKNESS = 1.5

THORN_RADIUS = 1/3
THORN_LENGTH = 1
THORN_SPACING = 3

PROFILE_SIZE = 16
PROFILE_CATCH = 2.5
PROFILE_THICKNESS = 1
PROFILE_NOTCH_SIZE = 5
PROFILE_NOTCH_DEPTH = 16
PROFILE_SHIELD_SIZE = 13
PROFILE_SHIELD_NOTCH = 2
PROFILE_SHIELD_DEPTH = 6
PROFILE_SHIELD_THICKNESS = 1

SHELF_SIZE = 18
SHELF_CATCH = 10
SHELF_THORN = 8

STAND_RAISE = 20
STAND_PIERCING = 9

PIERCING_SCALE = 1.2

WIRE_BOX_LENGTH = (235 - 150 - BODY_THICKNESS) / 2
WIRE_BOX_HEIGHT = 33
WIRE_HOLE_SIZE = 3
WIRE_POWER_HOLE_SIZE_X = 5.5
WIRE_POWER_HOLE_SIZE_Y = 4
WIRE_PIN_POS = 5
WIRE_PIN_SIZE = 3.7
WIRE_PIN_HEIGHT = 8
WIRE_HOLE_HEIGHT = 3
WIRE_HOLE_ONE_POS = 20
WIRE_HOLE_TWO_POS = 31
WIRE_CATCH_POS = 41.5
WIRE_CATCH_LENGTH = 10
WIRE_CATCH_HEIGHT = WIRE_PIN_HEIGHT

WIRE_HOLDER_HEIGHT = 19

LID_SLACK = 0.2
LID_NOTCH_DEPTH = 0.5
LID_NOTCH_SIZE = 2
LID_NOTCH_GAP = 2


def pin (radius, thickness, length, taper_up, taper_down):
    column = left (thickness/2) (cube ((thickness, radius, length)))
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


def cylinder_along_x (length, thickness):
    body = rotate ((0, 90, 0)) (cylinder (h = length, r = thickness/2))
    return body


def cylinder_along_y (length, thickness):
    body = rotate ((-90, 0, 0)) (cylinder (h = length, r = thickness/2))
    return body


def cylinder_along_z (length, thickness):
    body = cylinder (h = length, r = thickness/2)
    return body


def thorn (radius, length):
    body = cylinder (h = length, r1 = radius, r2 = 0)
    return body


def holder_shelf (width):

    body = union () (
        translate ((0, BODY_THICKNESS + SHELF_SIZE, 0)) (cube ((BODY_THICKNESS + PROFILE_SIZE + BODY_THICKNESS + SHELF_CATCH, BODY_THICKNESS, width))),
        translate ((BODY_THICKNESS + PROFILE_SIZE, 0, 0)) (cube ((BODY_THICKNESS, BODY_THICKNESS + SHELF_SIZE + BODY_THICKNESS, width))),
        translate ((BODY_THICKNESS + PROFILE_SIZE, 0, 0)) (cube ((BODY_THICKNESS + SHELF_CATCH, BODY_THICKNESS, width))),
        translate ((0, BODY_THICKNESS + SHELF_SIZE - PROFILE_CATCH, 0)) (cube ((BODY_THICKNESS, PROFILE_CATCH + BODY_THICKNESS, width))),
        translate ((BODY_THICKNESS + PROFILE_SIZE - PROFILE_CATCH, SHELF_SIZE - PROFILE_SIZE, 0)) (cube ((PROFILE_CATCH + BODY_THICKNESS, BODY_THICKNESS, width))))

    thorns = union () (
        translate ((BODY_THICKNESS + PROFILE_SIZE + BODY_THICKNESS + SHELF_THORN, BODY_THICKNESS + SHELF_SIZE + OVERLAP, 0)) (rotate ((90, 0, 0)) (thorn (THORN_RADIUS, THORN_LENGTH))),
        translate ((BODY_THICKNESS + PROFILE_SIZE + BODY_THICKNESS + SHELF_THORN, BODY_THICKNESS - OVERLAP, 0)) (rotate ((-90, 0, 0)) (thorn (THORN_RADIUS, THORN_LENGTH))))
    thorns_count = (width // THORN_SPACING)
    thorns_offset = (width % THORN_SPACING + THORN_SPACING) / 2
    thorns_positions = [ thorns_offset + index * THORN_SPACING for index in range (thorns_count) ]
    thorns_pattern = [ up (position) (thorns) for position in thorns_positions ]

    return body + union () (*thorns_pattern)


def holder_stand_hook (piercing_rotation = 90, extra_width = 0.0):

    stand_angle = (STAND_RAISE + (PROFILE_SIZE + extra_width)/2) / ivar.STAND_DEPTH

    body = union () (
        translate ((BODY_THICKNESS, STAND_RAISE + (PROFILE_SIZE + extra_width)/2, 0)) (
            multmatrix (((1, 0, 0, 0), (- stand_angle, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))) (
                cube ((ivar.STAND_DEPTH + OVERLAP*2, PROFILE_SIZE + extra_width, BODY_THICKNESS)))),
        translate ((0, STAND_RAISE + (PROFILE_SIZE + extra_width)/2, 0)) (
            cube ((BODY_THICKNESS, PROFILE_SIZE + extra_width, BODY_THICKNESS + ivar.STAND_WIDTH))),
        translate ((BODY_THICKNESS + ivar.STAND_DEPTH, 0, 0)) (
            cube ((BODY_THICKNESS, PROFILE_SIZE + extra_width, BODY_THICKNESS))))

    # Clip bottom side.
    clipping = translate ((- OVERLAP, STAND_RAISE + (PROFILE_SIZE + extra_width)/2, - OVERLAP)) (
        multmatrix (((1, 0, 0, 0), (- stand_angle, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))) (
            cube ((BODY_THICKNESS + OVERLAP*2, stand_angle * BODY_THICKNESS, BODY_THICKNESS + ivar.STAND_WIDTH + OVERLAP*2))))
    body -= clipping

    # Pierce hook side.
    piercing_base = translate ((-OVERLAP, STAND_RAISE + PROFILE_SIZE + extra_width, 0)) (
        rotate ((90, piercing_rotation, 90)) (
            scale ((PIERCING_SCALE, PIERCING_SCALE, 1)) (
                pin (PIN_RADIUS, PIN_THICKNESS, ivar.PIN_LENGTH, True, False))))
    piercing_one = translate ((0, 0, BODY_THICKNESS + STAND_PIERCING)) (piercing_base)
    piercing_two = translate ((0, 0, BODY_THICKNESS + ivar.STAND_WIDTH - STAND_PIERCING)) (piercing_base)
    body -= piercing_one + piercing_two

    return body


def holder_profile_lock ():

    lock_wall = translate ((- BODY_THICKNESS, 0, 0)) (
        cube ((BODY_THICKNESS, PROFILE_SIZE, PROFILE_NOTCH_DEPTH)))
    lock_arc = intersection () (
        cylinder (h = BODY_THICKNESS, r = PROFILE_SIZE),
        cube ((PROFILE_SIZE, PROFILE_SIZE, BODY_THICKNESS)))
    lock_pin = translate ((PROFILE_THICKNESS, PROFILE_THICKNESS, 0)) (intersection () (
        cube ((PROFILE_NOTCH_SIZE, PROFILE_NOTCH_SIZE, PROFILE_NOTCH_DEPTH)),
        rotate ((0, 0, 45))(cube ((PROFILE_NOTCH_SIZE * math.sqrt (2), PROFILE_NOTCH_SIZE * math.sqrt (2), PROFILE_NOTCH_DEPTH * 2), center = True))))
    lock_rim = intersection () (
        difference () (
            cylinder (h = PROFILE_SHIELD_DEPTH, r = PROFILE_SHIELD_SIZE + PROFILE_SHIELD_THICKNESS),
            cylinder (h = PROFILE_SHIELD_DEPTH + OVERLAP, r = PROFILE_SHIELD_SIZE)),
        translate ((PROFILE_SHIELD_NOTCH, PROFILE_SHIELD_NOTCH, 0)) (
            cube ((PROFILE_SIZE, PROFILE_SIZE, PROFILE_SHIELD_DEPTH))))

    lock = lock_wall + lock_arc + lock_pin + lock_rim

    return lock


def holder_middle ():

    hook = holder_stand_hook (piercing_rotation = 0)

    ending = union () (
        translate ((- BODY_THICKNESS, PROFILE_SIZE, 0)) (cube ((BODY_THICKNESS + PROFILE_SIZE + BODY_THICKNESS, BODY_THICKNESS, ivar.STAND_WIDTH + BODY_THICKNESS))),
        translate ((- BODY_THICKNESS, - BODY_THICKNESS, 0)) (cube ((BODY_THICKNESS, BODY_THICKNESS + PROFILE_SIZE + BODY_THICKNESS, ivar.STAND_WIDTH + BODY_THICKNESS))),
        translate ((PROFILE_SIZE, PROFILE_SIZE - PROFILE_CATCH, 0)) (cube ((BODY_THICKNESS, PROFILE_CATCH + BODY_THICKNESS, ivar.STAND_WIDTH + BODY_THICKNESS))),
        translate ((- BODY_THICKNESS, - BODY_THICKNESS, 0)) (cube ((PROFILE_CATCH + BODY_THICKNESS, BODY_THICKNESS, ivar.STAND_WIDTH + BODY_THICKNESS))))

    body = union () (
        translate ((0, 0, 0)) (hook),
        translate ((BODY_THICKNESS + ivar.STAND_DEPTH + BODY_THICKNESS, 0, 0)) (ending))

    return body


def holder_side ():

    hook = holder_stand_hook ()
    lock = holder_profile_lock ()

    body = union () (
        translate ((0, 0, 0)) (hook),
        translate ((BODY_THICKNESS + ivar.STAND_DEPTH + BODY_THICKNESS, PROFILE_SIZE, BODY_THICKNESS)) (
            rotate ((180, 0, 0)) (lock)))

    return body


def holder_wire ():

    hook = holder_stand_hook ()
    lock = holder_profile_lock ()

    cap_lead = translate ((BODY_THICKNESS, PROFILE_SIZE, 0)) (
        cube ((ivar.STAND_DEPTH + BODY_THICKNESS + PROFILE_SIZE, HOLDER_WIRE_SIZE + 2 * BODY_THICKNESS, 1)))
    cap_wall = translate ((BODY_THICKNESS + ivar.STAND_DEPTH, 0, 0)) (
        cube ((BODY_THICKNESS, PROFILE_SIZE + HOLDER_WIRE_SIZE + BODY_THICKNESS, 1)))
    cap_arc = translate ((BODY_THICKNESS + ivar.STAND_DEPTH + BODY_THICKNESS, PROFILE_SIZE, 0)) (
        rotate ((0, 0, -90)) (
            intersection () (
                cylinder (h = 1, r = PROFILE_SIZE),
                cube ((PROFILE_SIZE, PROFILE_SIZE, 1)))))
    cap = scale ((1, 1, HOLDER_WIRE_SIZE + 2 * BODY_THICKNESS)) (cap_lead + cap_wall + cap_arc)

    # Clip bottom side.
    clipping_angle = (STAND_RAISE + PROFILE_SIZE/2) / ivar.STAND_DEPTH
    clipping = translate ((BODY_THICKNESS - OVERLAP, 0, - OVERLAP)) (
        multmatrix (((1, 0, 0, 0), (- clipping_angle, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))) (
            cube ((BODY_THICKNESS + ivar.STAND_DEPTH + OVERLAP*2, STAND_RAISE + PROFILE_SIZE/2, BODY_THICKNESS + ivar.STAND_WIDTH + OVERLAP*2))))
    cap -= clipping

    body = union () (
        translate ((0, 0, 0)) (hook),
        translate ((0, 0, - HOLDER_WIRE_SIZE - BODY_THICKNESS)) (cap),
        translate ((BODY_THICKNESS + ivar.STAND_DEPTH + BODY_THICKNESS, PROFILE_SIZE, - HOLDER_WIRE_SIZE)) (
            rotate ((180, 0, 0)) (lock)))

    bore_helper_shared_x = BODY_THICKNESS + ivar.STAND_DEPTH + BODY_THICKNESS + PROFILE_SIZE*2/5
    bore_helper_turn_y = PROFILE_SIZE + BODY_THICKNESS + HOLDER_WIRE_SIZE / 2
    bore_helper_hole_y = PROFILE_SIZE*3/5
    bore_helper_shared_z = - HOLDER_WIRE_SIZE / 2

    bore_lock = translate ((bore_helper_shared_x, bore_helper_hole_y, - HOLDER_WIRE_SIZE - BODY_THICKNESS - OVERLAP)) (cylinder_along_z (BODY_THICKNESS + HOLDER_WIRE_SIZE / 2 + OVERLAP, HOLDER_WIRE_SIZE))
    bore_turn = translate ((bore_helper_shared_x, bore_helper_hole_y, bore_helper_shared_z)) (cylinder_along_y (PROFILE_SIZE * 2 / 5 + BODY_THICKNESS + HOLDER_WIRE_SIZE / 2, HOLDER_WIRE_SIZE))
    bore_side = translate ((0, bore_helper_turn_y, bore_helper_shared_z)) (cylinder_along_x (BODY_THICKNESS + ivar.STAND_DEPTH + BODY_THICKNESS + PROFILE_SIZE * 2 / 5, HOLDER_WIRE_SIZE))

    bore_ball_lock_turn = translate ((bore_helper_shared_x, bore_helper_hole_y, bore_helper_shared_z)) (sphere (HOLDER_WIRE_SIZE / 2))
    bore_lock_side_turn = translate ((bore_helper_shared_x, bore_helper_turn_y, bore_helper_shared_z)) (sphere (HOLDER_WIRE_SIZE / 2))

    body -= bore_lock + bore_ball_lock_turn + bore_turn + bore_lock_side_turn + bore_side

    return body


# The circular pin hat maybe looks better.
# The square pin hat can be printed horizontally.
# With layers aligned horizontally it is then stronger.

def holder_pin_circular ():
    stalk = up (BODY_THICKNESS) (pin (PIN_RADIUS, PIN_THICKNESS, ivar.PIN_LENGTH + BODY_THICKNESS, True, False))
    hat = cylinder (h = BODY_THICKNESS + OVERLAP, r = PIN_HAT)
    return stalk + hat


def holder_pin_square ():
    stalk = up (BODY_THICKNESS) (pin (PIN_RADIUS, PIN_THICKNESS, ivar.PIN_LENGTH + BODY_THICKNESS, True, False))
    hat = up ((BODY_THICKNESS + OVERLAP) / 2) (cube ((2 * PIN_HAT, 2 * PIN_RADIUS, BODY_THICKNESS + OVERLAP), center = True))
    return stalk + hat


def box_lid_notches (offset, gap):

    side = LID_NOTCH_SIZE + gap
    height = BODY_THICKNESS + LID_NOTCH_DEPTH + gap

    notch_l = translate ((0, - side/2, - side/2)) (cube ((height, side, side)))
    notch_r = mirror ((1, 0, 0)) (notch_l)
    notch_b = translate ((- side/2, 0, - side/2)) (cube ((side, height, side)))
    notch_t = mirror ((0, 1, 0)) (notch_b)

    notches = union () (
        # Left side.
        translate ((offset, WIRE_BOX_LENGTH * 1/4, 0)) (notch_l),
        translate ((offset, WIRE_BOX_LENGTH * 3/4, 0)) (notch_l),
        # Right side.
        translate ((ivar.STAND_WIDTH - offset, WIRE_BOX_LENGTH * 1/4, 0)) (notch_r),
        translate ((ivar.STAND_WIDTH - offset, WIRE_BOX_LENGTH * 3/4, 0)) (notch_r),
        # Bottom side.
        translate ((ivar.STAND_WIDTH * 1/4, offset, 0)) (notch_b),
        translate ((ivar.STAND_WIDTH * 3/4, offset, 0)) (notch_b),
        # Top side.
        translate ((ivar.STAND_WIDTH * 1/4, WIRE_BOX_LENGTH - offset, 0)) (notch_t),
        translate ((ivar.STAND_WIDTH * 3/4, WIRE_BOX_LENGTH - offset, 0)) (notch_t))

    return notches


def wire_box ():

    base = translate ((0, - WIRE_CATCH_LENGTH, 0)) (
        cube ((ivar.STAND_WIDTH, WIRE_BOX_LENGTH + WIRE_CATCH_LENGTH, BODY_THICKNESS)))

    catch_pin = translate ((WIRE_PIN_POS, - WIRE_PIN_POS, 0)) (
        cylinder (h = BODY_THICKNESS + WIRE_PIN_HEIGHT + OVERLAP, r = WIRE_PIN_SIZE/2))
    base += catch_pin

    catch_wall = translate ((WIRE_CATCH_POS, - WIRE_CATCH_LENGTH, 0)) (
        cube ((ivar.STAND_WIDTH - WIRE_CATCH_POS, WIRE_CATCH_LENGTH, BODY_THICKNESS + WIRE_CATCH_HEIGHT)))
    base += catch_wall

    body = difference () (
        translate ((0, 0, 0)) (cube ((ivar.STAND_WIDTH, WIRE_BOX_LENGTH, WIRE_BOX_HEIGHT - BODY_THICKNESS))),
        translate ((BODY_THICKNESS, BODY_THICKNESS, - OVERLAP)) (cube ((ivar.STAND_WIDTH - 2 * BODY_THICKNESS, WIRE_BOX_LENGTH - 2 * BODY_THICKNESS, WIRE_BOX_HEIGHT + 2 * OVERLAP))))
    base += body

    # Pierce hook side.
    piercing_base = translate ((0, WIRE_BOX_LENGTH - BODY_THICKNESS - OVERLAP, WIRE_HOLDER_HEIGHT)) (
        rotate ((-90, 60, 0)) (
            scale ((PIERCING_SCALE, PIERCING_SCALE, 1)) (
                pin (PIN_RADIUS, PIN_THICKNESS, ivar.PIN_LENGTH, True, False))))
    piercing_one = translate ((STAND_PIERCING, 0, 0)) (piercing_base)
    piercing_two = translate ((ivar.STAND_WIDTH - STAND_PIERCING, 0, 0)) (piercing_base)
    base -= piercing_one + piercing_two

    # Holes for power supply wires.
    hole_lo_one = translate ((WIRE_HOLE_ONE_POS, -OVERLAP, BODY_THICKNESS + WIRE_HOLE_HEIGHT)) (
        cylinder_along_y (BODY_THICKNESS + 2*OVERLAP, WIRE_HOLE_SIZE))
    hole_lo_two = translate ((WIRE_HOLE_TWO_POS, -OVERLAP, BODY_THICKNESS + WIRE_HOLE_HEIGHT)) (
        cylinder_along_y (BODY_THICKNESS + 2*OVERLAP, WIRE_HOLE_SIZE))
    base -= hole_lo_one + hole_lo_two

    # Notches for holding the lid.
    notches = translate ((0, 0, WIRE_BOX_HEIGHT - BODY_THICKNESS - LID_NOTCH_GAP - LID_NOTCH_SIZE / 2)) (
        box_lid_notches (0, 0))
    base += notches

    return base


def wire_box_lo_power ():

    box = wire_box ()

    hole_one = translate ((- OVERLAP, WIRE_BOX_LENGTH - 2*BODY_THICKNESS - WIRE_HOLE_SIZE*1/2, 2*BODY_THICKNESS + WIRE_HOLE_SIZE/2)) (
        cylinder_along_x (BODY_THICKNESS + 2*OVERLAP, WIRE_HOLE_SIZE))
    hole_two = translate ((- OVERLAP, WIRE_BOX_LENGTH - 3*BODY_THICKNESS - WIRE_HOLE_SIZE*3/2, 2*BODY_THICKNESS + WIRE_HOLE_SIZE/2)) (
        cylinder_along_x (BODY_THICKNESS + 2*OVERLAP, WIRE_HOLE_SIZE))
    box -= hole_one + hole_two

    return box


def wire_box_hi_power():

    box = wire_box()

    holes_apart = WIRE_POWER_HOLE_SIZE_Y - WIRE_POWER_HOLE_SIZE_X
    hole_one = translate ((ivar.STAND_WIDTH/2 - holes_apart/2, WIRE_BOX_LENGTH - 2*BODY_THICKNESS - WIRE_POWER_HOLE_SIZE_Y/2, - OVERLAP)) (
        cylinder_along_z (BODY_THICKNESS + 2 * OVERLAP, WIRE_POWER_HOLE_SIZE_Y))
    hole_two = translate ((ivar.STAND_WIDTH/2 + holes_apart/2, WIRE_BOX_LENGTH - 2*BODY_THICKNESS - WIRE_POWER_HOLE_SIZE_Y/2, - OVERLAP)) (
        cylinder_along_z (BODY_THICKNESS + 2 * OVERLAP, WIRE_POWER_HOLE_SIZE_Y))
    hole = hull () (hole_one, hole_two)
    box -= hole

    return box


def wire_lid ():

    base = cube ((ivar.STAND_WIDTH, WIRE_BOX_LENGTH, BODY_THICKNESS))

    rim = difference () (
        translate ((BODY_THICKNESS + LID_SLACK, BODY_THICKNESS + LID_SLACK, 0)) (
            cube ((ivar.STAND_WIDTH - 2*BODY_THICKNESS - 2*LID_SLACK, WIRE_BOX_LENGTH - 2*BODY_THICKNESS - 2*LID_SLACK, BODY_THICKNESS + 2*LID_NOTCH_GAP + LID_NOTCH_SIZE + LID_SLACK))),
        translate ((2*BODY_THICKNESS + LID_SLACK, 2*BODY_THICKNESS + LID_SLACK, - OVERLAP)) (
            cube ((ivar.STAND_WIDTH - 4*BODY_THICKNESS - 2*LID_SLACK, WIRE_BOX_LENGTH - 4*BODY_THICKNESS - 2*LID_SLACK, BODY_THICKNESS + 2*LID_NOTCH_GAP + LID_NOTCH_SIZE + LID_SLACK + 2*OVERLAP))))
    base += rim

    notches = translate ((0, 0, BODY_THICKNESS + LID_NOTCH_GAP + LID_NOTCH_SIZE/2 + LID_SLACK)) (
        box_lid_notches (LID_SLACK, LID_SLACK))
    base -= notches

    return base


holder_middle_direct = holder_middle ()
holder_middle_mirror = mirror ((1, 0, 0)) (holder_middle_direct)
        
holder_side_direct = holder_side ()
holder_side_mirror = mirror ((1, 0, 0)) (holder_side_direct)
        
holder_wire_direct = holder_wire ()
holder_wire_mirror = mirror ((1, 0, 0)) (holder_wire_direct)

scad_render_to_file (holder_shelf (HOLDER_SHELF_WIDTH), 'holder_shelf.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (holder_middle_direct, 'holder_middle_direct.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (holder_middle_mirror, 'holder_middle_mirror.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (holder_side_direct, 'holder_side_direct.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (holder_side_mirror, 'holder_side_mirror.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (holder_wire_direct, 'holder_wire_direct.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (holder_wire_mirror, 'holder_wire_mirror.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (holder_pin_circular (), 'holder_pin_circular.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (holder_pin_square (), 'holder_pin_square.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (wire_box_lo_power (), 'wire_box_lo_power.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (wire_box_hi_power (), 'wire_box_hi_power.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (wire_lid (), 'wire_lid.scad', file_header = f'$fn = {SEGMENTS};')
