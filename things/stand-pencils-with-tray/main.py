#!/usr/bin/env python3

import math

from solid import *
from solid.utils import *


SEGMENTS = 33

X = 0
Y = 1
Z = 2
OVERLAP = 0.001

SPIRAL_SLOPE = 45
SPIRAL_WINGS = 24

CUP_FLOOR_THICKNESS = 3
CUP_WALL_THICKNESS = 3
CUP_EDGE_RADIUS = 10

CUP_BASE = 60
CUP_HEIGHT = 70

BOX_HEIGHT = 20
BOX_SPACING = 5
BOX_SLOT = 20

BOX_EDGE_RADIUS = 10
BOX_WALL_THICKNESS = 3
BOX_FLOOR_THICKNESS = 5

MESH_SPACING = 10
MESH_WALL_THICKNESS = BOX_WALL_THICKNESS/2

EMBOSSING_DEPTH = 2
EMBOSSING_SLACK = 1


def mesh (width, length, spacing, thickness, height):
    width_in_cells = round (width / spacing)
    length_in_cells = round (length / spacing)
    zig = back (thickness/2) (cube ([width_in_cells * spacing, thickness, height]))
    zag = left (thickness/2) (cube ([thickness, length_in_cells * spacing, height]))
    zigs = [ forward (step * spacing) (zig) for step in range (width_in_cells + 1) ]
    zags = [ right (step * spacing) (zag) for step in range (length_in_cells + 1) ]
    return left (width_in_cells * spacing / 2) (back (length_in_cells * spacing / 2) (union () (*zigs, *zags)))


def spiral (radius, width, height, threads, direction, offset):
    # Compute twist to have given slope.
    circumference = 2 * math.pi * radius
    revolutions = height / circumference / math.tan (SPIRAL_SLOPE * math.pi / 180)
    # Generate spiral.
    step = 360 / threads
    beams = [ rotate ([0, 0, step * thread + offset]) (square ([radius * 2, width], center = True)) for thread in range (threads) ]
    footprint = union () (*beams)
    result = linear_extrude (height, convexity = 8, twist = math.copysign (360 * revolutions, direction), slices = height * 3) (footprint)
    # Whatever.
    return result    


def cube_rounded_edges (size, radius):
    edge = cylinder (r = radius, h = size [Z])
    lf =  left (size [X]/2 - radius) (forward (size [Y]/2 - radius) (edge))
    lb =  left (size [X]/2 - radius) (   back (size [Y]/2 - radius) (edge))
    rf = right (size [X]/2 - radius) (forward (size [Y]/2 - radius) (edge))
    rb = right (size [X]/2 - radius) (   back (size [Y]/2 - radius) (edge))
    return hull () (lf, lb, rf, rb)


def cup ():

    base = cube_rounded_edges ([CUP_BASE, CUP_BASE, CUP_FLOOR_THICKNESS], CUP_EDGE_RADIUS)

    tube_outer = cube_rounded_edges ([CUP_BASE, CUP_BASE, CUP_HEIGHT], CUP_EDGE_RADIUS)
    tube_inner = down (OVERLAP) (cube_rounded_edges ([CUP_BASE - 2*CUP_WALL_THICKNESS, CUP_BASE - 2*CUP_WALL_THICKNESS, CUP_HEIGHT + 2*OVERLAP], CUP_EDGE_RADIUS-CUP_WALL_THICKNESS))
    tube = difference () (tube_outer, tube_inner)

    lid_outer = cube_rounded_edges ([CUP_BASE, CUP_BASE, CUP_FLOOR_THICKNESS], CUP_EDGE_RADIUS)
    lid_inner = down (OVERLAP) (cube_rounded_edges ([CUP_BASE - 2*CUP_WALL_THICKNESS, CUP_BASE - 2*CUP_WALL_THICKNESS, CUP_FLOOR_THICKNESS + 2*OVERLAP], CUP_EDGE_RADIUS-CUP_WALL_THICKNESS))
    lid = up (CUP_HEIGHT - CUP_FLOOR_THICKNESS) (difference () (lid_outer, lid_inner))

    # Compute offsets so that the spirals are
    # at maximum phase distance just below the lid
    # and also support the corners of the lid symmetrically.

    circumference = 2 * math.pi * CUP_BASE
    revolutions = (CUP_HEIGHT - CUP_FLOOR_THICKNESS) / circumference / math.tan (SPIRAL_SLOPE * math.pi / 180)
    offset = 45 - revolutions * 360 + 360 / SPIRAL_WINGS / 4

    pattern_l = spiral (CUP_BASE, CUP_WALL_THICKNESS/2, CUP_HEIGHT, SPIRAL_WINGS, +1, offset)
    pattern_r = spiral (CUP_BASE, CUP_WALL_THICKNESS/2, CUP_HEIGHT, SPIRAL_WINGS, -1, -offset)
    pattern = union () (pattern_l, pattern_r)
    tube *= pattern

    logo = translate ([0, CUP_BASE/2 + 1/2, CUP_HEIGHT*3/5]) (rotate ([90, 0, 0]) (scale (3) (linear_extrude (1/3) (import_dxf ('logo.dxf')))))

    return union () (base, tube, logo, lid)


