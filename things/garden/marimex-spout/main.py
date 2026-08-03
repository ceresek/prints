#!/usr/bin/env python3

from build123d import *
from bd_warehouse.thread import *

from shared.dimensions import *
from shared.build.shapes import *


NUT_THICKNESS_HORIZONTAL = FIV_PERIMETERS
NUT_THICKNESS_VERTICAL = 2

NUT_RIM_LENGTH = 8

NUT_DIAMETER_INNER = 82.8
NUT_DIAMETER_HOLED = NUT_DIAMETER_INNER - NUT_RIM_LENGTH*2
NUT_DIAMETER_OUTER = NUT_DIAMETER_INNER + NUT_THICKNESS_HORIZONTAL*2

NUT_THREAD_LENGTH = 11
NUT_THREAD_PITCH = 2.6
NUT_THREAD_ANGLE = 60

NUT_BUMP_COUNT = 16
NUT_BUMP_HEIGHT = 1
NUT_BUMP_DIAMETER = 8

NUT_SPOUT_GAP = 0.2
NUT_SPOUT_SQUEEZE = 0.2

SPOUT_THICKNESS_HORIZONTAL = FIV_PERIMETERS
SPOUT_THICKNESS_VERTICAL = 2

SPOUT_DIAMETER_FINAL = 33
SPOUT_DIAMETER_OUTER = 78.8
SPOUT_DIAMETER_INNER = NUT_DIAMETER_HOLED - NUT_SPOUT_GAP*2

SPOUT_HEIGHT = 33


def nut ():

    with BuildPart () as part:

        # Bumps.
        with Locations ((0, 0, - NUT_THICKNESS_VERTICAL - SPOUT_THICKNESS_VERTICAL + NUT_SPOUT_SQUEEZE)):
            with PolarLocations (NUT_DIAMETER_OUTER/2 - NUT_BUMP_DIAMETER/2 + NUT_BUMP_HEIGHT, NUT_BUMP_COUNT):
                Cylinder (NUT_BUMP_DIAMETER/2, NUT_THICKNESS_VERTICAL + SPOUT_THICKNESS_VERTICAL - NUT_SPOUT_SQUEEZE + NUT_THREAD_LENGTH, align = (Align.CENTER, Align.CENTER, Align.MIN))

        # Rim rim.
        Cylinder (NUT_DIAMETER_OUTER/2, NUT_THICKNESS_VERTICAL + SPOUT_THICKNESS_VERTICAL - NUT_SPOUT_SQUEEZE, align = (Align.CENTER, Align.CENTER, Align.MAX))
        Cylinder (NUT_DIAMETER_HOLED/2, NUT_THICKNESS_VERTICAL + SPOUT_THICKNESS_VERTICAL - NUT_SPOUT_SQUEEZE, align = (Align.CENTER, Align.CENTER, Align.MAX), mode = Mode.SUBTRACT)
        Cylinder (SPOUT_DIAMETER_OUTER/2 + NUT_SPOUT_GAP, SPOUT_THICKNESS_VERTICAL - NUT_SPOUT_SQUEEZE, align = (Align.CENTER, Align.CENTER, Align.MAX), mode = Mode.SUBTRACT)

        # Outer core.
        Cylinder (NUT_DIAMETER_OUTER/2, NUT_THREAD_LENGTH, align = (Align.CENTER, Align.CENTER, Align.MIN))
        Cylinder (NUT_DIAMETER_INNER/2, NUT_THREAD_LENGTH, align = (Align.CENTER, Align.CENTER, Align.MIN), mode = Mode.SUBTRACT)

        # For some reason does not work unless wrapped.
        with BuildPart ():
            TrapezoidalThread (
                thread_angle = NUT_THREAD_ANGLE,
                diameter = NUT_DIAMETER_INNER,
                length = NUT_THREAD_LENGTH,
                pitch = NUT_THREAD_PITCH,
                external = False,
                end_finishes = ('square', 'chamfer'))

    return part.part


def spout ():

    with BuildPart () as part:

        # Rim rim.
        with Locations ((0, 0, - NUT_THICKNESS_VERTICAL - SPOUT_THICKNESS_VERTICAL)):
            Cylinder (SPOUT_DIAMETER_OUTER/2, SPOUT_THICKNESS_VERTICAL, align = (Align.CENTER, Align.CENTER, Align.MIN))
            Cylinder (SPOUT_DIAMETER_INNER/2, SPOUT_THICKNESS_VERTICAL + NUT_THICKNESS_VERTICAL, align = (Align.CENTER, Align.CENTER, Align.MIN))
            Cylinder (SPOUT_DIAMETER_INNER/2 - SPOUT_THICKNESS_HORIZONTAL, SPOUT_THICKNESS_VERTICAL + NUT_THICKNESS_VERTICAL, align = (Align.CENTER, Align.CENTER, Align.MIN), mode = Mode.SUBTRACT)

        # Spout spout.
        with BuildPart ():
            with BuildSketch ():
                Circle (SPOUT_DIAMETER_INNER/2)
                Circle (SPOUT_DIAMETER_INNER/2 - SPOUT_THICKNESS_HORIZONTAL, mode = Mode.SUBTRACT)
            with BuildSketch (Plane ((SPOUT_HEIGHT/8, 0, SPOUT_HEIGHT/2)).rotated ((0, 22, 0))):
                Circle (SPOUT_DIAMETER_INNER/3)
                Circle (SPOUT_DIAMETER_INNER/3 - SPOUT_THICKNESS_HORIZONTAL, mode = Mode.SUBTRACT)
            with BuildSketch (Plane ((SPOUT_HEIGHT*2/3, 0, SPOUT_HEIGHT)).rotated ((0, 50, 0))):
                Circle (SPOUT_DIAMETER_FINAL/2)
                Circle (SPOUT_DIAMETER_FINAL/2 - SPOUT_THICKNESS_HORIZONTAL, mode = Mode.SUBTRACT)

            loft ()

    return part.part


export_stl (nut (), 'nut.stl')
export_stl (spout (), 'spout.stl')
