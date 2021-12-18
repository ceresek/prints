#!/usr/bin/env python3

import math

from solid import *
from solid.utils import *

from components.common import *


SEGMENTS = 111

PHONE_WIDTH = 80
PHONE_HEIGHT = 166
PHONE_THICKNESS = 16

WALL_THICKNESS = 1.67
WALL_RADIUS = 3
WALL_OFFSET = 3

HOOK_WIDTH = 55
HOOK_DEPTH = 11
HOOK_CATCH = 11

BACK_WIDTH = PHONE_WIDTH + 2*WALL_THICKNESS + WALL_OFFSET
BACK_HEIGHT = PHONE_HEIGHT + 2*WALL_THICKNESS + WALL_OFFSET
BACK_THICKNESS = 3
BACK_ADJUST = 6.6
BACK_SLOPE = 33
BACK_BENT = 18

HEX_GAP = 0.86
HEX_RADIUS = 10
HEX_THICKNESS = 0.86

INSERT_SLACK = 0.135
INSERT_OVERLAP = 1
INSERT_THICKNESS = 1


def rounded_box (size, radius):

    corner = cylinder (r = radius, h = size [Z])
    ll_corner = translate ((radius, radius, 0)) (corner)
    lr_corner = translate ((size [X] - radius, radius, 0)) (corner)
    ul_corner = translate ((radius, size [Y] - radius, 0)) (corner)
    ur_corner = translate ((size [X] - radius, size [Y] - radius, 0)) (corner)

    return hull () (ll_corner + lr_corner + ul_corner + ur_corner)


HEX_SCALE_LONGER = math.cos (math.pi*1/6)
HEX_SCALE_SHORTER = math.cos (math.pi*2/6)

def hexagrid_spacing_vertical (gap, radius):
    return (radius * HEX_SCALE_SHORTER + radius + gap * HEX_SCALE_LONGER)

def hexagrid_overlap_vertical (gap, radius):
    return (radius * HEX_SCALE_SHORTER + gap / HEX_SCALE_LONGER + gap / HEX_SCALE_LONGER / 2)

def hexagrid_spacing_horizontal (gap, radius):
    return (2 * radius * HEX_SCALE_LONGER + gap)

def hexagrid_overlap_horizontal (gap, radius):
    return (gap)

def hexagrid_size_to_rows_cols (size, gap, radius):

    inner_horizontal = size [X] - hexagrid_overlap_horizontal (gap, radius)
    inner_vertical = size [Y] - hexagrid_overlap_vertical (gap, radius)

    cols = math.ceil (inner_horizontal / hexagrid_spacing_horizontal (gap, radius))
    rows = math.floor (math.ceil (inner_vertical / hexagrid_spacing_vertical (gap, radius)) / 2) * 2 + 1

    return ( rows, cols )

def size_to_hexagrid_size (size, gap, radius):

    rows, cols = hexagrid_size_to_rows_cols (size, gap, radius)

    outer_horizontal = cols * hexagrid_spacing_horizontal (gap, radius) + hexagrid_overlap_horizontal (gap, radius)
    outer_vertical = rows * hexagrid_spacing_vertical (gap, radius) + hexagrid_overlap_vertical (gap, radius)

    return ( outer_horizontal, outer_vertical, size [Z] )


def hexagon (radius, rim, thickness):
    outer = cylinder (r = radius + rim / HEX_SCALE_LONGER, h = thickness, segments = 6)
    inner = translate ((0, 0, 0 - OVERLAP)) (cylinder (r = radius, h = thickness + 2*OVERLAP, segments = 6))
    return rotate ((0, 0, 30)) (outer - inner)


def hexagrid (rows, cols, gap, radius, thickness):

    spacing_vertical = 2*hexagrid_spacing_vertical (gap, radius)
    spacing_horizontal = hexagrid_spacing_horizontal (gap, radius)

    element = translate ((gap + radius * HEX_SCALE_LONGER, gap / HEX_SCALE_LONGER + radius, 0)) (hexagon (radius, gap, thickness))

    grid_row_longer_list = [ translate ((spacing_horizontal*column, 0, 0)) (element) for column in range (cols) ]
    grid_row_longer = union () (*grid_row_longer_list)
    grid_rows_longer = [ translate ((0, spacing_vertical*row, 0)) (grid_row_longer) for row in range (math.ceil (rows/2)) ]

    grid_row_shorter_list = [ translate ((spacing_horizontal*column + spacing_horizontal/2, 0, 0)) (element) for column in range (cols-1) ]
    grid_row_shorter = union () (*grid_row_shorter_list)
    grid_rows_shorter = [ translate ((0, spacing_vertical*row + spacing_vertical/2, 0)) (grid_row_shorter) for row in range (math.floor (rows/2)) ]

    return union () (*grid_rows_longer, *grid_rows_shorter)


