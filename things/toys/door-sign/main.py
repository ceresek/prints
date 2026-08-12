#!/usr/bin/env python3

import math as _math

from build123d import *

from shared.dimensions import *
from shared.build.utils import *
from shared.build.shapes import *


LOGO_THICKNESS = 0.6

SIGN_DIAMETER_OUTER = 111
SIGN_THICKNESS_VERTICAL = 1
SIGN_THICKNESS_HORIZONTAL = TRE_PERIMETERS

PIN_DIAMETER = 3

CLICK_COUNT = 6
CLICK_WIDTH = 11
CLICK_OVERHANG = 1.2

BUMP_DIAMETER = 3
BUMP_HEIGHT = 0.13

CLICK_SLACK_VERTICAL = 0.0
CLICK_SLACK_HORIZONTAL = 0.2

CUTOUT_OFFSET = 3.33
CUTOUT_CHAMFER = 2.22

LID_HEIGHT = SIGN_THICKNESS_VERTICAL*3 + CLICK_OVERHANG + CLICK_SLACK_VERTICAL*2
BACK_HEIGHT = SIGN_THICKNESS_VERTICAL*2 + CLICK_OVERHANG + CLICK_SLACK_VERTICAL
BACK_DIAMETER_OUTER = SIGN_DIAMETER_OUTER - SIGN_THICKNESS_HORIZONTAL*2 - CLICK_SLACK_HORIZONTAL*2 - CLICK_OVERHANG*2


def lid (logos):

    with BuildPart () as part:

        # Body.
        Cylinder (SIGN_DIAMETER_OUTER/2, SIGN_THICKNESS_VERTICAL, align = ALIGN_CCB)
        Tube (SIGN_DIAMETER_OUTER/2, SIGN_DIAMETER_OUTER/2 - SIGN_THICKNESS_HORIZONTAL, LID_HEIGHT, align = ALIGN_CCB)
        Tube (PIN_DIAMETER/2 + SIGN_THICKNESS_HORIZONTAL + CLICK_SLACK_HORIZONTAL, PIN_DIAMETER/2 + CLICK_SLACK_HORIZONTAL, LID_HEIGHT - SIGN_THICKNESS_VERTICAL - CLICK_SLACK_VERTICAL, align = ALIGN_CCB)

        # Cutout thing.
        cutout_angle = 360 / len (logos)
        with BuildSketch ():
            Circle (SIGN_DIAMETER_OUTER/2, arc_size = cutout_angle, align = Align.MIN)
            offset (amount = -CUTOUT_OFFSET-CUTOUT_CHAMFER)
            offset (amount = CUTOUT_CHAMFER)
        extrude (amount = SIGN_THICKNESS_VERTICAL, mode = Mode.SUBTRACT)

        # Some angle trickery.
        click_angle = 360 * CLICK_WIDTH / _math.pi / SIGN_DIAMETER_OUTER
        bumps_shift = 180 / len (logos) - 180 / CLICK_COUNT
        click_shift = bumps_shift - click_angle/2

        # Click notch thing.
        with BuildPart () as click_notch:
            with PolarLocations (0, CLICK_COUNT, click_shift):
                with Locations ((0, 0, SIGN_THICKNESS_VERTICAL*2 + CLICK_SLACK_VERTICAL*2)):
                    Cylinder (SIGN_DIAMETER_OUTER/2, SIGN_THICKNESS_VERTICAL + CLICK_OVERHANG, arc_size = click_angle, align = Align.MIN)
                    Cylinder (SIGN_DIAMETER_OUTER/2 - SIGN_THICKNESS_HORIZONTAL - CLICK_OVERHANG, SIGN_THICKNESS_VERTICAL + CLICK_OVERHANG, arc_size = click_angle, align = Align.MIN, mode = Mode.SUBTRACT)
            chamfer (click_notch.edges ().filter_by (GeomType.CIRCLE).group_by (SortBy.RADIUS) [0].group_by (Axis.Z) [0], length = CLICK_OVERHANG)

        # Bumps.
        with BuildPart () as bumps:
            with Locations ((0, 0, SIGN_THICKNESS_VERTICAL*2 + CLICK_SLACK_VERTICAL)):
                with PolarLocations (SIGN_DIAMETER_OUTER/2 - SIGN_THICKNESS_HORIZONTAL - CLICK_SLACK_HORIZONTAL - CLICK_OVERHANG + BUMP_DIAMETER/2 - BUMP_HEIGHT, CLICK_COUNT, bumps_shift):
                    Cylinder (BUMP_DIAMETER/2, CLICK_OVERHANG + SIGN_THICKNESS_VERTICAL, align = ALIGN_CCB)
            chamfer (bumps.edges ().filter_by (GeomType.CIRCLE).group_by (Axis.Z) [0], length = BUMP_DIAMETER/2 * 0.96)
            Cylinder (SIGN_DIAMETER_OUTER/2, LID_HEIGHT, align = ALIGN_CCB, mode = Mode.INTERSECT)

    return part.part


