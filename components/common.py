X = 0
Y = 1
Z = 2

OVERLAP = 0.001

def size_to_area_xy (size):
    return ( size [X], size [Y] )

def size_to_area_xz (size):
    return ( size [X], size [Z] )

def size_to_area_yz (size):
    return ( size [Y], size [Z] )

def area_to_size (area, height):
    return ( area [X], area [Y], height )

def vector_extend (vector, increment):
    result = [ item + increment for item in vector ]
    return tuple (result)

def vector_ratio (numerator, denominator):
    result = [ numerator_item / denominator_item for ( numerator_item, denominator_item ) in zip (numerator, denominator) ]
    return tuple (result)

def vector_scale (vector, scale):
    result = [ item * scale for item in vector ]
    return tuple (result)
