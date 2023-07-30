#!/usr/bin/env python3

import math

from solid import *
from solid.utils import *


SEGMENTS = 111

X = 0
Y = 1
Z = 2

OVERLAP = 0.001

# General dimensions.

GENERAL_NUT_RADIUS = 4.1
GENERAL_NUT_HEIGHT = 3.3
GENERAL_NUT_DEPTH = 10

# Corner piece dimensions.

CORNER_SINK = 6
CORNER_FREE = 188
CORNER_SIDE = CORNER_FREE + CORNER_SINK

CORNER_THICKNESS = 5

# Intensity regulator dimensions.

SWITCH_HOLE_EDGE = 5
SWITCH_HOLE_WIDTH = 50
SWITCH_HOLE_HEIGHT = 77

SWITCH_DRILL_RADIUS = 2.1
SWITCH_DRILL_DISTANCE = 60
SWITCH_DRILL_THICKNESS = 2.8

SWITCH_COVER_HEIGHT = 14
SWITCH_COVER_THICKNESS = 2

SWITCH_VENTILATION_WIDTH = 3
SWITCH_VENTILATION_COUNT = 6

KNOB_HEIGHT = 14
KNOB_THICKNESS = 2
KNOB_CAP_RADIUS = 16
KNOB_AXIS_RADIUS = 3
KNOB_AXIS_LENGTH = 9

KNOB_PATTERN_CORNERS = 6
KNOB_PATTERN_REPLICAS = 16

# Power supply dimensions.

SUPPLY_BOX_WIDTH = 40
SUPPLY_BOX_HEIGHT = 30
SUPPLY_BOX_LENGTH = 150

SWITCH_SUPPLY_GAP = 5

# Alu profile dimensions.

PROFILE_BODY_THICKNESS = 1.7

PROFILE_SIZE = 16
PROFILE_CATCH = 2.5
PROFILE_THICKNESS = 1
PROFILE_HOLE_OFFSET = 6.6
PROFILE_NOTCH_BUMP = 0.6
PROFILE_NOTCH_SIZE = 6
PROFILE_NOTCH_DEPTH = 16
PROFILE_SHIELD_SIZE = 13
PROFILE_SHIELD_NOTCH = 2
PROFILE_SHIELD_DEPTH = 6
PROFILE_SHIELD_THICKNESS = 1

PROFILE_WALL_DISTANCE = 40

PROFILE_WIRE_SIZE = 6.789

PROFILE_HOLDER_LENGTH = 15
PROFILE_HOLDER_HOLE_INNER = 3.1
PROFILE_HOLDER_HOLE_OUTER = 6.5
PROFILE_HOLDER_RIM_THICKNESS = 1.5
PROFILE_HOLDER_RIM = 12
PROFILE_HOLDER_NUT_DIAMETER = 6.5
PROFILE_HOLDER_NUT_THICKNESS = 2.4

# Cable tunnel dimensions.

TUNNEL_WIDTH = 11.4
TUNNEL_HEIGHT = 10.2
TUNNEL_CAP_LENGTH = 22
TUNNEL_CAP_THICKNESS = 0.86

# Construction dimensions.

HOLDER_THICKNESS = 5
HOLDER_BAR_HEIGHT = 28

HOLDER_DRILL_RIM = 3
HOLDER_DRILL_WIDTH = 10
HOLDER_DRILL_RADIUS = 2.1

HOLDER_SUPPORT_WIDTH = 16
HOLDER_SUPPORT_DEPTH = 2*HOLDER_THICKNESS + SUPPLY_BOX_WIDTH
HOLDER_SUPPORT_HEIGHT = SWITCH_COVER_HEIGHT + SWITCH_SUPPLY_GAP


# Helpers.

def cylinder_along_x (length, thickness):
    body = rotate ((0, 90, 0)) (cylinder (h = length, r = thickness/2))
    return body


def cylinder_along_y (length, thickness):
    body = rotate ((-90, 0, 0)) (cylinder (h = length, r = thickness/2))
    return body


def cylinder_along_z (length, thickness):
    body = cylinder (h = length, r = thickness/2)
    return body


# Intensity regulator related components.

