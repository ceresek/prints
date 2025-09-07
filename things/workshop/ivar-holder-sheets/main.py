#!/usr/bin/env python3

import math as _math

from solid2 import *
from solid2.extensions.bosl2 import *

from components.common import *

from helpers import ivar


set_global_fn (111)


OVERLAP = 0.001

BRACKET_THICKNESS = FOR_PERIMETERS

BRACKET_PIN_OFFSET = 19

HOLDER_HEIGHT = ivar.PIN_DISTANCE_VERTICAL + BRACKET_PIN_OFFSET*2

BRACKET_PIERCING_CELL_GAP = TRE_PERIMETERS
BRACKET_PIERCING_CELL_RADIUS = 3.4

SLOT_COUNT = 3
SLOT_WIDTH = 2
SLOT_DEPTH = 22
SLOT_DESCENT = 10
SLOT_THICKNESS = 3

SLOT_BRACKET_OVERLAP = 10

SLOT_PRIMARY_CHAMFER_ANGLE_RAD = _math.atan (SLOT_DESCENT / (SLOT_WIDTH + SLOT_THICKNESS))
SLOT_PRIMARY_CHAMFER_ANGLE_DEG = _math.degrees (SLOT_PRIMARY_CHAMFER_ANGLE_RAD)
SLOT_SECONDARY_CHAMFER_ANGLE_DEG = 45
SLOT_SECONDARY_CHAMFER_ANGLE_RAD = _math.radians (SLOT_SECONDARY_CHAMFER_ANGLE_DEG)
SLOT_SECONDARY_CHAMFER_DEPTH = 10

PIN_DEPTH = 3.3
PIN_CHAMFER = 2.2


def _hexagon (radius, thickness):
    return rotate ((0, 0, 30)) (cylinder (r = radius, h = thickness, _fn = 6))


def hexagrid_spacing_vertical (gap, radius):
    return (3*radius + 2*gap*_math.cos (_math.pi/6))/2

def hexagrid_spacing_horizontal (gap, radius):
    return 2*radius*_math.cos (_math.pi/6) + gap

