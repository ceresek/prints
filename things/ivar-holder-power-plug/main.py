#!/usr/bin/env python3

import math

from solid import *
from solid.utils import *

from components.common import *

from helpers import ivar


SEGMENTS = 111

WALL_THICKNESS = 3
BACK_THICKNESS = 8

HEX_RIM = 1.67
HEX_RADIUS = 6
HEX_THICKNESS = 1.67

GAP_DEPTH = 20
GAP_WIDTH = 40
PLUG_WIDTH = 80
STAND_SIZE = 20
RUNG_OVERLAP = 10

RUNG_TO_HOLE_LOWER = 21
RUNG_TO_HOLE_UPPER = 3

SCREW_LENGTH = 17
SCREW_RADIUS = 2
SPACER_RADIUS = 6
SPACER_HEIGHT = 1.2
TOP_NUT_RADIUS = 4
TOP_NUT_HEIGHT = 4
BOTTOM_NUT_RADIUS = 8
BOTTOM_NUT_HEIGHT = 5
BOTTOM_NUT_DEPTH = GAP_DEPTH - SCREW_LENGTH + BOTTOM_NUT_HEIGHT + SPACER_HEIGHT

THORN_RADIUS_LOWER = 5/2
THORN_RADIUS_UPPER = 4/2
THORN_DEPTH = 1

PIN_CAP_WIDTH = 11
PIN_THICKNESS = 1.67
PIN_HOLE_SCALE = 1.1

TOP_SCREW_OFFSET = 12
TOP_PIN_OFFSET = 35

BOTTOM_SCREW_OFFSET = 23
BOTTOM_CUTOUT_WIDTH = GAP_WIDTH
BOTTOM_CUTOUT_HEIGHT = 28
BOTTOM_PIN_OFFSET = 54

BODY_PIN_GAP = 11
TOP_BODY_HEIGHT = TOP_PIN_OFFSET + ivar.PIN_DISTANCE_VERTICAL*2 + BODY_PIN_GAP
BOTTOM_BODY_HEIGHT = BOTTOM_PIN_OFFSET + ivar.PIN_DISTANCE_VERTICAL*2 + BODY_PIN_GAP


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


def hexagon (radius, thickness):
    return rotate ((0, 0, 30)) (cylinder (r = radius, h = thickness, segments = 6))


def hexagrid_spacing_vertical (gap, radius):
    return (3*radius + 2*gap*math.cos (math.pi/6))/2

def hexagrid_spacing_horizontal (gap, radius):
    return 2*radius*math.cos (math.pi/6) + gap

