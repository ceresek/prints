#!/usr/bin/env python3

import math
import operator

from solid import *
from solid.utils import *

from helpers import ivar


SEGMENTS = 111

X = 0
Y = 1
Z = 2
OVERLAP = 0.001


PIN_SHRINK_FACTOR = 4/5
PIN_THICKNESS = 1
PIN_RADIUS = ivar.PIN_RADIUS_SMALL
PIN_HAT = 5

# Setting fits four perimeters with 150 microns layers.
BODY_THICKNESS = 1.7

HOLDER_WIRE_SIZE = 6
HOLDER_SHELF_HEIGHT = ivar.SHELF_HEIGHT + 0.6

HOLDER_PIPE_SIZE = BODY_THICKNESS + HOLDER_WIRE_SIZE + BODY_THICKNESS

PROFILE_SIZE = 16
PROFILE_CATCH = 2.5
PROFILE_THICKNESS = 1
PROFILE_HOLE_OFFSET = 6.6
PROFILE_NOTCH_BUMP = 0.6
PROFILE_NOTCH_SIZE = 6
PROFILE_NOTCH_DEPTH = 16
PROFILE_SHIELD_SIZE = 13
PROFILE_SHIELD_NOTCH = 2
PROFILE_SHIELD_DEPTH = 6
PROFILE_SHIELD_THICKNESS = 1

PROFILE_OFFSET = (HOLDER_SHELF_HEIGHT - PROFILE_SIZE) / 2

MODULE_LENGTH = 150
MODULE_HEIGHT = 30.5
MODULE_WIDTH_TOP = 38
MODULE_WIDTH_BOTTOM = 40

PIERCING_SCALE = 1.2

WIRE_BOX_LENGTH = ivar.STAND_WIDTH
WIRE_BOX_HEIGHT = MODULE_HEIGHT + BODY_THICKNESS*2
WIRE_HOLE_SIZE = 3
WIRE_LIGHT_HOLE_OVERLAP = 1
WIRE_LIGHT_HOLE_SIZE = 3
WIRE_POWER_HOLE_SIZE = 7
WIRE_PIN_POS = 5
WIRE_PIN_SIZE = 3.7
WIRE_PIN_HEIGHT = 8
WIRE_HOLE_HEIGHT = 3
WIRE_HOLE_ONE_POS = 20
WIRE_HOLE_TWO_POS = 31
WIRE_CATCH_POS = 41.5
WIRE_CATCH_LENGTH = 10
WIRE_CATCH_HEIGHT = WIRE_PIN_HEIGHT

WIRE_SQUEEZE_SIZE = 8
WIRE_SQUEEZE_SCALE = 0.9

WIRE_HOLDER_HEIGHT = 19

LID_SLACK = 0.2
LID_NOTCH_DEPTH = 0.6
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


def holder_profile_lock ():

    lock_arc = intersection () (
        cylinder (h = BODY_THICKNESS, r = PROFILE_SIZE),
        cube ((PROFILE_SIZE, PROFILE_SIZE, BODY_THICKNESS)))
    lock_pin = translate ((PROFILE_THICKNESS, PROFILE_THICKNESS, 0)) (intersection () (
        cube ((PROFILE_NOTCH_SIZE, PROFILE_NOTCH_SIZE, PROFILE_NOTCH_DEPTH)),
        rotate ((0, 0, 45))(cube ((PROFILE_NOTCH_SIZE * math.sqrt (2), PROFILE_NOTCH_SIZE * math.sqrt (2), PROFILE_NOTCH_DEPTH * 2), center = True))))
    lock_bum = translate ((PROFILE_THICKNESS + PROFILE_NOTCH_SIZE/2, PROFILE_THICKNESS + PROFILE_NOTCH_SIZE/2, PROFILE_NOTCH_DEPTH/2)) (
        cylinder_along_z (PROFILE_NOTCH_DEPTH/3, PROFILE_NOTCH_BUMP*2))
    lock_rim = intersection () (
        difference () (
            cylinder (h = PROFILE_SHIELD_DEPTH, r = PROFILE_SHIELD_SIZE + PROFILE_SHIELD_THICKNESS),
            cylinder (h = PROFILE_SHIELD_DEPTH + OVERLAP, r = PROFILE_SHIELD_SIZE)),
        translate ((PROFILE_SHIELD_NOTCH, PROFILE_SHIELD_NOTCH, 0)) (
            cube ((PROFILE_SIZE, PROFILE_SIZE, PROFILE_SHIELD_DEPTH))))

    lock = lock_arc + lock_pin + lock_bum + lock_rim

    return lock