def hexagrid (rows, cols, gap, radius, thickness):

    spacing_vertical = 2*hexagrid_spacing_vertical (gap, radius)
    spacing_horizontal = hexagrid_spacing_horizontal (gap, radius)

    element = translate ((radius*_math.cos (_math.pi/6), radius, 0)) (_hexagon (radius, thickness))

    grid_row_longer_list = [ translate ((spacing_horizontal*column, 0, 0)) (element) for column in range (cols) ]
    grid_row_longer = union () (*grid_row_longer_list)
    grid_rows_longer = [ translate ((0, spacing_vertical*row, 0)) (grid_row_longer) for row in range ((rows+1)//2) ]

    grid_row_shorter_list = [ translate ((spacing_horizontal*column + spacing_horizontal/2, 0, 0)) (element) for column in range (cols-1) ]
    grid_row_shorter = union () (*grid_row_shorter_list)
    grid_rows_shorter = [ translate ((0, spacing_vertical*row + spacing_vertical/2, 0)) (grid_row_shorter) for row in range (rows//2) ]

    return union () (*grid_rows_longer, *grid_rows_shorter)


def hexagrid_pierced_wall (size, gap, radius, rim):

    piercing_spacing_vertical = hexagrid_spacing_vertical (gap, radius)
    piercing_spacing_horizontal = hexagrid_spacing_horizontal (gap, radius)

    cols = int (size [X] // piercing_spacing_horizontal) + 2
    rows = int (size [Z] // piercing_spacing_vertical) + 1

    centering_vertical = (size [Z] - (piercing_spacing_vertical * (rows-1)) - gap*_math.cos (_math.pi/6)/2) / 2
    centering_horizontal = (size [X] - (piercing_spacing_horizontal * (cols-2)) - gap) / 2

    body = cube (size)

    piercing = translate ((0 - centering_horizontal, size [Y] + OVERLAP, 0 - centering_vertical)) (
        rotate ((90, 0, 0)) (
            hexagrid (rows, cols, gap, radius, size [Y] + 2*OVERLAP)))

    rim = translate ((rim, -OVERLAP, rim)) (
        cube ((size [X] - 2*rim, size [Y] + 2*OVERLAP, size [Z] - 2*rim)))

    return (body - piercing) + (body - rim)


def bracket_grid (shift):

    rim = BRACKET_THICKNESS + ivar.STAND_CHAMFER

    bottom = translate ((-ivar.STAND_WIDTH/2, -BRACKET_THICKNESS, 0)) (
        hexagrid_pierced_wall ((ivar.STAND_WIDTH/2 + BRACKET_THICKNESS, BRACKET_THICKNESS, HOLDER_HEIGHT), BRACKET_PIERCING_CELL_GAP, BRACKET_PIERCING_CELL_RADIUS, rim))
    side = translate ((BRACKET_THICKNESS, 0, 0)) (
        rotate ((0, 0, 90)) (
            hexagrid_pierced_wall ((ivar.STAND_DEPTH + BRACKET_THICKNESS*2, BRACKET_THICKNESS, HOLDER_HEIGHT), BRACKET_PIERCING_CELL_GAP, BRACKET_PIERCING_CELL_RADIUS, rim)))
    top = translate ((-ivar.STAND_WIDTH/2, ivar.STAND_DEPTH, 0)) (
        hexagrid_pierced_wall ((ivar.STAND_WIDTH/2 + BRACKET_THICKNESS, BRACKET_THICKNESS, HOLDER_HEIGHT), BRACKET_PIERCING_CELL_GAP, BRACKET_PIERCING_CELL_RADIUS, rim))

    reinforcement_base = intersection () (
        cylinder (r = rim, h = HOLDER_HEIGHT, _fn = 4),
        cube ((rim, rim, HOLDER_HEIGHT)))
    reinforcement_bottom = translate ((BRACKET_THICKNESS, 0, 0)) (
        rotate ((0, 0, 90)) (
            reinforcement_base))
    reinforcement_top = translate ((BRACKET_THICKNESS, ivar.STAND_DEPTH, 0)) (
        rotate ((0, 0, 180)) (
            reinforcement_base))

    pin_base = (
        cyl (r = ivar.PIN_RADIUS_SMALL, h = BRACKET_THICKNESS + PIN_DEPTH + PIN_CHAMFER, chamfer2 = PIN_CHAMFER, anchor = BOTTOM)
        .down (BRACKET_THICKNESS)
        .rotate ([90, 0, 0])
        .left (ivar.STAND_PIN_HOLE_TO_EDGE + shift)
        .fwd (ivar.STAND_DEPTH)
        .up (BRACKET_PIN_OFFSET)
    )
    pin_count = int ((HOLDER_HEIGHT - BRACKET_PIN_OFFSET - 2*ivar.PIN_RADIUS_LARGE) // ivar.PIN_DISTANCE_VERTICAL) + 1
    pin_list = [translate ((0, 0, ivar.PIN_DISTANCE_VERTICAL * pin)) (pin_base) for pin in range (pin_count)]

    return union () (
        bottom, reinforcement_bottom,
        top, reinforcement_top,
        side, *pin_list)


def bracket_full (shift):

    face_wall = cuboid ((ivar.STAND_PIN_HOLE_TO_EDGE + ivar.PIN_RADIUS_SMALL + shift, BRACKET_THICKNESS, HOLDER_HEIGHT), rounding = BRACKET_THICKNESS, edges = [FRONT+LEFT], anchor = RIGHT+BACK+BOTTOM)
    side_wall = cuboid ((BRACKET_THICKNESS, ivar.STAND_DEPTH + 2*BRACKET_THICKNESS, HOLDER_HEIGHT), anchor = LEFT+FRONT+BOTTOM).fwd (BRACKET_THICKNESS)
    back_wall = cuboid ((ivar.STAND_PIN_HOLE_TO_EDGE + ivar.PIN_RADIUS_SMALL + shift, BRACKET_THICKNESS, HOLDER_HEIGHT), rounding = BRACKET_THICKNESS, edges = [BACK+LEFT], anchor = RIGHT+FRONT+BOTTOM).back (ivar.STAND_DEPTH)

    rows = _math.floor ((HOLDER_HEIGHT - BRACKET_PIN_OFFSET - ivar.PIN_RADIUS_SMALL) // ivar.PIN_DISTANCE_VERTICAL) + 1

    pin_base = (
        cyl (h = PIN_DEPTH + PIN_CHAMFER, r = ivar.PIN_RADIUS_SMALL, chamfer2 = PIN_CHAMFER, anchor = BOTTOM, orient = FORWARD)
        .left (ivar.STAND_PIN_HOLE_TO_EDGE + shift)
        .back (ivar.STAND_DEPTH)
        .up (BRACKET_PIN_OFFSET)
    )
    pin_list = [ pin_base.up (row * ivar.PIN_DISTANCE_VERTICAL) for row in range (rows) ]

    return face_wall + side_wall + back_wall + union () (*pin_list)


def slots ():

    width = SLOT_THICKNESS + (SLOT_WIDTH + SLOT_THICKNESS) * SLOT_COUNT
    depth = SLOT_THICKNESS + SLOT_DEPTH

    body = cube ((width, depth, HOLDER_HEIGHT))

    slot_base = translate ((SLOT_THICKNESS, SLOT_THICKNESS, SLOT_THICKNESS + SLOT_DESCENT*(SLOT_COUNT-1))) (
        cube ((SLOT_WIDTH, SLOT_DEPTH + OVERLAP, HOLDER_HEIGHT + OVERLAP)))
    slot_list = [translate (((SLOT_WIDTH+SLOT_THICKNESS)*slot, 0, -SLOT_DESCENT*slot)) (slot_base) for slot in range (SLOT_COUNT)]
    body -= union () (*slot_list)

    chamfer_primary = translate ((BRACKET_THICKNESS, -OVERLAP, HOLDER_HEIGHT)) (
        rotate ((0, SLOT_PRIMARY_CHAMFER_ANGLE_DEG, 0)) (
            cube ((width / _math.cos (SLOT_PRIMARY_CHAMFER_ANGLE_RAD), depth + 2*OVERLAP, HOLDER_HEIGHT))))

    chamfer_secondary_size = SLOT_SECONDARY_CHAMFER_DEPTH / _math.cos (SLOT_SECONDARY_CHAMFER_ANGLE_RAD)
    chamfer_secondary = translate ((SLOT_THICKNESS, depth - SLOT_SECONDARY_CHAMFER_DEPTH, HOLDER_HEIGHT)) (
        multmatrix (((1, 0, 0, 0), (0, 1, 0, 0), (-SLOT_DESCENT / (SLOT_WIDTH + SLOT_THICKNESS), 0, 1, 0), (0, 0, 0, 1))) (
            rotate ((-SLOT_SECONDARY_CHAMFER_ANGLE_DEG, 0, 0)) (
                cube ((width, chamfer_secondary_size, chamfer_secondary_size)))))

    return body - chamfer_primary - chamfer_secondary


def holder_grid (shift):

    holder = union () (
        translate ((0, 0, 0)) (bracket_grid (shift)),
        translate ((0, ivar.STAND_DEPTH - SLOT_BRACKET_OVERLAP - SLOT_THICKNESS, 0)) (slots ()),
    )

    return holder


def holder_full (shift):

    holder = union () (
        translate ((0, 0, 0)) (bracket_full (shift)),
        translate ((0, ivar.STAND_DEPTH - SLOT_BRACKET_OVERLAP - SLOT_THICKNESS, 0)) (slots ()),
    )

    return holder


holder_grid (0).save_as_scad ('holder-grid-zero.scad')
holder_grid (1).save_as_scad ('holder-grid-one.scad')
holder_grid (2).save_as_scad ('holder-grid-two.scad')
holder_full (0).save_as_scad ('holder-full-zero.scad')
holder_full (1).save_as_scad ('holder-full-one.scad')
holder_full (2).save_as_scad ('holder-full-two.scad')