def hexagrid (rows, cols, gap, radius, thickness):

    spacing_vertical = 2*hexagrid_spacing_vertical (gap, radius)
    spacing_horizontal = hexagrid_spacing_horizontal (gap, radius)

    element = translate ((radius*math.cos (math.pi/6), radius, 0)) (hexagon (radius, thickness))

    grid_row_longer_list = [ translate ((spacing_horizontal*column, 0, 0)) (element) for column in range (cols) ]
    grid_row_longer = union () (*grid_row_longer_list)
    grid_rows_longer = [ translate ((0, spacing_vertical*row, 0)) (grid_row_longer) for row in range ((rows+1)//2) ]

    grid_row_shorter_list = [ translate ((spacing_horizontal*column + spacing_horizontal/2, 0, 0)) (element) for column in range (cols-1) ]
    grid_row_shorter = union () (*grid_row_shorter_list)
    grid_rows_shorter = [ translate ((0, spacing_vertical*row + spacing_vertical/2, 0)) (grid_row_shorter) for row in range (rows//2) ]

    return union () (*grid_rows_longer, *grid_rows_shorter)


def hexagrid_pierced_slab (size, gap, radius, rim):

    piercing_spacing_vertical = hexagrid_spacing_vertical (gap, radius)
    piercing_spacing_horizontal = hexagrid_spacing_horizontal (gap, radius)

    cols = int (size [X] // piercing_spacing_horizontal) + 2
    rows = int (size [Y] // piercing_spacing_vertical) + 1

    centering_vertical = (size [Y] - (piercing_spacing_vertical * (rows-1)) - gap*math.cos (math.pi/6)/2) / 2
    centering_horizontal = (size [X] - (piercing_spacing_horizontal * (cols-2)) - gap) / 2

    body = cube (size)

    piercing = translate ((0 - centering_horizontal, 0 - centering_vertical, 0 - OVERLAP)) (
        hexagrid (rows, cols, gap, radius, size [Z] + 2*OVERLAP))

    rim = translate ((rim, rim, -OVERLAP)) (
        cube ((size [X] - 2*rim, size [Y] - 2*rim, size [Z] + 2*OVERLAP)))

    return (body - piercing) + (body - rim)


def pin_hole ():

    hole = rotate ((90, 0, 90)) (
        scale ((PIN_HOLE_SCALE, PIN_HOLE_SCALE, 1)) (
            pin (ivar.PIN_RADIUS_SMALL, PIN_THICKNESS, WALL_THICKNESS + 2 * OVERLAP, False, False)))

    return hole


def screw_hole ():

    top_spacer = translate ((0, 0, GAP_DEPTH - SPACER_HEIGHT - OVERLAP)) (cylinder (r = SPACER_RADIUS, h = SPACER_HEIGHT + 2*OVERLAP))
    top_nut = translate ((0, 0, GAP_DEPTH - SPACER_HEIGHT - TOP_NUT_HEIGHT - OVERLAP)) (cylinder (r = TOP_NUT_RADIUS, h = TOP_NUT_HEIGHT + 2*OVERLAP))
    bottom_nut = translate ((0, 0, 0 - OVERLAP)) (cylinder (r = BOTTOM_NUT_RADIUS, h = BOTTOM_NUT_DEPTH + 2*OVERLAP))
    bottom_spacer = translate ((0, 0, BOTTOM_NUT_DEPTH - OVERLAP)) (cylinder (r = SPACER_RADIUS, h = SPACER_HEIGHT + 2*OVERLAP))
    screw = cylinder (r = SCREW_RADIUS, h = GAP_DEPTH)

    return screw + top_spacer + top_nut + bottom_spacer + bottom_nut


def screw_holder ():

    holder = cylinder (r = BOTTOM_NUT_RADIUS + WALL_THICKNESS, h = GAP_DEPTH)

    thorn = translate ((0, 0 - SPACER_RADIUS - THORN_RADIUS_LOWER, GAP_DEPTH - OVERLAP)) (cylinder (r1 = THORN_RADIUS_LOWER, r2 = THORN_RADIUS_UPPER, h = THORN_DEPTH + OVERLAP))

    return holder + thorn


def holder_lower ():

    back = hexagrid_pierced_slab ((PLUG_WIDTH + GAP_WIDTH, BOTTOM_BODY_HEIGHT, BACK_THICKNESS), HEX_THICKNESS, HEX_RADIUS, HEX_RIM)

    stand_left_bottom = translate ((0, 0 - RUNG_OVERLAP, 0)) (cube ((STAND_SIZE, STAND_SIZE + RUNG_OVERLAP, GAP_DEPTH)))
    stand_right_bottom = translate ((PLUG_WIDTH - STAND_SIZE, 0 - RUNG_OVERLAP, 0)) (cube ((STAND_SIZE, STAND_SIZE + RUNG_OVERLAP, GAP_DEPTH)))
    stand_left_top = translate ((0, BOTTOM_BODY_HEIGHT - STAND_SIZE, 0)) (cube ((STAND_SIZE, STAND_SIZE, GAP_DEPTH)))
    stand_right_top = translate ((PLUG_WIDTH - STAND_SIZE, BOTTOM_BODY_HEIGHT - STAND_SIZE, 0)) (cube ((STAND_SIZE, STAND_SIZE, GAP_DEPTH)))

    fold = translate ((PLUG_WIDTH + GAP_WIDTH - WALL_THICKNESS, 0, 0)) (
        cube ((WALL_THICKNESS, BOTTOM_BODY_HEIGHT, ivar.STAND_WIDTH / 2 + ivar.STAND_DESK_GAP)))
    ridge = translate ((0, 0, 0)) (
        cube ((PLUG_WIDTH, WALL_THICKNESS, GAP_DEPTH + ivar.STAND_RUNG_WIDTH)))

    screw_holder_object = translate ((PLUG_WIDTH/2, BOTTOM_SCREW_OFFSET, 0)) (screw_holder ())

    screw_hole_object = translate ((PLUG_WIDTH/2, BOTTOM_SCREW_OFFSET, 0)) (screw_hole ())

    pin_hole_offset = BOTTOM_PIN_OFFSET
    pin_holes = []
    while pin_hole_offset < BOTTOM_BODY_HEIGHT - ivar.PIN_RADIUS_LARGE:
        pin_hole_object = translate ((PLUG_WIDTH + GAP_WIDTH - WALL_THICKNESS - OVERLAP, pin_hole_offset, ivar.STAND_PIN_HOLE_TO_EDGE + ivar.STAND_DESK_GAP)) (pin_hole ())
        pin_hole_offset += ivar.PIN_DISTANCE_VERTICAL
        pin_holes.append (pin_hole_object)

    cutout_hole = translate ((PLUG_WIDTH + GAP_WIDTH - BOTTOM_CUTOUT_WIDTH - OVERLAP, 0 - OVERLAP, 0 - OVERLAP)) (
        cube ((BOTTOM_CUTOUT_WIDTH + OVERLAP*2, BOTTOM_CUTOUT_HEIGHT + OVERLAP*2, ivar.STAND_WIDTH + OVERLAP*2)))
    cutout_rim = translate ((PLUG_WIDTH + GAP_WIDTH - BOTTOM_CUTOUT_WIDTH - HEX_RIM, 0, 0)) (
        cube ((BOTTOM_CUTOUT_WIDTH + HEX_RIM, BOTTOM_CUTOUT_HEIGHT + HEX_RIM, BACK_THICKNESS)))

    stands = stand_left_bottom + stand_right_bottom + stand_left_top + stand_right_top + screw_holder_object
    holes = screw_hole_object + union () (*pin_holes)
    bases = fold + ridge + back

    return stands + bases - holes + cutout_rim - cutout_hole


def holder_upper ():

    back = hexagrid_pierced_slab ((PLUG_WIDTH + GAP_WIDTH, TOP_BODY_HEIGHT, BACK_THICKNESS), HEX_THICKNESS, HEX_RADIUS, HEX_RIM)

    stand_left_bottom = translate ((0, 0, 0)) (cube ((STAND_SIZE, STAND_SIZE, GAP_DEPTH)))
    stand_right_bottom = translate ((PLUG_WIDTH - STAND_SIZE, 0, 0)) (cube ((STAND_SIZE, STAND_SIZE, GAP_DEPTH)))
    stand_left_top = translate ((0, TOP_BODY_HEIGHT - STAND_SIZE, 0)) (cube ((STAND_SIZE, STAND_SIZE + RUNG_OVERLAP, GAP_DEPTH)))
    stand_right_top = translate ((PLUG_WIDTH - STAND_SIZE, TOP_BODY_HEIGHT - STAND_SIZE, 0)) (cube ((STAND_SIZE, STAND_SIZE + RUNG_OVERLAP, GAP_DEPTH)))

    fold = translate ((PLUG_WIDTH + GAP_WIDTH - WALL_THICKNESS, 0, 0)) (
        cube ((WALL_THICKNESS, TOP_BODY_HEIGHT, ivar.STAND_WIDTH / 2 + ivar.STAND_DESK_GAP)))

    screw_holder_object = translate ((PLUG_WIDTH/2, TOP_BODY_HEIGHT - TOP_SCREW_OFFSET, 0)) (screw_holder ())
    screw_hole_object = translate ((PLUG_WIDTH/2, TOP_BODY_HEIGHT - TOP_SCREW_OFFSET, 0)) (screw_hole ())

    pin_hole_offset = TOP_BODY_HEIGHT - TOP_PIN_OFFSET
    pin_holes = []
    while pin_hole_offset > ivar.PIN_RADIUS_LARGE:
        pin_hole_object = translate ((PLUG_WIDTH + GAP_WIDTH - WALL_THICKNESS - OVERLAP, pin_hole_offset, ivar.STAND_PIN_HOLE_TO_EDGE + ivar.STAND_DESK_GAP)) (pin_hole ())
        pin_hole_offset -= ivar.PIN_DISTANCE_VERTICAL
        pin_holes.append (pin_hole_object)

    stands = stand_left_bottom + stand_right_bottom + stand_left_top + stand_right_top + screw_holder_object
    holes = screw_hole_object + union () (*pin_holes)
    bases = fold + back

    return stands + bases - holes


def holder_pin ():

    cap = cube ((PIN_CAP_WIDTH, ivar.PIN_RADIUS_SMALL*2, PIN_THICKNESS), center = True)
    body = pin (ivar.PIN_RADIUS_SMALL, PIN_THICKNESS, WALL_THICKNESS + PIN_THICKNESS / 2 + ivar.PIN_LENGTH, True, False)

    return cap + body


scad_render_to_file (holder_pin (), 'holder_pin.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (holder_lower (), 'holder_lower.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (holder_upper (), 'holder_upper.scad', file_header = f'$fn = {SEGMENTS};')
