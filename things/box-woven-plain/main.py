#!/usr/bin/env python3

import math as _math

from solid import *
from solid.utils import *

from components.common import *


SEGMENTS = 33


# Weave Config

NOZZLE_RADIUS = 0.4 / 2

STICK_RADIUS = 1.111
STICK_SQUISH = 0.111
STICK_SEGMENTS = 6
STICK_ROTATION = 0
COLUMN_RADIUS = 1.111
COLUMN_SPACING = 23.45

# General Box Config

BOX_FLOOR_THICKNESS = 0.8
BOX_LOGO_THICKNESS = 0.2
BOX_LOGO_SCALE = 3

BOX_DEPTH_ROWS = floor (83 / STICK_RADIUS / 2)
BOX_WIDTH_COLS = floor (150 / COLUMN_SPACING) + 1
BOX_HEIGHT_COLS = floor (240 / COLUMN_SPACING) + 1


# Utilities

def pos_with_angle (pos, radius, angle):
    return (
        pos [X] + radius * _math.cos (_math.radians (angle)),
        pos [Y] + radius * _math.sin (_math.radians (angle)),
        pos [Z])

# Weave

def connector (pos_one, angle_one, pos_two, angle_two):

    real_pos_one = pos_with_angle (pos_one, COLUMN_RADIUS + STICK_RADIUS * STICK_SQUISH, angle_one)
    real_pos_two = pos_with_angle (pos_two, COLUMN_RADIUS + STICK_RADIUS * STICK_SQUISH, angle_two)
    connector_vector = vector_difference (real_pos_two, real_pos_one)
    connector_length = vector_length (connector_vector)
    connector_rotation = point_to_rotation (connector_vector)

    connector = cylinder (STICK_RADIUS, connector_length, segments = STICK_SEGMENTS)
    connector = rotate ((0, 0, STICK_ROTATION)) (connector)
    connector = rotate ((0, 90, 0)) (connector)
    connector = rotate (connector_rotation) (connector)
    connector = translate (real_pos_one) (connector)

    return connector

def filler (angle_one, angle_two):

    outline = circle (STICK_RADIUS, segments = STICK_SEGMENTS)
    outline = rotate ((0, 0, 90)) (outline)
    outline = translate ((COLUMN_RADIUS + STICK_RADIUS * STICK_SQUISH, 0, 0)) (outline)
    filler = rotate_extrude (angle_two - angle_one) (outline)
    filler = rotate ((0, 0, angle_one)) (filler)

    return filler

def wall (num_rows, num_columns):

    column_positions = [(index * COLUMN_SPACING, 0, 0) for index in range (num_columns)]
    column_height = num_rows * STICK_RADIUS * 2
    column_proto = cylinder (COLUMN_RADIUS, column_height)
    columns_list = [translate (position) (column_proto) for position in column_positions]
    columns = union () (*columns_list)

    stick_positions_one = column_positions [:-1]
    stick_positions_two = column_positions [1:]
    stick_shifts_one = [270, 90] * ceil (num_columns / 2)
    stick_shifts_two = [90, 270] * ceil (num_columns / 2)
    sticks_list = [
        connector (pos_one, shift_one, pos_two, shift_two)
        for (pos_one, shift_one, pos_two, shift_two)
        in zip (stick_positions_one, stick_shifts_one, stick_positions_two, stick_shifts_two)
    ]

    # Too lazy to compute the filler angles.
    filler_proto_one = filler (-95, -85)
    filler_proto_two = filler (+85, +95)
    fillers_one_list = [translate (position) (filler_proto_one) for position in column_positions [::2]]
    fillers_two_list = [translate (position) (filler_proto_two) for position in column_positions [1::2]]

    sticks = union () (*sticks_list, *fillers_one_list, *fillers_two_list)

    sticks_mirror = mirror ((0, 1, 0)) (sticks)

    weave_positions = [(0, 0, STICK_RADIUS + index * STICK_RADIUS * 2) for index in range (num_rows)]
    weaves_one_list = [translate (position) (sticks) for position in weave_positions [::2]]
    weaves_two_list = [translate (position) (sticks_mirror) for position in weave_positions [1::2]]
    weaves = union () (*weaves_one_list, *weaves_two_list)

    return columns + weaves

