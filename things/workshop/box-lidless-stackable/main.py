#!/usr/bin/env python3

import math

from solid import *
from solid.utils import *

from components.common import *
from components.hexagon import *


SEGMENTS = 33


# Spool Storage Box Config

SPOOL_HEIGHT = 57.5
SPOOL_DIAMETER = 19.4
SPOOL_RADIUS = SPOOL_DIAMETER / 2

SPOOL_COLUMNS = 2
SPOOL_ROWS = 12

BOX_SLACK_HORIZONTAL_SPOOL = 2
BOX_SLACK_VERTICAL_SPOOL = 1
BOX_WIDTH_INNER_SPOOL = SPOOL_HEIGHT * SPOOL_COLUMNS + BOX_SLACK_HORIZONTAL_SPOOL
BOX_DEPTH_INNER_SPOOL = SPOOL_DIAMETER * SPOOL_ROWS + BOX_SLACK_HORIZONTAL_SPOOL
BOX_HEIGHT_INNER_SPOOL = SPOOL_DIAMETER + BOX_SLACK_VERTICAL_SPOOL
BOX_SIZE_INNER_SPOOL = ( BOX_WIDTH_INNER_SPOOL, BOX_DEPTH_INNER_SPOOL, BOX_HEIGHT_INNER_SPOOL )
BOX_HOLE_RADIUS_SPOOL = SPOOL_RADIUS - 2
BOX_HOLE_SPACING_SPOOL = SPOOL_DIAMETER

# General Box Config

BOX_LOGO_THICKNESS = 0.2
BOX_FLOOR_THICKNESS = 0.8
BOX_WALL_THICKNESS = 0.86
BOX_RIM_HEIGHT = 2
BOX_RIM_SLACK = 0.3
BOX_RIM_ANGLE = math.pi/6


# Hole

def area_hexagon_hole (area, radius, spacing, height):

    width = 2 * radius * math.cos (math.pi/6)
    gap = spacing - width

    count = math.trunc (area [X] / spacing)
    align = (area [X] - count*spacing + gap) / 2
    lift = (area [Y] - 2*radius) / 2

    prototype = rotate (( 0, 0, 30 )) (hexagon (radius, height))
    prototype = translate (( align + width/2, radius + lift, 0 )) (prototype)

    result = [ translate (( spacing * step, 0, 0 )) (prototype) for step in range (count) ]
    result = union () (*result)

    return result


# Box

def box_body (size, floor, wall):

    inner_size = ( size [X], size [Y], size [Z] + OVERLAP)
    outer_size = ( size [X] + 2*wall, size [Y] + 2*wall, size [Z] + floor)

    inner_body = cube (inner_size)
    outer_body = cube (outer_size)
    outer_body = translate (( 0 - wall, 0 - wall, 0 - floor)) (outer_body)
    body = outer_body - inner_body

    return body


def box_rim (area : P2, angle, wall, height, slack):

    inner_bottom_area = area
    inner_top_area = vector_extend (area, 2*slack + 2*wall)
    outer_bottom_area = vector_extend (area, 2*wall)
    outer_top_area = vector_extend (area, 2*slack + 4*wall)

    chamfer_inner_scale = vector_ratio (inner_top_area, inner_bottom_area)
    chamfer_outer_scale = vector_ratio (outer_top_area, outer_bottom_area)
    chamfer_height = (wall + slack) / math.tan (angle)

    chamfer_inner_body = linear_extrude (height = chamfer_height + 2*OVERLAP, scale = chamfer_inner_scale) (square (inner_bottom_area, center = True)) # type: ignore
    chamfer_outer_body = linear_extrude (height = chamfer_height, scale = chamfer_outer_scale) (square (outer_bottom_area, center = True)) # type: ignore
    chamfer_inner_body = translate (area_to_size (vector_scale (inner_bottom_area, 1/2), 0)) (chamfer_inner_body)
    chamfer_outer_body = translate (area_to_size (vector_scale (outer_bottom_area, 1/2), 0)) (chamfer_outer_body)
    chamfer_inner_body = translate (( 0, 0, 0 - OVERLAP )) (chamfer_inner_body)
    chamfer_outer_body = translate (( 0 - wall, 0 - wall, 0 )) (chamfer_outer_body)
    chamfer_body = chamfer_outer_body - chamfer_inner_body

    rim_inner_body = cube (area_to_size (inner_top_area, height + 2*OVERLAP))
    rim_outer_body = cube (area_to_size (outer_top_area, height))
    rim_inner_body = translate (( 0 - slack - wall, 0 - slack - wall, 0 - OVERLAP )) (rim_inner_body)
    rim_outer_body = translate (( 0 - slack - 2*wall, 0 - slack - 2*wall, 0 )) (rim_outer_body)
    rim_body = rim_outer_body - rim_inner_body

    chamfer_body = translate (( 0, 0, 0 - chamfer_height )) (chamfer_body)
    body = chamfer_body + rim_body

    return body


def box_body_with_rim (size, angle, floor, wall, height, slack):

    body = box_body (size, floor, wall)
    rim = box_rim (size_to_area_xy (size), angle, wall, height, slack)
    rim = translate (( 0, 0, size [Z] )) (rim)

    return body + rim


# Specific Boxes

box_spool = box_body_with_rim (BOX_SIZE_INNER_SPOOL, BOX_RIM_ANGLE, BOX_FLOOR_THICKNESS, BOX_WALL_THICKNESS, BOX_RIM_HEIGHT, BOX_RIM_SLACK)
holes_spool_along_x = area_hexagon_hole (size_to_area_xz (BOX_SIZE_INNER_SPOOL), BOX_HOLE_RADIUS_SPOOL, BOX_HOLE_SPACING_SPOOL, BOX_DEPTH_INNER_SPOOL + 2*BOX_WALL_THICKNESS + 2*OVERLAP)
holes_spool_along_x = rotate (( 90, 0, 0 )) (holes_spool_along_x)
holes_spool_along_x = translate (( 0, BOX_DEPTH_INNER_SPOOL + BOX_WALL_THICKNESS + OVERLAP, 0 )) (holes_spool_along_x)
holes_spool_along_y = area_hexagon_hole (size_to_area_yz (BOX_SIZE_INNER_SPOOL), BOX_HOLE_RADIUS_SPOOL, BOX_HOLE_SPACING_SPOOL, BOX_WIDTH_INNER_SPOOL + 2*BOX_WALL_THICKNESS + 2*OVERLAP)
holes_spool_along_y = rotate (( 90, 0, 90 )) (holes_spool_along_y)
holes_spool_along_y = translate (( 0 - BOX_WALL_THICKNESS - OVERLAP, 0, 0 )) (holes_spool_along_y)
logo_spool = linear_extrude (BOX_LOGO_THICKNESS) (import_dxf ('paw.dxf'))
logo_spool = scale (3) (logo_spool) # type: ignore
logo_move = vector_scale (area_to_size (size_to_area_xy (BOX_SIZE_INNER_SPOOL), 0), 1/2)
logo_spool = translate (logo_move) (logo_spool) # type: ignore
box_spool = box_spool - holes_spool_along_x - holes_spool_along_y + logo_spool

scad_render_to_file (box_spool, 'box-spool.scad', file_header = f'$fn = {SEGMENTS};')
