import math as _math


X = 0
Y = 1
Z = 2

OVERLAP = 0.001

ONE_PERIMETER = 0.45
TWO_PERIMETERS = 0.86
TRE_PERIMETERS = 1.26
FOR_PERIMETERS = 1.67
FIV_PERIMETERS = 2.08
SIX_PERIMETERS = 2.49
SVN_PERIMETERS = 2.89
EIT_PERIMETERS = 3.30
NIN_PERIMETERS = 3.70
TEN_PERIMETERS = 4.11


def point_to_rotation (point):
    xyz_length = vector_length (point)
    xy_length = vector_length (( point [X], point [Y] ))
    angle_y = 0 - _math.degrees (_math.asin (point [Z] / xyz_length))
    angle_z = _math.degrees (_math.asin (point [Y] / xy_length))
    if point [X] < 0: angle_z = 180 - angle_z
    return ( 0, angle_y, angle_z )

def size_to_area_xy (size):
    return ( size [X], size [Y] )

def size_to_area_xz (size):
    return ( size [X], size [Z] )

def size_to_area_yz (size):
    return ( size [Y], size [Z] )

def area_to_size (area, height):
    return ( area [X], area [Y], height )

def vector_length (vector):
    return _math.sqrt (sum ([ item * item for item in vector ]))

def vector_extend (vector, increment):
    result = [ item + increment for item in vector ]
    return tuple (result)

def vector_scale (vector, scale):
    result = [ item * scale for item in vector ]
    return tuple (result)

def vector_ratio (numerator, denominator):
    result = [ numerator_item / denominator_item for ( numerator_item, denominator_item ) in zip (numerator, denominator) ]
    return tuple (result)

def vector_difference (minuend, subtrahend):
    result = [ minuend_item - subtrahend_item for ( minuend_item, subtrahend_item ) in zip (minuend, subtrahend) ]
    return tuple (result)