def knob ():

    # Outer shell as a union of segmented cylinders.

    cap_base = cylinder (KNOB_CAP_RADIUS, KNOB_HEIGHT, segments = KNOB_PATTERN_CORNERS)
    cap_replicas = [ rotate ((0, 0, 360 / KNOB_PATTERN_CORNERS * step / KNOB_PATTERN_REPLICAS)) (cap_base) for step in range (KNOB_PATTERN_REPLICAS) ]
    cap_body = union () (*cap_replicas)

    cap_drill = cylinder (KNOB_CAP_RADIUS - KNOB_THICKNESS, KNOB_HEIGHT)
    cap_drill = translate ((0, 0, KNOB_THICKNESS)) (cap_drill)

    # Inner axis holder from smooth cylinders.

    axis_body = cylinder (KNOB_AXIS_RADIUS + KNOB_THICKNESS, KNOB_HEIGHT)

    axis_drill = cylinder (KNOB_AXIS_RADIUS, KNOB_HEIGHT)
    axis_drill = translate ((0, 0, KNOB_HEIGHT - KNOB_AXIS_LENGTH)) (axis_drill)

    knob = cap_body - cap_drill + axis_body - axis_drill

    return knob


def switch ():

    # Basic cover box.

    cover_base = cube ((SWITCH_HOLE_WIDTH + 2*SWITCH_COVER_THICKNESS, SWITCH_HOLE_HEIGHT + 2*SWITCH_COVER_THICKNESS, SWITCH_COVER_HEIGHT + SWITCH_COVER_THICKNESS), center = True)
    cover_base = translate ((0, 0, (SWITCH_COVER_HEIGHT + SWITCH_COVER_THICKNESS)/2)) (cover_base)

    cover_hole = cube ((SWITCH_HOLE_WIDTH, SWITCH_HOLE_HEIGHT, SWITCH_COVER_HEIGHT + OVERLAP), center = True)
    cover_hole = translate ((0, 0, SWITCH_COVER_THICKNESS + (SWITCH_COVER_HEIGHT + OVERLAP)/2)) (cover_hole)

    cover_base -= cover_hole

    # Equidistant ventilation slots.

    ventilation_step = SWITCH_HOLE_HEIGHT / (SWITCH_VENTILATION_COUNT + 1)

    ventilation_base = cube ((SWITCH_HOLE_WIDTH + 2*SWITCH_COVER_THICKNESS + 2*OVERLAP, SWITCH_VENTILATION_WIDTH, SWITCH_COVER_HEIGHT + OVERLAP), center = True)
    ventilation_base = translate ((0, 0 - SWITCH_HOLE_HEIGHT/2 + ventilation_step, SWITCH_COVER_THICKNESS + SWITCH_COVER_HEIGHT/2 + OVERLAP/2)) (ventilation_base)
    ventilation_replicas = [ translate ((0, index * ventilation_step, 0)) (ventilation_base) for index in range (SWITCH_VENTILATION_COUNT) ]
    ventilation_body = union () (*ventilation_replicas)

    cover_base -= ventilation_body

    # Screw attachment blocks with nuts.

    screw_base = cylinder (SWITCH_DRILL_RADIUS + SWITCH_DRILL_THICKNESS, SWITCH_COVER_HEIGHT + SWITCH_COVER_THICKNESS)

    screw_hole = cylinder (SWITCH_DRILL_RADIUS, SWITCH_COVER_HEIGHT + SWITCH_COVER_THICKNESS + 2*OVERLAP)
    screw_hole = translate ((0, 0, 0 - OVERLAP)) (screw_hole)

    screw_base -= hole () (screw_hole)

    screw_nut = cylinder (GENERAL_NUT_RADIUS, GENERAL_NUT_HEIGHT, segments = 6)
    screw_nut = translate ((0, 0, SWITCH_COVER_HEIGHT + SWITCH_COVER_THICKNESS - GENERAL_NUT_DEPTH)) (screw_nut)

    screw_base -= hole () (screw_nut)

    screw_one = translate ((0 - SWITCH_DRILL_DISTANCE/2, 0, 0)) (screw_base)
    screw_two = translate ((0 + SWITCH_DRILL_DISTANCE/2, 0, 0)) (screw_base)

    cover_base += screw_one + screw_two

    return cover_base


# Construction related components.

