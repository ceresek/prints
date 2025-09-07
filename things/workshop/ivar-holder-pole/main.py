#!/usr/bin/env python3

import math as _math

from solid2 import *
from solid2.extensions.bosl2 import *
from solid2.extensions.bosl2.gears import *
from solid2.extensions.bosl2.threading import *

from components.common import *
from helpers.transform import *


set_global_fn (111)


OVERLAP = 0.001

BODY_THICKNESS = FOR_PERIMETERS

POLE_DIAMETER_WOOD = 28.3
POLE_DIAMETER_METAL = 28.8

THREAD_GAP = 2
THREAD_LEAD = 1
THREAD_PITCH = 3
THREAD_SLACK = 0.8
THREAD_LENGTH = 22

THREAD_SHRINK_WOOD = 1.8
THREAD_SHRINK_METAL = 1.2

SCALE_SLICE = 0.1

WRAP_ANGLE = 30
WRAP_TEETH = 33
WRAP_CAP = 8

RING_LENGTH = 11
RING_HEIGHT = 42.42

SUPPORT_RING = 2
SUPPORT_COUNT = 2
SUPPORT_LENGTH = 210
SUPPORT_DIAMETER = 25.2
SUPPORT_THICKNESS_THIN = ONE_PERIMETER
SUPPORT_THICKNESS_THICK = 1.1


def wrap (pole_diameter, thread_shrink, closed):

    thread_diameter = pole_diameter + BODY_THICKNESS * 2 + THREAD_PITCH / 2

    thread = trapezoidal_threaded_rod (
        d = thread_diameter + THREAD_SLACK,
        l = THREAD_LENGTH + OVERLAP * 2,
        pitch = THREAD_PITCH,
        end_len1 = THREAD_LEAD,
        internal = True,
        anchor = BOTTOM,
    )

    thread = scale_along_z (
        thread,
        [thread_diameter + THREAD_SLACK, thread_diameter + THREAD_SLACK, SCALE_SLICE],
        THREAD_LENGTH + OVERLAP * 2,
        1 - thread_shrink / (thread_diameter + THREAD_SLACK)
    )

    thread = thread.down (OVERLAP)

    body = (
        cyl (
            d = thread_diameter + THREAD_SLACK + BODY_THICKNESS * 2,
            l = THREAD_LENGTH + closed * BODY_THICKNESS,
            anchor = BOTTOM)
        +
        spur_gear (
            _math.pi * (thread_diameter + THREAD_SLACK + BODY_THICKNESS * 2) / WRAP_TEETH,
            WRAP_TEETH,
            WRAP_CAP,
            helical = WRAP_ANGLE,
            anchor = TOP,
        )
        .up (THREAD_LENGTH + closed * BODY_THICKNESS)
    )

    body -= thread

    return body


def ring (pole_diameter):

    thread_diameter = pole_diameter + BODY_THICKNESS * 2 + THREAD_PITCH / 2

    body = (
        cyl (d = thread_diameter, l = RING_LENGTH + BODY_THICKNESS, anchor = BOTTOM)
        +
        cuboid ([thread_diameter, thread_diameter / 2 + RING_HEIGHT + BODY_THICKNESS, RING_LENGTH + BODY_THICKNESS], anchor = BOTTOM + BACK)
        +
        trapezoidal_threaded_rod (
            d = thread_diameter,
            l = THREAD_LENGTH,
            pitch = THREAD_PITCH,
            end_len2 = THREAD_LEAD,
            anchor = BOTTOM,
        )
        .up (RING_LENGTH + BODY_THICKNESS)
        -
        cuboid ([thread_diameter + OVERLAP * 2, RING_HEIGHT, RING_LENGTH + OVERLAP], anchor = BOTTOM + BACK)
        .fwd (thread_diameter / 2)
        .up (BODY_THICKNESS)
        -
        cyl (d = pole_diameter, l = BODY_THICKNESS + RING_LENGTH + THREAD_LENGTH + OVERLAP * 2, anchor = BOTTOM)
        .down (OVERLAP)
        -
        cuboid ([thread_diameter + OVERLAP * 2, THREAD_GAP, THREAD_LENGTH + OVERLAP], anchor = BOTTOM)
        .up (RING_LENGTH + BODY_THICKNESS)
        .rotate ([0, 0, 45])
        -
        cuboid ([THREAD_GAP, thread_diameter + OVERLAP * 2, THREAD_LENGTH + OVERLAP], anchor = BOTTOM)
        .up (RING_LENGTH + BODY_THICKNESS)
        .rotate ([0, 0, 45])
    )

    return body


def support ():

    ring = (
        cyl (
            d1 = SUPPORT_DIAMETER + SUPPORT_THICKNESS_THIN * 2,
            d2 = SUPPORT_DIAMETER + SUPPORT_THICKNESS_THICK * 2,
            l = SUPPORT_RING + OVERLAP,
            anchor = BOTTOM)
        +
        cyl (
            d = SUPPORT_DIAMETER + SUPPORT_THICKNESS_THICK * 2,
            l = SUPPORT_RING + OVERLAP,
            anchor = BOTTOM)
        .up (SUPPORT_RING)
        +
        cyl (
            d1 = SUPPORT_DIAMETER + SUPPORT_THICKNESS_THICK * 2,
            d2 = SUPPORT_DIAMETER + SUPPORT_THICKNESS_THIN * 2,
            l = SUPPORT_RING + OVERLAP,
            anchor = BOTTOM)
        .up (SUPPORT_RING * 2)
    )

    ring_list = [ ring.up (index * (SUPPORT_LENGTH - SUPPORT_RING * 3) / SUPPORT_COUNT) for index in range (SUPPORT_COUNT + 1) ]

    body = (
        cyl (
            d = SUPPORT_DIAMETER + SUPPORT_THICKNESS_THIN * 2,
            l = SUPPORT_LENGTH,
            anchor = BOTTOM)
    )

    pole = (
        cyl (
            d = SUPPORT_DIAMETER,
            l = SUPPORT_LENGTH + OVERLAP * 2,
            anchor = BOTTOM)
        .down (OVERLAP)
    )

    return union () (*ring_list) + body - pole


wrap (POLE_DIAMETER_WOOD, THREAD_SHRINK_WOOD, False).save_as_scad ('wrap-wood.scad')
wrap (POLE_DIAMETER_METAL, THREAD_SHRINK_METAL, True).save_as_scad ('wrap-metal.scad')

ring (POLE_DIAMETER_WOOD).save_as_scad ('ring-wood.scad')
ring (POLE_DIAMETER_METAL).save_as_scad ('ring-metal.scad')

support ().save_as_scad ('support.scad')
