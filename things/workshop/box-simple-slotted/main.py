#!/usr/bin/env python3

import math

from solid import *
from solid.utils import *


SEGMENTS = 33

X = 0
Y = 1
Z = 2
OVERLAP = 0.001

BOX_WIDTH = 140
BOX_DEPTH = 105
BOX_HEIGHT = 50
BOX_WALL_THICKNESS = 3
BOX_FLOOR_THICKNESS = 3

SPACER_WALL_THICKNESS = 1

LID_SLACK = 1
LID_HEIGHT = 10


def hollow_box (width, depth, height, floor, wall):
    box_outer = cube ([width, depth, height])
    box_inner = translate ([wall, wall, floor]) (
        cube ([width - 2*wall, depth - 2*wall, height - floor + OVERLAP]))
    return difference () (box_outer, box_inner)


def spacers (width, depth, height, count, wall):
    spacer = cube ([wall, depth, height])
    distance = (width - count * wall) / (count + 1)
    positions = [ distance + index * (distance + wall) for index in range (count) ]
    spacers = [ right (position) (spacer) for position in positions ]
    return union () (*spacers)


def box_with_spacers (rows, columns):

    box = hollow_box (BOX_WIDTH, BOX_DEPTH, BOX_HEIGHT, BOX_FLOOR_THICKNESS, BOX_WALL_THICKNESS)

    spacers_along_x = right (BOX_WALL_THICKNESS) (spacers (BOX_WIDTH - 2*BOX_WALL_THICKNESS, BOX_DEPTH, BOX_HEIGHT, columns - 1, SPACER_WALL_THICKNESS))
    spacers_along_y = forward (BOX_WALL_THICKNESS) (mirror ([+1,-1,0]) (spacers (BOX_DEPTH - 2*BOX_WALL_THICKNESS, BOX_WIDTH, BOX_HEIGHT, rows - 1, SPACER_WALL_THICKNESS)))

    box += spacers_along_x + spacers_along_y

    logo = linear_extrude (1) (import_dxf ('paw.dxf'))
    logo_side = translate ([1/2, BOX_DEPTH - 30, 20]) (rotate ([90, 0, -90]) (logo))
    logo_front = translate ([30, 1/2, 20]) (rotate ([90, 0, 0]) (logo))

    box -= logo_side + logo_front

    return box


lid = hollow_box (
    BOX_WIDTH + LID_SLACK + 2*BOX_WALL_THICKNESS,
    BOX_DEPTH + LID_SLACK + 2*BOX_WALL_THICKNESS,
    LID_HEIGHT, BOX_FLOOR_THICKNESS, BOX_WALL_THICKNESS)


scad_render_to_file (box_with_spacers (1, 1), 'box-1-1.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (box_with_spacers (1, 2), 'box-1-2.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (box_with_spacers (2, 2), 'box-2-2.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (box_with_spacers (2, 3), 'box-2-3.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (box_with_spacers (3, 3), 'box-3-3.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (box_with_spacers (3, 4), 'box-3-4.scad', file_header = f'$fn = {SEGMENTS};')

scad_render_to_file (lid, 'lid.scad', file_header = f'$fn = {SEGMENTS};')