def construction_cover ():

    triangular_base = polyhedron (
        [
            (0, 0, 0), (0, 0 - CORNER_SIDE, 0), (0 - CORNER_SIDE, 0, 0),
            (0, 0, CORNER_THICKNESS), (0, 0 - CORNER_SIDE, CORNER_THICKNESS), (0 - CORNER_SIDE, 0, CORNER_THICKNESS)
        ],
        [
            (0, 2, 1),
            (1, 2, 5, 4),
            (0, 3, 5, 2),
            (0, 1, 4, 3),
            (3, 4, 5)
        ])

    # Intensity regulator hole with screw holes.

    switch_hole = cube ((SWITCH_HOLE_WIDTH, SWITCH_HOLE_HEIGHT, CORNER_THICKNESS + 2*OVERLAP))
    switch_hole = translate ((0 - SWITCH_HOLE_WIDTH/2, 0 - SWITCH_HOLE_HEIGHT/2, 0 - OVERLAP)) (switch_hole)

    drill_hole = cylinder (SWITCH_DRILL_RADIUS, CORNER_THICKNESS + 2*OVERLAP)
    drill_hole = translate ((0, 0, 0 - OVERLAP)) (drill_hole)
    drill_hole_one = translate ((0 - SWITCH_DRILL_DISTANCE/2, 0, 0)) (drill_hole)
    drill_hole_two = translate ((0 + SWITCH_DRILL_DISTANCE/2, 0, 0)) (drill_hole)

    switch_hole += drill_hole_one + drill_hole_two

    switch_hole = rotate ((0, 0, 0 - 45)) (switch_hole)
    switch_hole_shift = CORNER_SIDE / 2 - SWITCH_HOLE_HEIGHT / 2 / math.sqrt (2) - SWITCH_HOLE_EDGE / math.sqrt (2)
    switch_hole = translate ((0 - switch_hole_shift, 0 - switch_hole_shift, 0)) (switch_hole)

    triangular_base -= switch_hole

    # Construction holder screw holes.

    support_hole = cylinder (HOLDER_DRILL_RADIUS, HOLDER_SUPPORT_HEIGHT + 2*OVERLAP)
    support_hole = translate ((0, 0, 0 - OVERLAP)) (support_hole)
    support_hole_shift = (SUPPLY_BOX_LENGTH - HOLDER_SUPPORT_WIDTH) / 2
    support_hole_one = translate ((0 - support_hole_shift, 0, 0)) (support_hole)
    support_hole_two = translate ((0 + support_hole_shift, 0, 0)) (support_hole)

    support_hole = support_hole_one + support_hole_two

    support_hole = rotate ((0, 0, 0 - 45)) (support_hole)
    support_hole_shift = CORNER_SIDE / 2 - (HOLDER_THICKNESS + SUPPLY_BOX_WIDTH / 2) / math.sqrt (2)
    support_hole = translate ((0 - support_hole_shift, 0 - support_hole_shift, 0)) (support_hole)

    triangular_base -= support_hole

    # Add profile connectors.

    # Shift just estimated to look good.
    connector_left = profile_connector ()
    connector_left = rotate ((0, 0, 0 - 90)) (connector_left)
    connector_left = translate ((0 - SUPPLY_BOX_LENGTH, 0 - PROFILE_WALL_DISTANCE - CORNER_SINK + PROFILE_SIZE/2, CORNER_THICKNESS)) (connector_left)

    # Shift just estimated to look good.
    connector_right = profile_connector ()
    connector_right = mirror ((1, 0, 0)) (connector_right)
    connector_right = translate ((0 - PROFILE_WALL_DISTANCE - CORNER_SINK + PROFILE_SIZE/2, 0 - SUPPLY_BOX_LENGTH, CORNER_THICKNESS)) (connector_right)

    return triangular_base + connector_left + connector_right


