import math as _math

from solid2 import *
from solid2.extensions.bosl2 import *

from components.common import *


def bend (object, box, radius, segments):

    segment_step = box [X] / segments
    segment_size = ( segment_step, box [Y], box [Z] )

    rotation_circumference = 2 * _math.pi * radius
    rotation_step = 360 * segment_step / rotation_circumference

    puzzle = []

    for segment_index in range (segments):

        segment_rotation = segment_index * rotation_step
        segment_position = segment_index * segment_step
        segment_boundary = translate (( segment_position, 0, 0 )) (cube (segment_size))
        segment_content = intersection () (object, segment_boundary)

        # Move above origin for rotation.
        segment_content = translate (( - segment_position - segment_size [X] / 2, 0, radius - segment_size [Z] / 2)) (segment_content)

        # Rotate as intended.
        segment_content = rotate (( 0, segment_rotation, 0 )) (segment_content)

        # Aggregate.
        puzzle.append (segment_content)

    # Unionize :-)
    return union () (*puzzle)


def scale_along_z (object, slice, height, factor):

    steps = _math.ceil (height / slice [Z])
    tweak = (factor - 1) / steps

    slice_base = cuboid (slice, anchor = BOTTOM)
    slice_list = [ slice_base.up (slice [Z] * step) for step in range (steps) ]
    object_list = [ object * slice for slice in slice_list ]
    scaled_list = [ object.scale ([ 1 + tweak * step, 1 + tweak * step, 1 ]) for step, object in enumerate (object_list) ]

    return union () (*scaled_list)