def holder_wire ():

    lock = holder_profile_lock ()

    # Construct shelf hook.
    hook_width = ivar.STAND_PIN_HOLE_TO_EDGE + PIN_RADIUS
    hook_height = HOLDER_PIPE_SIZE + HOLDER_SHELF_HEIGHT + HOLDER_PIPE_SIZE

    hook = union () (
        translate ((0, 0, 0 - BODY_THICKNESS)) (
            cube ((ivar.STAND_DEPTH, hook_height, BODY_THICKNESS))),
        translate ((0 - BODY_THICKNESS, 0, 0)) (
            cube ((BODY_THICKNESS, hook_height, hook_width))),
        translate ((0 - BODY_THICKNESS, HOLDER_PIPE_SIZE + HOLDER_SHELF_HEIGHT, 0 - HOLDER_PIPE_SIZE)) (
            cube ((BODY_THICKNESS + ivar.STAND_DEPTH + PROFILE_SIZE, BODY_THICKNESS, HOLDER_PIPE_SIZE))),
        translate ((0 - BODY_THICKNESS, 0, 0 - BODY_THICKNESS)) (
            cube ((BODY_THICKNESS + OVERLAP, hook_height, BODY_THICKNESS + OVERLAP))))

    # Pierce hook side.
    hook_hole_size = PIN_RADIUS*2*PIERCING_SCALE
    hook_hole_offset = HOLDER_PIPE_SIZE + HOLDER_SHELF_HEIGHT - ivar.SHELF_PIERCING_TO_SURFACE
    hook_hole = translate ((0 - BODY_THICKNESS - OVERLAP, hook_hole_offset, ivar.STAND_PIN_HOLE_TO_EDGE)) (
        cylinder_along_x (BODY_THICKNESS + OVERLAP*2, hook_hole_size))
    hook_slot_x = translate ((0 - BODY_THICKNESS - OVERLAP, 0 - OVERLAP, ivar.STAND_PIN_HOLE_TO_EDGE)) (
        cube ((BODY_THICKNESS + OVERLAP*2, hook_hole_offset + hook_hole_size/2 + OVERLAP, ivar.STAND_WIDTH)))
    hook_slot_y = translate ((0 - BODY_THICKNESS - OVERLAP, 0 - OVERLAP, ivar.STAND_PIN_HOLE_TO_EDGE - hook_hole_size/2)) (
        cube ((BODY_THICKNESS + OVERLAP*2, hook_hole_offset + OVERLAP, ivar.STAND_WIDTH)))
    hook -= hook_hole + hook_slot_x + hook_slot_y

    # Construct wire cap.
    cap_lead = translate ((0 - BODY_THICKNESS, 0, 0)) (
        cube ((BODY_THICKNESS + ivar.STAND_DEPTH, HOLDER_PIPE_SIZE, HOLDER_PIPE_SIZE)))
    cap_wall = translate ((ivar.STAND_DEPTH, PROFILE_SIZE, 0)) (
        cube ((PROFILE_SIZE, HOLDER_SHELF_HEIGHT + HOLDER_PIPE_SIZE - PROFILE_SIZE + OVERLAP, HOLDER_PIPE_SIZE)))
    cap_arc = translate ((ivar.STAND_DEPTH, PROFILE_SIZE, 0)) (
        rotate ((0, 0, -90)) (
            intersection () (
                cylinder (h = HOLDER_PIPE_SIZE, r = PROFILE_SIZE),
                cube ((PROFILE_SIZE, PROFILE_SIZE, HOLDER_PIPE_SIZE)))))
    cap = cap_lead + cap_wall + cap_arc

    body = union () (
        mirror ((0, 0, 1)) (cap),
        translate ((0, 0, 0)) (hook),
        translate ((ivar.STAND_DEPTH, PROFILE_SIZE + PROFILE_OFFSET + HOLDER_PIPE_SIZE, 0 - BODY_THICKNESS - HOLDER_WIRE_SIZE)) (
            rotate ((180, 0, 0)) (lock)))

    # Construct wire hole.
    bore_helper_shared_x = ivar.STAND_DEPTH + PROFILE_HOLE_OFFSET
    bore_helper_side_y = BODY_THICKNESS + HOLDER_WIRE_SIZE/2
    bore_helper_turn_y = BODY_THICKNESS + HOLDER_WIRE_SIZE / 2 + PROFILE_HOLE_OFFSET
    bore_helper_hole_y = HOLDER_PIPE_SIZE + PROFILE_OFFSET + PROFILE_SIZE - PROFILE_HOLE_OFFSET
    bore_helper_shared_z = 0 - BODY_THICKNESS - HOLDER_WIRE_SIZE/2

    bore_side = translate ((0 - BODY_THICKNESS - OVERLAP, bore_helper_side_y, bore_helper_shared_z)) (cylinder_along_x (BODY_THICKNESS + ivar.STAND_DEPTH + OVERLAP*2, HOLDER_WIRE_SIZE))
    bore_bent = translate ((ivar.STAND_DEPTH, bore_helper_turn_y, bore_helper_shared_z)) (rotate ((0, 0, -90)) (rotate_extrude (90) (translate ((PROFILE_HOLE_OFFSET, 0, 0)) (circle (HOLDER_WIRE_SIZE / 2)))))
    bore_turn = translate ((bore_helper_shared_x, bore_helper_turn_y - OVERLAP, bore_helper_shared_z)) (cylinder_along_y (bore_helper_hole_y - bore_helper_turn_y + OVERLAP, HOLDER_WIRE_SIZE))
    bore_lock = translate ((bore_helper_shared_x, bore_helper_hole_y, 0 - HOLDER_WIRE_SIZE - BODY_THICKNESS*2 - OVERLAP)) (cylinder_along_z (BODY_THICKNESS + HOLDER_WIRE_SIZE/2 + OVERLAP, HOLDER_WIRE_SIZE))

    bore_ball_lock_turn = translate ((bore_helper_shared_x, bore_helper_hole_y, bore_helper_shared_z)) (sphere (HOLDER_WIRE_SIZE/2))

    body -= bore_lock + bore_ball_lock_turn + bore_turn + bore_bent + bore_side

    return body


