#!/usr/bin/env python3

import math as _math

from solid import *
from solid.utils import *

from components.common import *


SEGMENTS = 33


# Constants

TILE_HEIGHT_PIN = 5
TILE_WIDTH_PIN = 0.86
TILE_WIDTH_GAP = 0.43
TILE_DEPTH = 1.67
TILE_SLOPE = 40

TILE_PIN_RADIUS = 0.37
TILE_DIP_RADIUS = 0.48

TILE_SLACK = 0.08

TILE_WIDTH = TILE_WIDTH_PIN * 2 + TILE_WIDTH_GAP + TILE_SLACK * 2
TILE_HEIGHT_SUB = TILE_DEPTH * _math.tan (_math.radians (TILE_SLOPE))
TILE_HEIGHT_ALL = TILE_HEIGHT_PIN - TILE_HEIGHT_SUB + TILE_SLACK * 2

TILE_SEAM = TILE_DEPTH + TILE_SLACK

STAND_FLOOR_THICKNESS = 2
STAND_FLOOR_RATIO = 3/4

STAND_HEIGHT = 12.34

STAND_PATTERN_ROWS = 2
STAND_PATTERN_HEIGHT = TILE_HEIGHT_ALL * STAND_PATTERN_ROWS + TILE_HEIGHT_SUB
STAND_PATTERN_OFFSET = (STAND_HEIGHT - STAND_PATTERN_HEIGHT) / 2


# Measurements

def get_rounded_stand_dimension (dimension):

    # For a pattern to fit across stand seam,
    # the stand dimension plus the seam width
    # have to form a multiple of the pattern step.

    pattern_count = _math.ceil ((dimension + TILE_SEAM) / TILE_WIDTH / 2)
    pattern_dimension = pattern_count * TILE_WIDTH * 2 - TILE_SEAM

    return pattern_dimension


# Pattern

def do_tile_pattern (rows, columns):

    tile_ini = polyhedron (
        points = [
            # Bottom layer.
            (0, 0, 0), (TILE_WIDTH_PIN, 0, 0), (TILE_WIDTH_PIN, TILE_HEIGHT_PIN, 0), (0, TILE_HEIGHT_PIN, 0),
            # Top layer.
            (0, 0 + TILE_HEIGHT_SUB, TILE_DEPTH),
            (TILE_WIDTH_PIN, 0 + TILE_HEIGHT_SUB, TILE_DEPTH),
            (TILE_WIDTH_PIN, TILE_HEIGHT_PIN - TILE_HEIGHT_SUB, TILE_DEPTH),
            (0, TILE_HEIGHT_PIN - TILE_HEIGHT_SUB, TILE_DEPTH),
        ],
        faces = [
            # Bottom.
            (0, 1, 2, 3),
            # Wrap.
            (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0),
            # Top.
            (4, 7, 6, 5),
        ])

    rib = translate ((0, TILE_HEIGHT_PIN / 2, TILE_DEPTH)) (sphere (TILE_DIP_RADIUS))
    dip = translate ((0, TILE_HEIGHT_PIN / 2, TILE_PIN_RADIUS + TILE_SLACK)) (sphere (TILE_DIP_RADIUS))
    pin = translate ((TILE_WIDTH_PIN, TILE_HEIGHT_PIN / 2, TILE_DEPTH - TILE_PIN_RADIUS)) (sphere (TILE_PIN_RADIUS))

    tile_dip = tile_ini - rib - dip
    tile_pin = tile_ini + pin

    tile_dip = translate ((TILE_SLACK, TILE_SLACK, 0)) (tile_dip)
    tile_pin = translate ((TILE_SLACK + TILE_WIDTH_PIN + TILE_WIDTH_GAP, TILE_SLACK, 0)) (tile_pin)

    tile = tile_dip + tile_pin

    tiles = []

    for row in range (rows):
        for column in range (columns):
            if (row + column) % 2 == 0:
                tiles.append (translate ((column * TILE_WIDTH, row * TILE_HEIGHT_ALL, 0)) (tile))

    return union () (*tiles)


# Stand

def do_stand (rows, columns, radius, width, height):

    gap_horizontal = (width - columns * radius * 2) / (columns + 1)
    gap_vertical = (height - rows * radius * 2) / (rows + 1)

    step_horizontal = gap_horizontal + radius * 2
    step_vertical = gap_vertical + radius * 2

    stand = cube ((width, height, STAND_HEIGHT))

    drill = cylinder (radius, STAND_HEIGHT)
    drill = translate ((0, 0, STAND_FLOOR_THICKNESS)) (drill)
    drill += cylinder (radius * STAND_FLOOR_RATIO, STAND_HEIGHT)
    drill = translate ((gap_horizontal + radius, gap_vertical + radius, 0 - OVERLAP)) (drill)

    for row in range (rows):
        for column in range (columns):
            stand -= translate ((step_horizontal * column, step_vertical * row, 0)) (drill)

    pattern_columns_ew = _math.floor (height / TILE_WIDTH / 2) * 2
    pattern_offset_ew = (height - pattern_columns_ew * TILE_WIDTH) / 2

    pattern_columns_ns = _math.floor (width / TILE_WIDTH / 2) * 2
    pattern_offset_ns = (width - pattern_columns_ns * TILE_WIDTH) / 2

    pattern_ew = do_tile_pattern (STAND_PATTERN_ROWS, pattern_columns_ew)
    pattern_ns = do_tile_pattern (STAND_PATTERN_ROWS, pattern_columns_ns)

    pattern_s = translate ((pattern_offset_ns, 0, STAND_PATTERN_OFFSET)) (rotate ((90, 0, 0)) (pattern_ns))
    pattern_e = translate ((width, pattern_offset_ew, STAND_PATTERN_OFFSET)) (rotate ((90, 0, 90)) (pattern_ew))
    pattern_n = translate ((width - pattern_offset_ns, height, STAND_PATTERN_OFFSET)) (rotate ((90, 0, 180)) (pattern_ns))
    pattern_w = translate ((0, height - pattern_offset_ew, STAND_PATTERN_OFFSET)) (rotate ((90, 0, 270)) (pattern_ew))

    stand += pattern_s + pattern_e + pattern_n + pattern_w

    return stand


# Main

DIM_SQUARE = get_rounded_stand_dimension (62)
DIM_LONG_WIDTH = get_rounded_stand_dimension (125)
DIM_LONG_HEIGHT = get_rounded_stand_dimension (22)

scad_render_to_file (do_stand (4, 4, 15/2, DIM_SQUARE, DIM_SQUARE), 'stand-square-aa.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (do_stand (5, 5, 11/2, DIM_SQUARE, DIM_SQUARE), 'stand-square-aaa.scad', file_header = f'$fn = {SEGMENTS};')

scad_render_to_file (do_stand (2, 10, 11/2, DIM_LONG_WIDTH, DIM_LONG_HEIGHT), 'stand-long-aaa.scad', file_header = f'$fn = {SEGMENTS};')
