#!/usr/bin/env python3

import math as _math

from solid2 import *
from solid2.extensions.bosl2 import *

from components.common import *


set_global_fn (111)


OVERLAP = 0.01


SINK_BATHROOM_HOLE_DIAMETER_UPPER = 35.5
SINK_BATHROOM_HOLE_DIAMETER_LOWER = 36.6
SINK_BATHROOM_HOLE_DEPTH = 17

SINK_KITCHEN_HOLE_DIAMETER_UPPER = 33
SINK_KITCHEN_HOLE_DIAMETER_LOWER = 34
SINK_KITCHEN_HOLE_DEPTH = 9

SINK_SHOWER_HOLE_DIAMETER_UPPER = 35
SINK_SHOWER_HOLE_DIAMETER_LOWER = 36
SINK_SHOWER_HOLE_DEPTH = 13

SCREW_HOLE_DIAMETER = 8.1
SCREW_HOLE_DISTANCE = 8.2

TUBE_HOLE_DIAMETER = 13
TUBE_HOLE_DISTANCE = 9
TUBE_HOLE_GAP = 1.7

RIM_LENGTH = 11
RIM_THICKNESS = 2


def pack (sink_hole_diameter_upper, sink_hole_diameter_lower, sink_hole_depth):

    tube_hole_angle = _math.degrees (_math.asin ((TUBE_HOLE_DIAMETER / 2 + TUBE_HOLE_GAP / 2) / TUBE_HOLE_DISTANCE))

    body = cyl (h = sink_hole_depth + RIM_THICKNESS, d1 = sink_hole_diameter_lower, d2 = sink_hole_diameter_upper, anchor = BOTTOM)
    body += cyl (h = RIM_THICKNESS, d = sink_hole_diameter_lower + RIM_LENGTH * 2, anchor = BOTTOM)
    body -= cyl (h = sink_hole_depth + RIM_THICKNESS + OVERLAP * 2, d = SCREW_HOLE_DIAMETER, anchor = BOTTOM).back (SCREW_HOLE_DISTANCE).down (OVERLAP)
    body -= cyl (h = sink_hole_depth + RIM_THICKNESS + OVERLAP * 2, d = TUBE_HOLE_DIAMETER, anchor = BOTTOM).fwd (TUBE_HOLE_DISTANCE).rotate ([0, 0, 0 + tube_hole_angle]).down (OVERLAP)
    body -= cyl (h = sink_hole_depth + RIM_THICKNESS + OVERLAP * 2, d = TUBE_HOLE_DIAMETER, anchor = BOTTOM).fwd (TUBE_HOLE_DISTANCE).rotate ([0, 0, 0 - tube_hole_angle]).down (OVERLAP)

    return body


pack (SINK_SHOWER_HOLE_DIAMETER_UPPER, SINK_SHOWER_HOLE_DIAMETER_LOWER, SINK_SHOWER_HOLE_DEPTH).save_as_scad ('pack-shower.scad')
pack (SINK_KITCHEN_HOLE_DIAMETER_UPPER, SINK_KITCHEN_HOLE_DIAMETER_LOWER, SINK_KITCHEN_HOLE_DEPTH).save_as_scad ('pack-kitchen.scad')
pack (SINK_BATHROOM_HOLE_DIAMETER_UPPER, SINK_BATHROOM_HOLE_DIAMETER_LOWER, SINK_BATHROOM_HOLE_DEPTH).save_as_scad ('pack-bathroom.scad')