def holder_bent ():

    lock = holder_profile_lock ()

    # Construct wire cap.
    cap_lead_length = BODY_THICKNESS + ivar.STAND_DEPTH
    cap_lead_height = PROFILE_HOLE_OFFSET + HOLDER_WIRE_SIZE / 2 + BODY_THICKNESS

    cap_lead_body = cube ((cap_lead_length, cap_lead_height, HOLDER_PIPE_SIZE))

    cap_arc_body = cylinder (h = HOLDER_PIPE_SIZE, r = PROFILE_SIZE)
    cap_arc_body *= cube ((PROFILE_SIZE, PROFILE_SIZE, HOLDER_PIPE_SIZE))
    cap_arc_body += translate ((0, 0, HOLDER_PIPE_SIZE - BODY_THICKNESS)) (lock)

    cap_lead_body = translate ((0 - BODY_THICKNESS, 0, 0)) (cap_lead_body)
    cap_arc_body = rotate ((0, -45, 180)) (cap_arc_body)
    cap_arc_body = translate ((ivar.STAND_DEPTH, cap_lead_height, 0)) (cap_arc_body)
    cap = cap_lead_body + cap_arc_body

    # Pierce wire cap.
    cap_arc_hole_delta_x = (HOLDER_PIPE_SIZE - PROFILE_HOLE_OFFSET) / math.sqrt (2)
    cap_arc_hole_delta_y = (HOLDER_PIPE_SIZE + PROFILE_HOLE_OFFSET) / math.sqrt (2)
    cap_arc_ball_to_side = BODY_THICKNESS + HOLDER_WIRE_SIZE/2
    cap_arc_ball_to_side_at_angle = cap_arc_ball_to_side * math.sqrt (2)
    cap_arc_hole_to_side_at_angle = cap_arc_hole_delta_y * math.sqrt (2)
    cap_arc_hole_depth = cap_arc_hole_to_side_at_angle - cap_arc_ball_to_side_at_angle
    cap_arc_ball_delta_x = cap_arc_hole_delta_x - cap_arc_hole_depth / math.sqrt (2)
    cap_arc_ball_offset = ivar.STAND_DEPTH + cap_arc_ball_delta_x

    cap_lead_hole = cylinder_along_x (BODY_THICKNESS + cap_arc_ball_offset + OVERLAP, HOLDER_WIRE_SIZE)
    cap_lead_hole = translate ((0 - BODY_THICKNESS - OVERLAP, cap_arc_ball_to_side, cap_arc_ball_to_side)) (cap_lead_hole)
    cap -= cap_lead_hole

    cap_arc_hole = cylinder_along_z (cap_arc_hole_depth + OVERLAP, HOLDER_WIRE_SIZE)
    cap_arc_hole = translate ((0, 0, HOLDER_PIPE_SIZE - cap_arc_hole_depth + OVERLAP)) (cap_arc_hole)
    cap_arc_hole = translate ((0 - PROFILE_HOLE_OFFSET, 0 - PROFILE_HOLE_OFFSET, 0)) (cap_arc_hole)
    cap_arc_hole = rotate ((0, 45, 0)) (cap_arc_hole)
    cap_arc_hole = translate ((ivar.STAND_DEPTH, cap_lead_height, 0)) (cap_arc_hole)
    cap -= cap_arc_hole

    cap_arc_ball = translate ((cap_arc_ball_offset, cap_arc_ball_to_side, cap_arc_ball_to_side)) (sphere (HOLDER_WIRE_SIZE/2))
    cap -= cap_arc_ball

    cap = mirror ((0, 0, 1)) (cap)

    # Construct shelf hook.
    hook_width = ivar.STAND_PIN_HOLE_TO_EDGE + PIN_RADIUS
    hook_height = cap_lead_height + HOLDER_SHELF_HEIGHT + HOLDER_PIPE_SIZE

    hook = union () (
        translate ((0, 0, 0 - BODY_THICKNESS)) (
            cube ((ivar.STAND_DEPTH, hook_height, BODY_THICKNESS))),
        translate ((0 - BODY_THICKNESS, 0, 0)) (
            cube ((BODY_THICKNESS, hook_height, hook_width))),
        translate ((0 - BODY_THICKNESS, cap_lead_height + HOLDER_SHELF_HEIGHT, 0 - HOLDER_PIPE_SIZE)) (
            cube ((BODY_THICKNESS + ivar.STAND_DEPTH, BODY_THICKNESS, HOLDER_PIPE_SIZE))),
        translate ((0 - BODY_THICKNESS, 0, 0 - BODY_THICKNESS)) (
            cube ((BODY_THICKNESS + OVERLAP, hook_height, BODY_THICKNESS + OVERLAP))))

    # Pierce hook side.
    hook_hole_size = PIN_RADIUS*2*PIERCING_SCALE
    hook_hole_offset = HOLDER_PIPE_SIZE + HOLDER_SHELF_HEIGHT - ivar.SHELF_PIERCING_TO_SURFACE
    hook_hole = translate ((0 - BODY_THICKNESS - OVERLAP, hook_hole_offset, ivar.STAND_PIN_HOLE_TO_EDGE)) (
        cylinder_along_x (BODY_THICKNESS + OVERLAP*2, hook_hole_size))
    hook_slot_x = translate ((0 - BODY_THICKNESS - OVERLAP, 0 - OVERLAP, ivar.STAND_PIN_HOLE_TO_EDGE)) (
        cube ((BODY_THICKNESS + OVERLAP*2, hook_hole_offset + hook_hole_size/2 + OVERLAP, ivar.STAND_WIDTH)))
    hook_slot_y = translate ((0 - BODY_THICKNESS - OVERLAP, 0 - OVERLAP, ivar.STAND_PIN_HOLE_TO_EDGE - hook_hole_size/2)) (
        cube ((BODY_THICKNESS + OVERLAP*2, hook_hole_offset + OVERLAP, ivar.STAND_WIDTH)))
    hook -= hook_hole + hook_slot_x + hook_slot_y

    return hook + cap


