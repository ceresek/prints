import math as _math

from solid import *

from components.common import *


def bend (object, box, radius, segments):

    segment_step = box [X] / segments
    segment_size = ( segment_step, box [Y], box [Z] )

    rotation_circumference = 2 * _math.pi * radius
    rotation_step = 360 * segment_step / rotation_circumference

    stretch_factor = _math.tan (_math.radians (rotation_step / 2)) * segment_size [X] / segment_size [Z]

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
