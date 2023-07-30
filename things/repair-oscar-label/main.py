#!/usr/bin/env python3

from solid import *

from helpers.transform import *


SEGMENTS = 66


# Main

text_flat = text ('Mrtník 2022', font = 'Kurier Cond Heavy')
text_body = linear_extrude (2) (text_flat)
text_real = bend (text_body, (77, 20, 2), 35.5/2, SEGMENTS * 10)

text_real = rotate ((90, 0, -111)) (text_real)
text_real = translate ((0, 0, 15)) (text_real)

sync = translate ((0, 0, -11)) (cylinder (20, 8))

scad_render_to_file (text_real + sync, 'text.scad', file_header = f'$fn = {SEGMENTS};')