# The circular pin hat maybe looks better.
# The square pin hat can be printed horizontally.
# With layers aligned horizontally it is stronger.
# But the layers may also peel off when inserted.

def holder_pin_circular ():
    stalk = up (BODY_THICKNESS) (pin (PIN_RADIUS, PIN_THICKNESS, ivar.PIN_LENGTH + BODY_THICKNESS, True, False))
    hat = cylinder (h = BODY_THICKNESS + OVERLAP, r = PIN_HAT)
    return stalk + hat


def holder_pin_square ():
    stalk = up (BODY_THICKNESS) (pin (PIN_RADIUS, PIN_THICKNESS, ivar.PIN_LENGTH + BODY_THICKNESS, True, False))
    hat = up ((BODY_THICKNESS + OVERLAP) / 2) (cube ((2 * PIN_HAT, 2 * PIN_RADIUS, BODY_THICKNESS + OVERLAP), center = True))
    return stalk + hat


def holder_pin_module ():

    stalk = translate ((ivar.PIN_DISTANCE_HORIZONTAL/2, 0, 0)) (pin (PIN_RADIUS, PIN_THICKNESS, ivar.PIN_LENGTH, True, False))

    inner_x_bottom = MODULE_WIDTH_BOTTOM/2
    inner_y_bottom = BODY_THICKNESS
    inner_x_top = MODULE_WIDTH_TOP/2
    inner_y_top = BODY_THICKNESS + MODULE_HEIGHT
    outer_x_bottom = inner_x_bottom + BODY_THICKNESS
    outer_y_bottom = inner_y_bottom - BODY_THICKNESS
    outer_x_top = inner_x_top + BODY_THICKNESS
    outer_y_top = inner_y_top + BODY_THICKNESS

    sketch = polygon (
        [
            (0, outer_y_bottom), (outer_x_bottom, outer_y_bottom), (outer_x_top, outer_y_top), (0, outer_y_top),
            (0, inner_y_bottom), (inner_x_bottom, inner_y_bottom), (inner_x_top, inner_y_top), (0, inner_y_top),
        ],
        [[0, 1, 2, 3], [4, 5, 6, 7]])
    wrap = linear_extrude (2 * PIN_RADIUS) (sketch)
    wrap = rotate ((-90, 0, 0)) (wrap)
    wrap = translate ((0, 0 - PIN_RADIUS, 0)) (wrap)

    half = stalk + wrap
    twin = mirror ((1, 0, 0)) (half)

    return half + twin


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

    base = translate ((0, 0 - WIRE_CATCH_LENGTH, 0)) (
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

    # Holes for holding the box.
    piercing_offset_x = ivar.STAND_WIDTH/2 - ivar.STAND_PIN_HOLE_TO_EDGE
    piercing_offset_y = ivar.PIN_DISTANCE_VERTICAL - (MODULE_LENGTH % ivar.PIN_DISTANCE_VERTICAL) / 2
    piercing_base = translate ((ivar.STAND_WIDTH/2, piercing_offset_y, 0 - OVERLAP)) (
        scale ((PIERCING_SCALE, PIERCING_SCALE, 1)) (
            pin (PIN_RADIUS, PIN_THICKNESS, ivar.PIN_LENGTH, True, False)))
    piercing_one = translate ((0 + piercing_offset_x, 0, 0)) (piercing_base)
    piercing_two = translate ((0 - piercing_offset_x, 0, 0)) (piercing_base)
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

    hole_offset_x = (WIRE_LIGHT_HOLE_SIZE - WIRE_LIGHT_HOLE_OVERLAP)/2
    hole_base = translate ((ivar.STAND_WIDTH/2, WIRE_BOX_LENGTH - BODY_THICKNESS - OVERLAP, BODY_THICKNESS + WIRE_LIGHT_HOLE_SIZE/2)) (
        cylinder_along_y (BODY_THICKNESS + OVERLAP*2, WIRE_LIGHT_HOLE_SIZE))
    hole_one = translate ((0 + hole_offset_x, 0, 0)) (hole_base)
    hole_two = translate ((0 - hole_offset_x, 0, 0)) (hole_base)
    box -= hole_one + hole_two

    pin_offset_x = WIRE_LIGHT_HOLE_SIZE/2 * WIRE_SQUEEZE_SCALE + WIRE_SQUEEZE_SIZE/2
    pin_base = translate ((ivar.STAND_WIDTH/2, WIRE_BOX_LENGTH*3/4, 0)) (cylinder_along_z (BODY_THICKNESS + WIRE_LIGHT_HOLE_SIZE*3, WIRE_SQUEEZE_SIZE))
    pin_one = translate ((0 + pin_offset_x, 0, 0)) (pin_base)
    pin_two = translate ((0 - pin_offset_x, 0, 0)) (pin_base)
    box += pin_one + pin_two

    return box


def wire_box_hi_power():

    box = wire_box()

    hole = translate ((BODY_THICKNESS + WIRE_POWER_HOLE_SIZE/2, WIRE_BOX_LENGTH - BODY_THICKNESS - OVERLAP, BODY_THICKNESS + WIRE_POWER_HOLE_SIZE/2)) (
        cylinder_along_y (BODY_THICKNESS + OVERLAP*2, WIRE_POWER_HOLE_SIZE))
    box -= hole

    pin_offset_x = WIRE_POWER_HOLE_SIZE/2 * WIRE_SQUEEZE_SCALE + WIRE_SQUEEZE_SIZE/2
    pin_base = translate ((ivar.STAND_WIDTH/2, WIRE_BOX_LENGTH*3/4, 0)) (cylinder_along_z (BODY_THICKNESS + WIRE_POWER_HOLE_SIZE*3/2, WIRE_SQUEEZE_SIZE))
    pin_one = translate ((0 + pin_offset_x, 0, 0)) (pin_base)
    pin_two = translate ((0 - pin_offset_x, 0, 0)) (pin_base)
    box += pin_one + pin_two

    return box


def wire_lid ():

    base = translate ((0, 0 - WIRE_CATCH_LENGTH, 0)) (
        cube ((ivar.STAND_WIDTH, WIRE_BOX_LENGTH + WIRE_CATCH_LENGTH, BODY_THICKNESS)))

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


scad_render_to_file (holder_wire (), 'holder_wire.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (holder_bent (), 'holder_bent.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (wire_box_hi_power (), 'wire_box_hi_power.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (wire_box_lo_power (), 'wire_box_lo_power.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (wire_lid (), 'wire_lid.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (holder_pin_module (), 'holder_pin_module.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (holder_pin_square (), 'holder_pin_square.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (holder_pin_circular (), 'holder_pin_circular.scad', file_header = f'$fn = {SEGMENTS};')