def box (rows, cols):

    inner_width = cols * (CUP_BASE + BOX_SPACING) + BOX_SPACING + BOX_WALL_THICKNESS + BOX_SLOT
    inner_height = rows * (CUP_BASE + BOX_SPACING) + BOX_SPACING
    total_width = inner_width + 2 * BOX_WALL_THICKNESS
    total_height = inner_height + 2 * BOX_WALL_THICKNESS
    pattern_size = max (total_width, total_height) * 2

    base = cube_rounded_edges ([total_width, total_height, BOX_FLOOR_THICKNESS], BOX_EDGE_RADIUS)

    pattern = rotate ([0, 0, 45]) (mesh (pattern_size, pattern_size, MESH_SPACING, MESH_WALL_THICKNESS, BOX_FLOOR_THICKNESS))
    base *= pattern

    wall_outer = cube_rounded_edges ([total_width, total_height, BOX_HEIGHT], BOX_EDGE_RADIUS)
    wall_inner = down (OVERLAP) (cube_rounded_edges ([total_width - 2*BOX_WALL_THICKNESS, total_height - 2*BOX_WALL_THICKNESS, BOX_HEIGHT + 2*OVERLAP], BOX_EDGE_RADIUS-BOX_WALL_THICKNESS))
    wall = difference () (wall_outer, wall_inner)

    spacer = up (BOX_HEIGHT/2) (right (total_width/2 - BOX_SLOT - BOX_WALL_THICKNESS*3/2) (cube ([BOX_WALL_THICKNESS, total_height, BOX_HEIGHT], center = True)))

    compact = right (total_width/2) (forward (total_height/2) (union () (base, wall, spacer)))

    dip = cube_rounded_edges ([CUP_BASE + EMBOSSING_SLACK, CUP_BASE + EMBOSSING_SLACK, EMBOSSING_DEPTH], CUP_EDGE_RADIUS + EMBOSSING_SLACK/2)
    for row in range (rows):
        for col in range (cols):
            compact -= up (BOX_FLOOR_THICKNESS - EMBOSSING_DEPTH + OVERLAP) (
                right (BOX_WALL_THICKNESS + BOX_SPACING + CUP_BASE/2 + (CUP_BASE + BOX_SPACING) * col) (
                    forward (BOX_WALL_THICKNESS + BOX_SPACING + CUP_BASE/2 + (CUP_BASE + BOX_SPACING) * row) (
                        dip)))
    
    return compact


scad_render_to_file (cup (), 'cup.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (box (1, 2), 'box-1-2.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (box (1, 3), 'box-1-3.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (box (2, 1), 'box-2-1.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (box (2, 2), 'box-2-2.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (box (2, 3), 'box-2-3.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (box (3, 3), 'box-3-3.scad', file_header = f'$fn = {SEGMENTS};')
