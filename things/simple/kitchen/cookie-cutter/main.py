#!/usr/bin/env python3

from solid2 import *


set_global_fn (33)


CUTTER_EDGE_THICKNESS = 0.86
CUTTER_EDGE_HEIGHT = 1

CUTTER_BODY_THICKNESS = 1.67
CUTTER_BODY_HEIGHT = 16

CUTTER_CUSP_THICKNESS = 3
CUTTER_CUSP_HEIGHT = 3


def cutter (name):

    shape_inner = import_ (name)
    shape_outer_edge = shape_inner.offset (CUTTER_EDGE_THICKNESS)
    shape_outer_body = shape_inner.offset (CUTTER_BODY_THICKNESS)
    shape_outer_cusp = shape_inner.offset (CUTTER_CUSP_THICKNESS)

    volume_edge = (shape_outer_edge - shape_inner).linear_extrude (CUTTER_EDGE_HEIGHT)
    volume_body = (shape_outer_body - shape_inner).linear_extrude (CUTTER_BODY_HEIGHT)
    volume_cusp = (shape_outer_cusp - shape_inner).linear_extrude (CUTTER_CUSP_HEIGHT)

    cutter = volume_cusp + (volume_body + volume_edge.up (CUTTER_BODY_HEIGHT)).up (CUTTER_CUSP_HEIGHT)

    return cutter


# Main

cutter ('sheltie-one.svg').save_as_scad ('sheltie-one.scad')
cutter ('sheltie-two.svg').save_as_scad ('sheltie-two.scad')