def holder_lower ():

    back_rows, back_cols = hexagrid_size_to_rows_cols ((BACK_WIDTH, BACK_WIDTH, 0), HEX_GAP, HEX_RADIUS)
    back_size = size_to_hexagrid_size ((BACK_WIDTH, BACK_WIDTH, BACK_THICKNESS), HEX_GAP, HEX_RADIUS)

    body_hex_gap = 3*HEX_GAP + 2*INSERT_SLACK
    body_hex_radius = HEX_RADIUS - (INSERT_SLACK + HEX_GAP)/HEX_SCALE_LONGER
    cutout_hex_gap = HEX_GAP + 2*INSERT_SLACK + 2*OVERLAP
    cutout_hex_radius = HEX_RADIUS - (INSERT_SLACK + OVERLAP)/HEX_SCALE_LONGER

    insert_body = translate ((0 - (HEX_GAP + INSERT_SLACK)/HEX_SCALE_LONGER, 0 - HEX_GAP - INSERT_SLACK, 0)) (
        hexagrid (back_rows, back_cols, body_hex_gap, body_hex_radius, INSERT_THICKNESS + INSERT_OVERLAP))
    insert_cutout = translate ((0 - OVERLAP/HEX_SCALE_LONGER, 0 - 2*hexagrid_spacing_vertical (cutout_hex_gap, cutout_hex_radius) - OVERLAP, 0 - OVERLAP)) (
        hexagrid (back_rows + 4, back_cols, cutout_hex_gap, cutout_hex_radius, INSERT_THICKNESS + OVERLAP))

    back = translate ((0, 0, INSERT_THICKNESS)) (
        hexagrid (back_rows, back_cols, HEX_GAP, HEX_RADIUS, BACK_THICKNESS + BACK_BENT))

    bent_radius = back_size [Y] ** 2 / BACK_BENT / 8 + BACK_BENT / 2
    hook_angle = math.degrees (math.asin (back_size [Y] / bent_radius / 2))

    bent = translate ((0 - OVERLAP, back_size [Y] / 2, INSERT_THICKNESS + BACK_THICKNESS + bent_radius)) (
        rotate ((0, 90, 0)) (
            cylinder (r = bent_radius, h = back_size [X] + 2*OVERLAP)))

    hook = union () (
        rounded_box ((HOOK_WIDTH, HOOK_DEPTH + WALL_OFFSET + WALL_THICKNESS, WALL_THICKNESS), WALL_RADIUS),
        translate ((0, HOOK_DEPTH + WALL_OFFSET + WALL_THICKNESS, 0)) (
            rotate ((90 - hook_angle, 0, 0)) (
                rounded_box ((HOOK_WIDTH, HOOK_CATCH + WALL_THICKNESS, WALL_THICKNESS), WALL_RADIUS))))

    hook = translate (((back_size [X] - HOOK_WIDTH)/2, back_size [Y] - WALL_OFFSET, BACK_THICKNESS + BACK_BENT - WALL_OFFSET)) (
        rotate ((90 + hook_angle + BACK_ADJUST, 0, 0)) (
            hook))

    return insert_body - insert_cutout + back - bent + hook


def holder_upper ():

    back_rows, back_cols = hexagrid_size_to_rows_cols ((BACK_WIDTH, BACK_HEIGHT, 0), HEX_GAP, HEX_RADIUS)
    back_size = size_to_hexagrid_size ((BACK_WIDTH, BACK_HEIGHT, BACK_THICKNESS), HEX_GAP, HEX_RADIUS)
    wall_ratio = BACK_SLOPE / back_size [X]
    wall_angle = math.atan (wall_ratio)
    wall_reduce_width = math.cos (wall_angle)
    wall_reduce_height = math.sin (wall_angle)
    slope_size = ( back_size [X] + 2*OVERLAP, back_size [Y] + 2*OVERLAP, back_size [Z] + BACK_SLOPE + OVERLAP)

    back = hexagrid (back_rows, back_cols, HEX_GAP, HEX_RADIUS, BACK_THICKNESS + BACK_SLOPE)
    slope = multmatrix ((
        (1, 0, 0, 0 - OVERLAP),
        (0, 1, 0, 0 - OVERLAP),
        (0 - wall_ratio, 0, 1, BACK_SLOPE + BACK_THICKNESS),
        (0, 0, 0, 1))) (
            cube (slope_size))

    wall_right = translate ((back_size [X] - WALL_OFFSET * wall_reduce_width, WALL_OFFSET, WALL_OFFSET * wall_reduce_height)) (
        rotate ((0, math.degrees (wall_ratio) - 90, 0)) (
            rounded_box ((PHONE_THICKNESS + BACK_THICKNESS, back_size [Y] - 2*WALL_OFFSET, WALL_THICKNESS), WALL_RADIUS)
        )
    )

    bottom_wall_width = (back_size [X] / wall_reduce_width - 4 * WALL_OFFSET) / 3

    wall_bottom_left = translate ((WALL_OFFSET * wall_reduce_width, WALL_OFFSET + WALL_THICKNESS, BACK_SLOPE - WALL_OFFSET * wall_reduce_height)) (
        rotate ((90, math.degrees (wall_angle), 0)) (
            rounded_box ((bottom_wall_width, PHONE_THICKNESS + BACK_THICKNESS, WALL_THICKNESS), WALL_RADIUS)
        )
    )

    wall_bottom_right = translate ((back_size [X] - (bottom_wall_width + WALL_OFFSET) * wall_reduce_width, WALL_OFFSET + WALL_THICKNESS, (bottom_wall_width + WALL_OFFSET) * wall_reduce_height)) (
        rotate ((90, math.degrees (wall_angle), 0)) (
            rounded_box ((bottom_wall_width, PHONE_THICKNESS + BACK_THICKNESS, WALL_THICKNESS), WALL_RADIUS)
        )
    )

    return back - slope + wall_right + wall_bottom_left + wall_bottom_right


scad_render_to_file (holder_lower (), 'holder_lower.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (holder_upper (), 'holder_upper.scad', file_header = f'$fn = {SEGMENTS};')
