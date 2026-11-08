#!/usr/bin/env python3

from build123d import *

from shared.dimensions import *
from shared.build.shapes import *


STRAP_WIDTH = 23
STRAP_HEIGHT = 7
STRAP_FILLET = 0.3
STRAP_CHAMFER = 0.4
SIDE_DELTA_WIDTH = 5.5
SIDE_DELTA_HEIGHT = 1.2
RING_WIDTH = 5
RING_THICKNESS = TRE_PERIMETERS
CATCH_WIDTH = 6
CATCH_HEIGHT = 2.6
CATCH_THICKNESS = 1.6


def ring ():

    with BuildPart () as part:
        with BuildSketch () as sketch:
            with BuildLine () as line:
                (
                    Deltaline (0, STRAP_HEIGHT/2)
                    .x (STRAP_WIDTH/2 - SIDE_DELTA_WIDTH)
                    .xy (SIDE_DELTA_WIDTH, - SIDE_DELTA_HEIGHT)
                    .y (- STRAP_HEIGHT + SIDE_DELTA_HEIGHT*2)
                    .xy (- SIDE_DELTA_WIDTH, - SIDE_DELTA_HEIGHT)
                    .xy (- STRAP_WIDTH/2 + SIDE_DELTA_WIDTH*3/2, SIDE_DELTA_HEIGHT/2)
                    .x (- SIDE_DELTA_WIDTH/2)
                )
            mirror (line.line, about = Plane.YZ)

            inner = make_face (mode = Mode.PRIVATE)
            outer = offset (inner, amount = RING_THICKNESS, mode = Mode.PRIVATE)

            add (outer, mode = Mode.ADD)
            add (inner, mode = Mode.SUBTRACT)

        extrude (amount = RING_WIDTH)

        chamfer_faces = part.faces ().filter_by (Plane.XY)
        chamfer_edges = [ chamfer_face.outer_wire ().edges () for chamfer_face in chamfer_faces ]
        chamfer (chamfer_edges, length = STRAP_CHAMFER)

        fillet_edges = part.edges ().filter_by (Axis.Z)
        fillet (fillet_edges, radius = STRAP_FILLET)

    return part.part


def ring_inner_catch ():

    with BuildPart () as part:
        with Locations ((0, - STRAP_HEIGHT/2 + SIDE_DELTA_HEIGHT/2)):
            Box (CATCH_WIDTH, CATCH_HEIGHT, CATCH_THICKNESS, align = (Align.CENTER, Align.MIN, Align.MIN))
        add (ring ())

    return part.part


def ring_outer_catch ():

    with BuildPart () as part:
        with Locations ((0, STRAP_HEIGHT/2)):
            Box (CATCH_WIDTH, CATCH_HEIGHT, CATCH_THICKNESS, align = (Align.CENTER, Align.MAX, Align.MIN))
        add (ring ())

    return part.part


export_stl (ring (), 'ring.stl')
export_stl (ring_inner_catch (), 'ring-inner-catch.stl')
export_stl (ring_outer_catch (), 'ring-outer-catch.stl')