def construction_holder ():

    support_beam_shift = HOLDER_THICKNESS * math.tan (math.pi/8)

    support_base = cube ((HOLDER_SUPPORT_WIDTH, HOLDER_SUPPORT_DEPTH, HOLDER_SUPPORT_HEIGHT))

    support_catch = cube ((HOLDER_THICKNESS, HOLDER_THICKNESS, HOLDER_SUPPORT_HEIGHT + HOLDER_THICKNESS))
    support_catch_inner = translate ((HOLDER_SUPPORT_WIDTH, HOLDER_THICKNESS, 0)) (support_catch)
    support_catch_outer = translate ((HOLDER_SUPPORT_WIDTH, SUPPLY_BOX_WIDTH, 0)) (support_catch)

    support_base += support_catch_inner + support_catch_outer

    support_edge_inner = cube ((HOLDER_SUPPORT_WIDTH, HOLDER_THICKNESS, HOLDER_SUPPORT_HEIGHT + SUPPLY_BOX_HEIGHT + SUPPLY_BOX_WIDTH + HOLDER_BAR_HEIGHT))

    support_base += support_edge_inner

    support_edge_outer = cube ((HOLDER_SUPPORT_WIDTH, HOLDER_THICKNESS, HOLDER_SUPPORT_HEIGHT + SUPPLY_BOX_HEIGHT + support_beam_shift))
    support_edge_outer = translate ((0, SUPPLY_BOX_WIDTH + HOLDER_THICKNESS, 0)) (support_edge_outer)

    support_base += support_edge_outer

    # Angled support for more rigid construction.

    support_beam = cube ((HOLDER_SUPPORT_WIDTH, HOLDER_THICKNESS, SUPPLY_BOX_WIDTH * math.sqrt (2) + support_beam_shift + HOLDER_THICKNESS))
    support_beam = translate ((0, 0, 0 - support_beam_shift)) (support_beam)
    support_beam = rotate ((45, 0, 0)) (support_beam)
    support_beam = translate ((0, SUPPLY_BOX_WIDTH + HOLDER_THICKNESS, HOLDER_SUPPORT_HEIGHT + SUPPLY_BOX_HEIGHT)) (support_beam)

    support_base += support_beam

    # Construction cover screw holes with nuts.

    support_nut = cylinder (GENERAL_NUT_RADIUS, GENERAL_NUT_HEIGHT, segments = 6)
    support_nut = translate ((0, 0, GENERAL_NUT_DEPTH)) (support_nut)
    support_drill = cylinder (HOLDER_DRILL_RADIUS, HOLDER_SUPPORT_HEIGHT + 2*OVERLAP)
    support_drill_nut = support_drill + support_nut
    support_drill_nut = translate ((HOLDER_SUPPORT_WIDTH/2, HOLDER_SUPPORT_DEPTH/2, 0 - OVERLAP)) (support_drill_nut)

    support_base -= support_drill_nut

    # Top wall hole.

    holder_rim_base = cylinder (HOLDER_DRILL_RADIUS + HOLDER_DRILL_RIM, HOLDER_THICKNESS)
    holder_rim_one = translate ((0 - HOLDER_DRILL_WIDTH/2, 0, 0)) (holder_rim_base)
    holder_rim_two = translate ((0 + HOLDER_DRILL_WIDTH/2, 0, 0)) (holder_rim_base)
    holder_rim = hull () (holder_rim_one, holder_rim_two)
    holder_rim = rotate ((0 - 90, 0, 0)) (holder_rim)
    holder_rim = translate ((HOLDER_SUPPORT_WIDTH/2, 0 - OVERLAP, HOLDER_SUPPORT_HEIGHT + SUPPLY_BOX_HEIGHT + SUPPLY_BOX_WIDTH + HOLDER_BAR_HEIGHT/2)) (holder_rim)

    support_base += holder_rim

    holder_drill_base = cylinder (HOLDER_DRILL_RADIUS, HOLDER_THICKNESS + 2*OVERLAP)
    holder_drill_one = translate ((0 - HOLDER_DRILL_WIDTH/2, 0, 0)) (holder_drill_base)
    holder_drill_two = translate ((0 + HOLDER_DRILL_WIDTH/2, 0, 0)) (holder_drill_base)
    holder_drill = hull () (holder_drill_one, holder_drill_two)
    holder_drill = rotate ((0 - 90, 0, 0)) (holder_drill)
    holder_drill = translate ((HOLDER_SUPPORT_WIDTH/2, 0 - OVERLAP, HOLDER_SUPPORT_HEIGHT + SUPPLY_BOX_HEIGHT + SUPPLY_BOX_WIDTH + HOLDER_BAR_HEIGHT/2)) (holder_drill)

    support_base -= holder_drill

    # Symmetrical construction with connecting arch.

    support_base_one = translate ((SUPPLY_BOX_LENGTH/2 - HOLDER_SUPPORT_WIDTH, 0, 0)) (support_base)
    support_base_two = mirror ((1, 0, 0)) (support_base_one)

    support_bar_shift = SUPPLY_BOX_LENGTH/2 - HOLDER_SUPPORT_WIDTH
    support_cut_shift = support_bar_shift * math.sqrt (2)

    support_bar = cube ((SUPPLY_BOX_LENGTH - 2*HOLDER_SUPPORT_WIDTH, HOLDER_THICKNESS, support_bar_shift + HOLDER_BAR_HEIGHT))
    support_bar = translate ((0 - SUPPLY_BOX_LENGTH/2 + HOLDER_SUPPORT_WIDTH, 0, 0)) (support_bar)

    support_cut = cube ((support_cut_shift, HOLDER_THICKNESS + 2*OVERLAP, support_cut_shift))
    support_cut = translate ((0 - support_cut_shift/2, 0 - OVERLAP, 0 - support_cut_shift/2)) (support_cut)
    support_cut = rotate ((0, 45, 0)) (support_cut)

    support_bar -= support_cut

    support_bar = translate ((0, 0, HOLDER_SUPPORT_HEIGHT + SUPPLY_BOX_HEIGHT + SUPPLY_BOX_WIDTH - support_bar_shift)) (support_bar)

    return support_base_one + support_base_two + support_bar


