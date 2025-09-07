#!/usr/bin/env python3

from solid2 import *
from solid2.extensions.bosl2 import *


set_global_fn (111)


OVERLAP = 0.001

CUP_DIAMETER = 95
CUP_THICKNESS = 1.2

LID_THICKNESS = 1
LID_OVERLAP = 3

CATCH_HEIGHT = 1
CATCH_WIDTH = 3
CATCHES = 5

LAYER = 0.2


def lid ():

    lid = (
        cyl (
            h = LID_THICKNESS + CUP_THICKNESS + LID_OVERLAP,
            d = CUP_DIAMETER + CATCH_HEIGHT/2 + LID_THICKNESS*2,
            circum = True,
            anchor = BOTTOM,
        ) -
        cyl (
            h = CUP_THICKNESS + LID_OVERLAP + OVERLAP,
            d = CUP_DIAMETER + CATCH_HEIGHT/2,
            circum = True,
            anchor = BOTTOM,
        )
        .up (LID_THICKNESS)
    )

    catch = (
        prismoid (
            size1 = (CATCH_WIDTH, CUP_THICKNESS + LID_OVERLAP),
            size2 = (CATCH_WIDTH, LAYER),
            height = CATCH_HEIGHT,
            anchor = BOTTOM + FRONT,
        )
        .rotate ((90, 0, 0))
        .up (LID_THICKNESS)
        .fwd (CUP_DIAMETER/2 + CATCH_HEIGHT/2)
    )

    catches = [ catch.rotate ((0, 0, step * 360 / CATCHES )) for step in range (CATCHES) ]

    return lid + union () (*catches)


lid ().save_as_scad ('lid.scad')