def back (logos):

    with BuildPart () as part:

        # Body.
        Cylinder (PIN_DIAMETER/2, BACK_HEIGHT, align = ALIGN_CCB)
        Cylinder (BACK_DIAMETER_OUTER/2, SIGN_THICKNESS_VERTICAL, align = ALIGN_CCB)
        Tube (BACK_DIAMETER_OUTER/2, BACK_DIAMETER_OUTER/2 - SIGN_THICKNESS_HORIZONTAL, BACK_HEIGHT, align = ALIGN_CCB)

        # Edge.
        with Locations ((0, 0, SIGN_THICKNESS_VERTICAL + CLICK_SLACK_VERTICAL)):
            Tube (BACK_DIAMETER_OUTER/2 + CLICK_OVERHANG, BACK_DIAMETER_OUTER/2, CLICK_OVERHANG + SIGN_THICKNESS_VERTICAL, align = ALIGN_CCB)
            chamfer (part.edges ().filter_by (GeomType.CIRCLE).group_by (SortBy.RADIUS) [-1].group_by (Axis.Z) [0], length = CLICK_OVERHANG - FUDGE)

        # Some angle trickery.
        bumps_shift = 180 / len (logos) - 180 / CLICK_COUNT
        bumps_count = CLICK_COUNT * len (logos) * 3

        # Bumps.
        with BuildPart (mode = Mode.SUBTRACT) as bumps:
            with PolarLocations (BACK_DIAMETER_OUTER/2 + BUMP_DIAMETER/2 - CLICK_SLACK_HORIZONTAL - BUMP_HEIGHT, bumps_count, bumps_shift):
                Cylinder (BUMP_DIAMETER/2, SIGN_THICKNESS_VERTICAL + CLICK_OVERHANG, align = ALIGN_CCB)
            chamfer (bumps.edges ().filter_by (GeomType.CIRCLE).group_by (Axis.Z) [-1], length = BUMP_DIAMETER/2 * 0.96)

        # Click notch thing.
        notch_angle = 360 * (CLICK_WIDTH + CLICK_SLACK_HORIZONTAL*2) / _math.pi / SIGN_DIAMETER_OUTER
        with BuildPart (mode = Mode.SUBTRACT):
            with Locations (Location ((0, 0, 0), (0, 0, -notch_angle/2))):
                Cylinder (BACK_DIAMETER_OUTER/2 + CLICK_OVERHANG + FUDGE*22, BACK_HEIGHT, arc_size = notch_angle, align = Align.MIN)
                Cylinder (BACK_DIAMETER_OUTER/2 + FUDGE*22, BACK_HEIGHT, arc_size = notch_angle, align = Align.MIN, mode = Mode.SUBTRACT)

        # Logos.
        for logo_base, logo_location in zip (logos, PolarLocations (SIGN_DIAMETER_OUTER/4 + CUTOUT_OFFSET, len (logos), 180 / len (logos), rotate = False)):

            # Fetch the logo file.
            logo_name = f'logo-{logo_base}.svg'
            logo_svg = import_svg (logo_name)
            logo = Compound (logo_svg)

            # Scale to fit.
            box = logo.bounding_box ()
            scale = SIGN_DIAMETER_OUTER / max (box.size.X, box.size.Y) * 3/11
            logo = logo.scale (scale)

            # Centerize.
            box = logo.bounding_box ()
            logo = logo.translate (-box.center ())

            # Polarize.
            logo = logo.moved (logo_location)

            # Woohoo :-)
            with BuildSketch (Plane.XY.offset (SIGN_THICKNESS_VERTICAL)): add (logo)
            extrude (amount = LOGO_THICKNESS)

    return part.part


LOGOS_ONE = [ 'check', 'game', 'skull', 'sleep' ]

export_stl (lid (LOGOS_ONE), 'lid_one.stl')
export_stl (back (LOGOS_ONE), 'back_one.stl')