# Wiring related components.

def profile_lock ():

    lock_arc = intersection () (
        cylinder (h = PROFILE_BODY_THICKNESS, r = PROFILE_SIZE),
        cube ((PROFILE_SIZE, PROFILE_SIZE, PROFILE_BODY_THICKNESS)))
    lock_pin = translate ((PROFILE_THICKNESS, PROFILE_THICKNESS, 0)) (intersection () (
        cube ((PROFILE_NOTCH_SIZE, PROFILE_NOTCH_SIZE, PROFILE_NOTCH_DEPTH)),
        rotate ((0, 0, 45))(cube ((PROFILE_NOTCH_SIZE * math.sqrt (2), PROFILE_NOTCH_SIZE * math.sqrt (2), PROFILE_NOTCH_DEPTH * 2), center = True))))
    lock_bum = translate ((PROFILE_THICKNESS + PROFILE_NOTCH_SIZE/2, PROFILE_THICKNESS + PROFILE_NOTCH_SIZE/2, PROFILE_NOTCH_DEPTH/2)) (
        cylinder_along_z (PROFILE_NOTCH_DEPTH/3, PROFILE_NOTCH_BUMP*2))
    lock_rim = intersection () (
        difference () (
            cylinder (h = PROFILE_SHIELD_DEPTH, r = PROFILE_SHIELD_SIZE + PROFILE_SHIELD_THICKNESS),
            cylinder (h = PROFILE_SHIELD_DEPTH + OVERLAP, r = PROFILE_SHIELD_SIZE)),
        translate ((PROFILE_SHIELD_NOTCH, PROFILE_SHIELD_NOTCH, 0)) (
            cube ((PROFILE_SIZE, PROFILE_SIZE, PROFILE_SHIELD_DEPTH))))

    lock = lock_arc + lock_pin + lock_bum + lock_rim

    return lock


