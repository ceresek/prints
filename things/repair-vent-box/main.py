#!/usr/bin/env python3

from solid import *
from solid.utils import *


OVERLAP = 0.01
SEGMENTS = 33


# Dimensions

CELL_STEP_H = 10.75
CELL_STEP_V = 10
WALL = 1

PIN_SKEW = 0.96
PIN_DEPTH = 10

PIN_SIZE_H = CELL_STEP_H - WALL
PIN_SIZE_V = CELL_STEP_V - WALL

FLOOR = 3

SCREW_BODY = 4.4
SCREW_HEAD = 8.2

PAW_LENGTH = 50


# Components

def pin ():

    xl = PIN_SIZE_H/2
    yl = PIN_SIZE_V/2
    xh = xl * PIN_SKEW
    yh = yl * PIN_SKEW
    z = PIN_DEPTH

    pin = polyhedron (
        points = [
            # Bottom layer.
            (-xl, -yl, 0), (xl, -yl, 0), (xl, yl, 0), (-xl, yl, 0),
            # Top layer.
            (-xh, -yh, z), (xh, -yh, z), (xh, yh, z), (-xh, yh, z),
        ],
        faces = [
            # Bottom.
            (0, 1, 2, 3),
            # Wrap.
            (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0),
            # Top.
            (4, 7, 6, 5),
        ])

    return pin


# Shapes

def shape_t (leg, bar):

    leg_pin = rotate ((0, 0, 90)) (pin ())
    leg_pos = range (0, leg)
    leg_len = CELL_STEP_V + leg * CELL_STEP_H
    leg_list = [ translate ((0, PIN_SIZE_H/2 + PIN_SIZE_V/2 + 2*WALL + CELL_STEP_H * pos, 0)) (leg_pin) for pos in leg_pos ]
    leg_pins = union () (*leg_list)
    leg_floor = translate ((-PIN_SIZE_V/2, -PIN_SIZE_V/2, -FLOOR)) (cube ((PIN_SIZE_V, leg_len, FLOOR + OVERLAP)))

    bar_pin = pin ()
    bar_pos = range (0, bar)
    bar_len = bar * CELL_STEP_H - WALL
    bar_list = [ translate ((PIN_SIZE_H/2 - bar_len/2 + CELL_STEP_H * pos, 0, 0)) (bar_pin) for pos in bar_pos ]
    bar_pins = union () (*bar_list)
    bar_floor = translate ((-bar_len/2, -PIN_SIZE_V/2, -FLOOR)) (cube ((bar_len, PIN_SIZE_V, FLOOR + OVERLAP)))

    return leg_pins + leg_floor + bar_pins + bar_floor


def shape_l (leg, bar):

    leg_pin = rotate ((0, 0, 90)) (pin ())
    leg_pos = range (0, leg)
    leg_len = CELL_STEP_V + leg * CELL_STEP_H
    leg_list = [ translate ((0, PIN_SIZE_H/2 + PIN_SIZE_V/2 + 2*WALL + CELL_STEP_H * pos, 0)) (leg_pin) for pos in leg_pos ]
    leg_pins = union () (*leg_list)
    leg_floor = translate ((-PIN_SIZE_V/2, -PIN_SIZE_V/2, -FLOOR)) (cube ((PIN_SIZE_V, leg_len, FLOOR + OVERLAP)))

    bar_pin = pin ()
    bar_pos = range (0, bar)
    bar_len = bar * CELL_STEP_H - WALL
    bar_list = [ translate ((PIN_SIZE_H/2 - PIN_SIZE_V/2 + CELL_STEP_H * pos, 0, 0)) (bar_pin) for pos in bar_pos ]
    bar_pins = union () (*bar_list)
    bar_floor = translate ((-PIN_SIZE_V/2, -PIN_SIZE_V/2, -FLOOR)) (cube ((bar_len, PIN_SIZE_V, FLOOR + OVERLAP)))

    return leg_pins + leg_floor + bar_pins + bar_floor


def shape_d (bar):

    bar_pin = pin ()
    bar_pos = range (0, bar)
    bar_len = bar * CELL_STEP_H - WALL
    bar_list = [ translate ((PIN_SIZE_H/2 - bar_len/2 + CELL_STEP_H * pos, 0, 0)) (bar_pin) for pos in bar_pos ]
    bar_pins = union () (*bar_list)
    bar_floor = translate ((-bar_len/2, -PIN_SIZE_V/2, 0 - FLOOR - SCREW_HEAD)) (cube ((bar_len, PIN_SIZE_V, FLOOR + SCREW_HEAD + OVERLAP)))

    screw_hole = cylinder (SCREW_BODY/2, PIN_SIZE_V + 2*OVERLAP)
    screw_hole = rotate ((90, 0, 0)) (screw_hole)
    screw_hole = translate ((0, PIN_SIZE_V/2 + OVERLAP, 0 - FLOOR/2 - SCREW_HEAD/2)) (screw_hole)

    return bar_pins + bar_floor - screw_hole


def shape_o ():

    side_one = cylinder (SCREW_HEAD/2 + FLOOR/2, FLOOR)
    side_two = translate ((PAW_LENGTH, 0, 0)) (side_one)

    rise = cylinder (SCREW_HEAD/2 + FLOOR/2, FLOOR + WALL)
    rise = translate ((PAW_LENGTH, 0, 0)) (rise)

    screw_hole = cylinder (SCREW_BODY/2, FLOOR + 2*OVERLAP)
    screw_hole = translate ((0, 0, -OVERLAP)) (screw_hole)

    return hull () (side_one, side_two) + rise - screw_hole


# Main

scad_render_to_file (shape_t (3, 5), 'shape-t.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (shape_l (3, 4), 'shape-l.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (shape_d (5), 'shape-d.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (shape_o (), 'shape-o.scad', file_header = f'$fn = {SEGMENTS};')
