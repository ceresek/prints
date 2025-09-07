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
BOX_WALL_THICKNESS = 0.44
BOX_FLOOR_THICKNESS = 0.8

LID_HEIGHT = 10

POCKET_SLACK = 1


def pocket (rows, columns):
    width = (BOX_WIDTH - 2*BOX_WALL_THICKNESS - POCKET_SLACK) / columns
    depth = (BOX_DEPTH - 2*BOX_WALL_THICKNESS - POCKET_SLACK) / rows
    height = BOX_HEIGHT - 2*BOX_FLOOR_THICKNESS
    return cube ((width, depth, height))

box = cube ((BOX_WIDTH, BOX_DEPTH, BOX_HEIGHT - LID_HEIGHT))
lid = cube ((BOX_WIDTH, BOX_DEPTH, LID_HEIGHT))

scad_render_to_file (box, 'box.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (lid, 'lid.scad', file_header = f'$fn = {SEGMENTS};')

scad_render_to_file (pocket (3, 3), 'pocket-3-3.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (pocket (3, 4), 'pocket-3-4.scad', file_header = f'$fn = {SEGMENTS};')