def profile_connector ():

    # Construct wire cap.

    lock = profile_lock ()
    lock = rotate ((90, 0, 0)) (lock)
    lock = translate ((0, PROFILE_BODY_THICKNESS, 0)) (lock)

    cap_lead_length = PROFILE_WALL_DISTANCE - PROFILE_SIZE/2
    cap_lead = cube ((cap_lead_length, PROFILE_WIRE_SIZE + 2*PROFILE_BODY_THICKNESS, PROFILE_SIZE))
    cap_lead = translate ((0 - cap_lead_length, 0, 0)) (cap_lead)

    cap_arc = intersection () (
        cylinder_along_y (PROFILE_WIRE_SIZE + 2*PROFILE_BODY_THICKNESS, 2*PROFILE_SIZE),
        cube ((PROFILE_SIZE, PROFILE_SIZE, PROFILE_SIZE)))

    body = lock + cap_lead + cap_arc

    # Drill wire hole.

    bore_helper_shared_x = PROFILE_HOLE_OFFSET
    bore_helper_shared_y = PROFILE_BODY_THICKNESS + PROFILE_WIRE_SIZE/2
    bore_helper_shared_z = PROFILE_HOLE_OFFSET
    bore_helper_lead_x = 0 - cap_lead_length + PROFILE_BODY_THICKNESS + PROFILE_WIRE_SIZE/2

    # Made long to pierce cover later.
    bore_in_out = cylinder_along_z (bore_helper_shared_z + CORNER_THICKNESS + OVERLAP, PROFILE_WIRE_SIZE)
    bore_in_out = translate ((bore_helper_lead_x, bore_helper_shared_y, 0 - CORNER_THICKNESS - OVERLAP)) (bore_in_out)

    bore_in_lead = cylinder_along_x (bore_helper_shared_x - bore_helper_lead_x, PROFILE_WIRE_SIZE)
    bore_in_lead = translate ((bore_helper_lead_x, bore_helper_shared_y, bore_helper_shared_z)) (bore_in_lead)

    bore_in_arc = cylinder_along_y (bore_helper_shared_y + OVERLAP, PROFILE_WIRE_SIZE)
    bore_in_arc = translate ((bore_helper_shared_x, 0 - OVERLAP, bore_helper_shared_z)) (bore_in_arc)

    ball_at_out_lead = sphere (PROFILE_WIRE_SIZE/2)
    ball_at_out_lead = translate ((bore_helper_lead_x, bore_helper_shared_y, bore_helper_shared_z)) (ball_at_out_lead)

    ball_at_lead_arc = sphere (PROFILE_WIRE_SIZE/2)
    ball_at_lead_arc = translate ((bore_helper_shared_x, bore_helper_shared_y, bore_helper_shared_z)) (ball_at_lead_arc)

    body -= hole () (bore_in_out + ball_at_out_lead + bore_in_lead + ball_at_lead_arc + bore_in_arc)

    return body


def profile_holder ():

    holder_body = cylinder (PROFILE_HOLDER_HOLE_OUTER/2, PROFILE_HOLDER_LENGTH)
    holder_hole = cylinder (PROFILE_HOLDER_HOLE_INNER/2, PROFILE_HOLDER_LENGTH + PROFILE_HOLDER_RIM_THICKNESS + PROFILE_HOLDER_NUT_THICKNESS + 2*OVERLAP)
    holder_hole = translate ((0, 0, 0 - OVERLAP)) (holder_hole)
    holder_nut = cylinder (PROFILE_HOLDER_NUT_DIAMETER/2, PROFILE_HOLDER_NUT_THICKNESS + OVERLAP, segments = 6)
    holder_nut = translate ((0, 0, PROFILE_HOLDER_LENGTH + PROFILE_HOLDER_RIM_THICKNESS)) (holder_nut)
    holder_rim = cylinder (PROFILE_HOLDER_RIM/2, PROFILE_HOLDER_RIM_THICKNESS + PROFILE_HOLDER_NUT_THICKNESS)
    holder_rim = translate ((0, 0, PROFILE_HOLDER_LENGTH)) (holder_rim)

    return holder_rim + holder_body - holder_hole - holder_nut


def tunnel_cap ():

    cap_body = cube ((TUNNEL_WIDTH + 2*TUNNEL_CAP_THICKNESS, TUNNEL_HEIGHT + 2*TUNNEL_CAP_THICKNESS, TUNNEL_CAP_LENGTH + TUNNEL_CAP_THICKNESS), center = True)
    cap_body = translate ((0, 0, (TUNNEL_CAP_LENGTH - TUNNEL_CAP_THICKNESS) / 2)) (cap_body)
    cap_hole = cube ((TUNNEL_WIDTH, TUNNEL_HEIGHT, TUNNEL_CAP_LENGTH + OVERLAP), center = True)
    cap_hole = translate ((0, 0, TUNNEL_CAP_THICKNESS + (TUNNEL_CAP_LENGTH + OVERLAP) / 2)) (cap_hole)

    return cap_body - cap_hole


# Blerch.

scad_render_to_file (knob (), 'knob.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (switch (), 'switch.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (construction_cover (), 'construction_cover.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (construction_holder (), 'construction_holder.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (profile_lock (), 'profile_lock.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (profile_connector (), 'profile_connector.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (profile_holder (), 'profile_holder.scad', file_header = f'$fn = {SEGMENTS};')
scad_render_to_file (tunnel_cap (), 'tunnel_cap.scad', file_header = f'$fn = {SEGMENTS};')