def corner (num_rows, angle):

    angle_one = angle - 45
    angle_two = angle + 45
    angle_support = (angle + 180) % 360

    corner_positions = [(0, 0, STICK_RADIUS + index * STICK_RADIUS * 2) for index in range (num_rows)]
    corner_proto_one = filler (angle_one, angle_two)
    corner_proto_two = filler (0, 360)
    corners_one_list = [translate (position) (corner_proto_one) for position in corner_positions [::2]]
    corners_two_list = [translate (position) (corner_proto_two) for position in corner_positions [1::2]]
    corners = union () (*corners_one_list, *corners_two_list)

    support_height = num_rows * STICK_RADIUS * 2
    support_one = cylinder (COLUMN_RADIUS, support_height)
    support_two = translate (((COLUMN_RADIUS + STICK_RADIUS * STICK_SQUISH + NOZZLE_RADIUS) * sqrt (2) - COLUMN_RADIUS, 0, 0)) (support_one)
    support_two = rotate ((0, 0, angle_support)) (support_two)
    support = hull () (support_one, support_two)

    return corners + support

# Box

def box ():

    # Rounded corners so no cube here.
    box_width_centers = (BOX_WIDTH_COLS - 1) * COLUMN_SPACING
    box_height_centers = (BOX_HEIGHT_COLS - 1) * COLUMN_SPACING
    floor_column_proto = cylinder (COLUMN_RADIUS, BOX_FLOOR_THICKNESS)
    floor = union () (
        translate ((0, 0, 0)) (floor_column_proto),
        translate ((box_width_centers, 0, 0)) (floor_column_proto),
        translate ((0, box_height_centers, 0)) (floor_column_proto),
        translate ((box_width_centers, box_height_centers, 0)) (floor_column_proto))
    floor = hull () (floor)

    logo = linear_extrude (BOX_LOGO_THICKNESS) (import_dxf ('paw.dxf'))
    logo = scale (BOX_LOGO_SCALE) (logo) # type: ignore
    logo = translate ((box_width_centers / 2, box_height_centers / 2, BOX_FLOOR_THICKNESS)) (logo)

    # Walls.
    wall_x_proto = wall (BOX_DEPTH_ROWS, BOX_WIDTH_COLS)
    wall_y_proto = wall (BOX_DEPTH_ROWS, BOX_HEIGHT_COLS)

    wall_one = translate ((0, 0, BOX_FLOOR_THICKNESS)) (rotate ((0, 0, 0)) (wall_x_proto))
    wall_two = translate ((box_width_centers, 0, BOX_FLOOR_THICKNESS)) (rotate ((0, 0, 90)) (wall_y_proto))
    wall_tre = translate ((box_width_centers, box_height_centers, BOX_FLOOR_THICKNESS)) (rotate ((0, 0, 180)) (wall_x_proto))
    wall_for = translate ((0, box_height_centers, BOX_FLOOR_THICKNESS)) (rotate ((0, 0, 270)) (wall_y_proto))

    # Corners
    corners_one = translate ((0, 0, BOX_FLOOR_THICKNESS)) (corner (BOX_DEPTH_ROWS, 225))
    corners_two = translate ((box_width_centers, 0, BOX_FLOOR_THICKNESS)) (corner (BOX_DEPTH_ROWS, 315))
    corners_tre = translate ((box_width_centers, box_height_centers, BOX_FLOOR_THICKNESS)) (corner (BOX_DEPTH_ROWS, 45))
    corners_for = translate ((0, box_height_centers, BOX_FLOOR_THICKNESS)) (corner (BOX_DEPTH_ROWS, 135))

    return floor + logo + wall_one + wall_two + wall_tre + wall_for + corners_one + corners_two + corners_tre + corners_for


# Main

scad_render_to_file (box (), 'box.scad', file_header = f'$fn = {SEGMENTS};')
